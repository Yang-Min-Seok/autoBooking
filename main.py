#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import logging
import time
from datetime import timedelta
from datetime import datetime
from modules.get_date_id import get_badminton_date_id
from modules.get_reservation_ids import get_reservation_ids_by_time_slot
from modules.niigata_macro import NiigataReservationMacro

# Define constants
DAY_AFTER = 6
EQUIPMENT = 'バドミントン'
WEEKDAY_MAP = ['月', '火', '水', '木', '金', '土', '日']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "logs", "reservation.log")

# Set logging
# Ensure logs directory exists before configuring FileHandler
logs_dir = os.path.join(BASE_DIR, "logs")
if not os.path.exists(logs_dir):
    try:
        os.makedirs(logs_dir, exist_ok=True)
    except Exception as e:
        # If we can't create logs dir, fallback to console only
        print(f"[WARN] Could not create logs directory: {e}")
        LOG_FILE = None

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8') if LOG_FILE else logging.NullHandler(),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Facility name and ID mapping (edit these dictionaries as needed)
FACILITY_NAME_MAP = {
    'HIGASHI': '東総合スポーツセンター',
    'KITA': '北地区スポーツセンター',
    'TOYANO': '鳥屋野総合体育館',
    'NISHI': '西総合スポーツセンター',
    'KAMEDA': '亀田総合体育館',
}
FACILITY_ID_MAP = {
    'HIGASHI': 413,
    'KITA': 408,
    'TOYANO': 420,
    'NISHI': 442,
    'KAMEDA': 429,
}

# Load user data from my_data.json
def load_user_data(json_file='my_data.json'):
    try:
        with open(os.path.join(BASE_DIR, json_file), 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"[INFO] User data loaded: {json_file}")

        # Map facility name and id if keyword is used
        facility_key = data.get('FACILITY_NAME')
        if facility_key in FACILITY_NAME_MAP:
            data['FACILITY_NAME'] = FACILITY_NAME_MAP[facility_key]
        if facility_key in FACILITY_ID_MAP:
            data['FACILITY_ID'] = FACILITY_ID_MAP[facility_key]

        return data
    except FileNotFoundError:
        logger.error(f"[ERROR] File not found: {json_file}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"[ERROR] JSON decode error in {json_file}: {e}")
        return None

# Get date and time from user data
def parse_date_and_time(user_data):
    try:
        # Set date_obj to DAY_AFTER days after today
        today = datetime.now()
        date_obj = today + timedelta(days=DAY_AFTER)
        day = str(date_obj.day)
        time_slot = f"{user_data['TIME']}時"
        facility_name = user_data['FACILITY_NAME']
        facility_id = user_data['FACILITY_ID']

        logger.info(f"[INFO] Parsed information - date: {day}th, time slot: {time_slot}, facility: {facility_name} {date_obj.strftime('%Y-%m-%d')}")
        return day, time_slot, date_obj, facility_name, facility_id

    except Exception as e:
        logger.error(f"[ERROR] Date/time parsing error: {e}")
        return None, None, None, None, None

# Find available reservation
def find_available_reservation(date_id, target_time_slot):

    try:
        url = f"https://niigata-kaikou.jp/schedule/course/{date_id}/1"
        logger.info(f"[INFO] Checking available courts: {url}")

        time_slot_data = get_reservation_ids_by_time_slot(url)
        
        if target_time_slot in time_slot_data and time_slot_data[target_time_slot]:
            available_courts = time_slot_data[target_time_slot]
            
            # If tuple: (ID, court name), if string: only ID
            if available_courts and isinstance(available_courts[0], tuple):
                court_info = [f"{court} (ID: {res_id})" for res_id, court in available_courts]
                logger.info(f"Available courts: {court_info}")
                first_id, first_court = available_courts[0]
            else:
                logger.info(f"Available court IDs: {available_courts}")
                first_id = available_courts[0]
                first_court = "Selected court"
            
            return first_id, first_court
        else:
            logger.warning(f"No available courts for time slot '{target_time_slot}'.")
            return None, None
            
    except Exception as e:
        logger.error(f"Failed to check available courts: {e}")
        return None, None

# Execute reservation with user data
def make_reservation_with_data(user_data, date_obj, course_time_id, court_name, course_name):
    try:
        macro = NiigataReservationMacro()
        
        # Transform date to required format
        weekday = WEEKDAY_MAP[date_obj.weekday()]
        formatted_date = f"{date_obj.year}年{date_obj.month}月{date_obj.day}日（{weekday}）"
        course_time_name = f"{user_data['TIME']}時"

        logger.info(f"Start reservation - court: {court_name}, time: {course_time_name}")

        success = macro.make_reservation(
            course_time_id=course_time_id,
            date=formatted_date,
            equipment=EQUIPMENT,
            course_time_name=course_time_name,
            course_name=course_name,
            facility_name=user_data['FACILITY_NAME'],
            facility_id=user_data['FACILITY_ID'],
            name=user_data['NAME'],
            tel=user_data['PHONE_NUMBER'],
            email=user_data['E_MAIL']
        )
        
        if success:
            logger.info(f"Reservation completed - court: {court_name}")
        
        return success, court_name
        
    except Exception as e:
        logger.error(f"Reservation execution failed: {e}")
        return False, None

# Main execution function
def main():
    # Wait until next 07:00:00 before starting main logic
    def wait_until(hour=7, minute=0, second=0):
        now = datetime.now()
        target = now.replace(hour=hour, minute=minute, second=second, microsecond=0)
        if now >= target:
            logger.info("Target time already passed for today. Proceeding without wait.")
            return True
        remaining = (target - now).total_seconds()
        logger.info(f"Waiting until {target.strftime('%Y-%m-%d %H:%M:%S')} (sleep {int(remaining)}s)")
        try:
            # Sleep in chunks to allow graceful interrupt
            while remaining > 0:
                chunk = min(60, remaining)
                time.sleep(chunk)
                remaining -= chunk
            # final short spin to be precise
            while datetime.now() < target:
                time.sleep(0.05)
            return True
        except KeyboardInterrupt:
            logger.info("Waiting interrupted by user.")
            return False

    should_continue = wait_until(7, 0, 0)
    if not should_continue:
        return False

    start_time = time.time()
    logger.info(f"### Start reservation ###")
    
    try:
        # 1. Load user data
        user_data = load_user_data()
        if not user_data:
            logger.error("[ERROR] Failed to load user data.")
            return False

        # 2. Parse date and time information
        day, time_slot, date_obj, facility_name, facility_id = parse_date_and_time(user_data)
        if not all([day, time_slot, date_obj, facility_name, facility_id]):
            logger.error("[ERROR] Invalid date/time/facility information.")
            return False

        # 3. Get date ID
        logger.info(f"[INFO] Searching booking id for {day}...")
        date_id = get_badminton_date_id(day, facility_id)
        if not date_id:
            logger.error(f"[ERROR] Can't find booking id for {day}...")
            return False

        # 4. Find available reservation
        logger.info(f"[INFO] Checking available courts: {time_slot}...")
        time_slot_data = get_reservation_ids_by_time_slot(f"https://niigata-kaikou.jp/schedule/course/{date_id}/1")
        available_courts = time_slot_data.get(time_slot, [])
        if not available_courts:
            logger.error(f"[ERROR] Can't find available courts for '{time_slot}'...")
            return False

        # 5. Make reservations
        court_no = int(user_data.get('COURT_NO', 1))
        reserved_count = 0
        reserved_courts = []
        for idx, (course_time_id, court_name) in enumerate(available_courts):
            if reserved_count >= court_no:
                break
            # Use course_time_id as course_name
            course_name = course_time_id
            logger.info(f"[INFO] Making reservation for court: {court_name} (ID: {course_time_id})...")
            success, reserved_court = make_reservation_with_data(user_data, date_obj, course_time_id, court_name, course_name)
            if success:
                reserved_count += 1
                reserved_courts.append(court_name)
                logger.info(f"Reservation completed - court: {court_name}")
            else:
                logger.error(f"Reservation failed for court: {court_name}")

        end_time = time.time()
        elapsed_time = end_time - start_time

        if reserved_count == court_no:
            logger.info(f"### Reservation has been completed successfully for {reserved_count} courts ###")
            logger.info(f"Reserved courts : {reserved_courts}")
            logger.info(f"Total elapsed time: {elapsed_time:.2f} seconds")
            return True
        else:
            logger.error(f"=== Reservation failed ({reserved_count}/{court_no} courts reserved) ===")
            logger.info(f"Total elapsed time: {elapsed_time:.2f} seconds")
            return False

    except Exception as e:
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.error(f"Unexpected error occurred: {e}")
        logger.info(f"Time taken until error: {elapsed_time:.2f} seconds")
        return False

if __name__ == "__main__":
    main()
