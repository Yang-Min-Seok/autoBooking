#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re

# 상수 정의
BASE_URL = "https://niigata-kaikou.jp"
DEFAULT_FACILITY_ID = 420
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

def get_badminton_date_id(target_day, facility_id=DEFAULT_FACILITY_ID):
    """
    특정 날짜의 배드민턴 예약 날짜 ID를 반환합니다.
    
    Args:
        target_day (str): 찾고 싶은 날짜 (예: "17")
        facility_id (int): 시설 ID (기본값: 420 - 鳥屋野総合体育館)
    
    Returns:
        str: 날짜 ID (예: "13118") 또는 None
    """
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
        print(f"오류 발생: {e}")
        return None

if __name__ == "__main__":
    # 테스트 실행
    date_id = get_badminton_date_id("17")
    if date_id:
        print(f"성공! 날짜 ID: {date_id}")
        print(f"예약 URL: {BASE_URL}/schedule/course/{date_id}/1")
    else:
        print("날짜 ID를 찾을 수 없습니다.")
