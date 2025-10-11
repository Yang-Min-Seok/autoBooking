import requests
from bs4 import BeautifulSoup
import re
import json
from typing import List, Dict, Tuple

# 상수 정의
BASE_URL = "https://niigata-kaikou.jp"
RESERVE_PATTERN = re.compile(r'/schedule/reserve/(\d+)')


def _extract_reservation_ids(soup):
    """HTML에서 예약 ID들과 코트 이름을 추출하는 내부 함수"""
    time_headers = soup.find_all('th', class_='schedule-type')
    time_slots = [header.get_text(strip=True) for header in time_headers]
    
    # 시간대별로 (예약ID, 코트명) 튜플 리스트 저장
    time_slot_data = {time_slot: [] for time_slot in time_slots}
    
    for row in soup.find_all('tr'):
        # 코트명 찾기
        court_name_cell = row.find('td', class_='day-sticky')
        if not court_name_cell:
            continue
        
        court_name = court_name_cell.get_text(strip=True)
        time_cells = row.find_all('td', class_='text-center')
        
        # 첫 번째 셀은 코트명이므로 제외하고 처리
        for i, cell in enumerate(time_cells[1:], start=0):
            reservation_link = cell.find('a', href=RESERVE_PATTERN)
            
            if reservation_link and i < len(time_slots):
                href = reservation_link.get('href')
                match = RESERVE_PATTERN.search(href)
                
                if match:
                    reservation_id = match.group(1)
                    time_slot = time_slots[i]
                    # (예약ID, 코트명) 튜플로 저장
                    time_slot_data[time_slot].append((reservation_id, court_name))
    
    return time_slot_data


def get_reservation_ids_by_time_slot(url: str) -> Dict[str, List[Tuple[str, str]]]:
    """
    시간대별로 예약 ID와 코트명을 그룹화하여 반환하는 함수
    
    Args:
        url (str): 스케줄 페이지 URL
        
    Returns:
        Dict[str, List[Tuple[str, str]]]: 시간대별 (예약ID, 코트명) 튜플 리스트
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        return _extract_reservation_ids(soup)
        
    except Exception as e:
        print(f"오류 발생: {e}")
        return {}


if __name__ == "__main__":
    # 테스트 실행
    test_url = f"{BASE_URL}/schedule/course/13118/1"
    time_slot_data = get_reservation_ids_by_time_slot(test_url)
    
    print("=== 시간대별 예약 정보 ===")
    for time_slot, reservations in time_slot_data.items():
        print(f"\n{time_slot}:")
        for res_id, court_name in reservations:
            print(f"  - {court_name} (ID: {res_id})")