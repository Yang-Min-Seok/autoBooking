import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
import re
import json
import time
from typing import List, Dict, Tuple

# define constants
BASE_URL = "https://niigata-kaikou.jp"
RESERVE_PATTERN = re.compile(r'/schedule/reserve/(\d+)')

# Get reservation IDs by time slot
def _extract_reservation_ids(soup):
    time_headers = soup.find_all('th', class_='schedule-type')
    time_slots = [header.get_text(strip=True) for header in time_headers]
    
    time_slot_data = {time_slot: [] for time_slot in time_slots}
    
    for row in soup.find_all('tr'):
        court_name_cell = row.find('td', class_='day-sticky')
        if not court_name_cell:
            continue
        
        court_name = court_name_cell.get_text(strip=True)
        time_cells = row.find_all('td', class_='text-center')
        
        for i, cell in enumerate(time_cells[1:], start=0):
            reservation_link = cell.find('a', href=RESERVE_PATTERN)
            
            if reservation_link and i < len(time_slots):
                href = reservation_link.get('href')
                match = RESERVE_PATTERN.search(href)
                
                if match:
                    reservation_id = match.group(1)
                    time_slot = time_slots[i]
                    time_slot_data[time_slot].append((reservation_id, court_name))
    
    return time_slot_data

# Get reservation IDs by time slot
def get_reservation_ids_by_time_slot(url: str, session=None) -> Dict[str, List[Tuple[str, str]]]:
    try:
        if session is None:
            session = requests.Session()
            adapter = HTTPAdapter(pool_connections=10, pool_maxsize=10)
            session.mount('http://', adapter)
            session.mount('https://', adapter)
        request_started = time.perf_counter()
        response = session.get(url, timeout=(5, 10))
        print(f"Court-list request completed in {time.perf_counter() - request_started:.3f}s")
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        return _extract_reservation_ids(soup)
        
    except Exception as e:
        print(f"Error occurred: {e}")
        return {}
