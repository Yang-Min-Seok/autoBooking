#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import logging

# 상수 정의
BASE_URL = "https://niigata-kaikou.jp"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Cache-Control': 'max-age=0',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1'
}

logger = logging.getLogger(__name__)

class NiigataReservationMacro:
    """新潟市スポーツ施設自動予約マクロ"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.csrf_token = None
    
    def get_csrf_token(self, course_time_id):
        """CSRF 토큰 획득"""
        try:
            url = f"{BASE_URL}/schedule/reserve/{course_time_id}"
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            csrf_input = soup.find('input', {'name': '_token'})
            
            if csrf_input and csrf_input.get('value'):
                self.csrf_token = csrf_input['value']
                logger.info(f"CSRF 토큰 획득: {self.csrf_token[:20]}...")
                return True
            else:
                logger.error("CSRF 토큰을 찾을 수 없습니다.")
                return False
                
        except Exception as e:
            logger.error(f"CSRF 토큰 획득 실패: {e}")
            return False
    
    def make_reservation(self, course_time_id, facility_name, facility_id, date, equipment, course_name, course_time_name, name, tel, email):
        """예약 실행"""
        try:
            logger.info("예약 시작")
            
            # CSRF 토큰 획득
            if not self.get_csrf_token(course_time_id):
                return False
            
            # 1단계: confirm 모드로 예약 확인 페이지 접근
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
            
            logger.info(f"confirm 요청 응답: {response.status_code}")
            
            if response.status_code == 200:
                # 예약자 정보 입력 페이지인 경우 바로 send 모드로 전송
                if "予約者情報の入力" in response.text:
                    logger.info("예약자 정보 입력 페이지 확인됨")
                    return self.send_reservation(response.text)
                else:
                    logger.error("예상치 못한 페이지입니다.")
                    return False
            else:
                logger.error(f"confirm 요청 실패: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"예약 실행 실패: {e}")
            return False
    
    def send_reservation(self, confirm_page_html):
        """send 모드로 예약 실행"""
        try:
            logger.info("send 모드로 예약 실행")
            
            soup = BeautifulSoup(confirm_page_html, 'html.parser')
            
            # POST 폼 찾기
            target_form = soup.find('form', {'method': 'post'})
            if not target_form:
                logger.error("POST 폼을 찾을 수 없습니다.")
                return False
            
            # 폼 데이터 수집
            form_data = {}
            inputs = target_form.find_all('input')
            
            for inp in inputs:
                name = inp.get('name')
                value = inp.get('value', '')
                form_data[name] = value
            
            # mode를 send로 변경
            form_data['mode'] = 'send'
            
            logger.info(f"폼 데이터 수집 완료: {len(form_data)}개 필드")
            
            # POST 요청으로 예약 실행
            post_url = f"{BASE_URL}/schedule/post?"
            response = self.session.post(
                post_url,
                data=form_data,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            
            logger.info(f"예약 요청 응답: {response.status_code}")
            
            if response.status_code == 302:
                # 리다이렉트 응답 (예약 성공)
                location = response.headers.get('location', '')
                if 'reserve_thanks' in location:
                    logger.info("예약이 성공적으로 완료되었습니다!")
                    logger.info(f"리다이렉트 위치: {location}")
                    return True
                else:
                    logger.warning(f"예상치 못한 리다이렉트: {location}")
                    return True
            elif response.status_code == 200:
                # 응답 내용 확인
                response_text = response.text
                if "予約完了" in response_text:
                    logger.info("예약이 성공적으로 완료되었습니다!")
                    return True
                elif "エラー" in response_text:
                    logger.error("예약 중 오류가 발생했습니다.")
                    return False
                else:
                    logger.warning("예약 결과를 확인할 수 없습니다.")
                    return True
            else:
                logger.error(f"예약 요청 실패: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"예약 실행 실패: {e}")
            return False
    

if __name__ == "__main__":
    # 테스트 실행
    macro = NiigataReservationMacro()
    success = macro.make_reservation(
        course_time_id=250345,
        facility_name='鳥屋野総合体育館',
        facility_id=420,
        date='2025年10月15日（水）',
        equipment='バドミントン',
        course_name='バドミントン 1',
        course_time_name='9-11時',
        name='apple',
        tel='0123456789',
        email='jeongwonjun0718@gmail.com'
    )
    
    print("예약 성공!" if success else "예약 실패!")
