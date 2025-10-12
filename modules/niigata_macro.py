#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import logging

# Define constants
BASE_URL = "https://niigata-kaikou.jp"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1'
}

logger = logging.getLogger(__name__)

class NiigataReservationMacro:
    """Niigata City Sports Facility Auto Reservation Macro"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.csrf_token = None
    
    def get_csrf_token(self, course_time_id):
        """Obtain CSRF token"""
        try:
            url = f"{BASE_URL}/schedule/reserve/{course_time_id}"
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            csrf_input = soup.find('input', {'name': '_token'})
            
            if csrf_input and csrf_input.get('value'):
                self.csrf_token = csrf_input['value']
                logger.info(f"CSRF token obtained: {self.csrf_token[:20]}...")
                return True
            else:
                logger.error("CSRF token not found.")
                return False
                
        except Exception as e:
            logger.error(f"Failed to obtain CSRF token: {e}")
            return False
    
    def make_reservation(self, course_time_id, facility_name, facility_id, date, equipment, course_name, course_time_name, name, tel, email):
        """Execute reservation"""
        try:
            logger.info("Start reservation")
            
            # Obtain CSRF token
            if not self.get_csrf_token(course_time_id):
                return False
            
            # Step 1: Access reservation confirmation page in confirm mode
            reservation_data = {
                '_token': self.csrf_token,
                'course_time_id': course_time_id,
                'facility_name': facility_name,
                'facility_id': facility_id,
                'date': date,
                'equipment': equipment,
                'course_name': course_name,
                'course_time_name': course_time_name,
                'name': name,
                'tel': tel,
                'email': email,
                'mode': 'confirm'
            }
            
            post_url = f"{BASE_URL}/schedule/post?"
            response = self.session.post(
                post_url,
                data=reservation_data,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            
            logger.info(f"confirm request response: {response.status_code}")
            
            if response.status_code == 200:
                # If it is the reservation information input page, immediately send in send mode
                if "予約者情報の入力" in response.text:
                    logger.info("Reservation information input page detected")
                    return self.send_reservation(response.text)
                else:
                    logger.error("Unexpected page.")
                    return False
            else:
                logger.error(f"confirm request failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Reservation execution failed: {e}")
            return False
    
    def send_reservation(self, confirm_page_html):
        """Execute reservation in send mode"""
        try:
            logger.info("Execute reservation in send mode")
            
            soup = BeautifulSoup(confirm_page_html, 'html.parser')
            
            # Find POST form
            target_form = soup.find('form', {'method': 'post'})
            if not target_form:
                logger.error("POST form not found.")
                return False
            
            # Collect form data
            form_data = {}
            inputs = target_form.find_all('input')
            
            for inp in inputs:
                name = inp.get('name')
                value = inp.get('value', '')
                form_data[name] = value
            
            # Change mode to send
            form_data['mode'] = 'send'
            
            logger.info(f"Form data collected: {len(form_data)} fields")
            
            # Execute reservation with POST request
            post_url = f"{BASE_URL}/schedule/post?"
            response = self.session.post(
                post_url,
                data=form_data,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            
            logger.info(f"Reservation request response: {response.status_code}")
            
            if response.status_code == 302:
                # Redirect response (reservation successful)
                location = response.headers.get('location', '')
                if 'reserve_thanks' in location:
                    logger.info("Reservation completed successfully!")
                    logger.info(f"Redirect location: {location}")
                    return True
                else:
                    logger.warning(f"Unexpected redirect: {location}")
                    return True
            elif response.status_code == 200:
                # Check response content
                response_text = response.text
                if "予約完了" in response_text:
                    logger.info("Reservation completed successfully!")
                    return True
                elif "エラー" in response_text:
                    logger.error("An error occurred during reservation.")
                    return False
                else:
                    logger.warning("Unable to confirm reservation result.")
                    return True
            else:
                logger.error(f"Reservation request failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Reservation execution failed: {e}")
            return False
