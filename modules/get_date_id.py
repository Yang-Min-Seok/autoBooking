#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re

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

# Get badminton date ID
"""
Returns the date ID for badminton reservation on the specified day.

Args:
    target_day (str): The day to search for (e.g., "17")
    facility_id (int): The facility ID (default: 420 - 鳥屋野総合体育館)

Returns:
    str: The date ID (e.g., "13118") or None
"""
def get_badminton_date_id(target_day, facility_id):

    try:
        session = requests.Session()
        session.headers.update(HEADERS)
        
        url = f"{BASE_URL}/facility/{facility_id}/schedule"
        response = session.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        schedule_table = soup.find('table', class_='c-table01')
        
        if not schedule_table:
            return None
        
        for row in schedule_table.find_all('tr'):
            day_cell = row.find('td', class_='day-sticky')
            if not day_cell:
                continue
            
            day_match = re.search(r'(\d+)日', day_cell.get_text(strip=True))
            if not day_match or day_match.group(1) != str(target_day):
                continue
            
            cells = row.find_all('td')
            if len(cells) < 3:
                continue
            
            badminton_cell = cells[2]
            reserve_link = badminton_cell.find('a', href=True)
            
            if reserve_link:
                href = reserve_link['href']
                match = re.search(r'/schedule/course/(\d+)/1', href)
                if match:
                    return match.group(1)
        
        return None
        
    except Exception as e:
        print(f"Error occurred: {e}")
        return None
