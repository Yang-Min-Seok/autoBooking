#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
import time
from datetime import datetime
from get_date_id import get_badminton_date_id
from get_reservation_ids import get_reservation_ids_by_time_slot
from niigata_macro import NiigataReservationMacro

# 상수 정의
FACILITY_NAME = '鳥屋野総合体育館'
FACILITY_ID = 420
EQUIPMENT = 'バドミントン'
COURSE_NAME = 'バドミントン 1'
WEEKDAY_MAP = ['月', '火', '水', '木', '金', '土', '日']

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('reservation.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def load_user_data(json_file='my_data.json'):
    """사용자 데이터를 JSON 파일에서 로드"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"사용자 데이터 로드 완료: {json_file}")
        return data
    except FileNotFoundError:
        logger.error(f"JSON 파일을 찾을 수 없습니다: {json_file}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"JSON 파싱 오류: {e}")
        return None

def parse_date_and_time(user_data):
    """사용자 데이터에서 날짜와 시간 정보 파싱"""
    try:
        date_obj = datetime.strptime(user_data['DATE'], '%Y-%m-%d')
        day = str(date_obj.day)
        time_slot = f"{user_data['TIME']}時"
        
        logger.info(f"파싱된 정보 - 날짜: {day}일, 시간대: {time_slot}")
        return day, time_slot, date_obj
        
    except ValueError as e:
        logger.error(f"날짜/시간 파싱 오류: {e}")
        return None, None, None

def find_available_reservation(date_id, target_time_slot):
    """예약 가능한 코트 ID와 이름 찾기"""
    try:
        url = f"https://niigata-kaikou.jp/schedule/course/{date_id}/1"
        logger.info(f"예약 가능한 코트 조회: {url}")
        
        time_slot_data = get_reservation_ids_by_time_slot(url)
        
        if target_time_slot in time_slot_data and time_slot_data[target_time_slot]:
            available_courts = time_slot_data[target_time_slot]
            
            # 튜플인 경우: (ID, 코트명), 문자열인 경우: ID만
            if available_courts and isinstance(available_courts[0], tuple):
                court_info = [f"{court} (ID: {res_id})" for res_id, court in available_courts]
                logger.info(f"예약 가능한 코트들: {court_info}")
                first_id, first_court = available_courts[0]
            else:
                logger.info(f"예약 가능한 코트 ID들: {available_courts}")
                first_id = available_courts[0]
                first_court = "선택된 코트"
            
            return first_id, first_court
        else:
            logger.warning(f"'{target_time_slot}' 시간대에 예약 가능한 코트가 없습니다.")
            return None, None
            
    except Exception as e:
        logger.error(f"예약 가능한 코트 조회 실패: {e}")
        return None, None

def make_reservation_with_data(user_data, date_obj, course_time_id, court_name):
    """사용자 데이터로 예약 실행"""
    try:
        macro = NiigataReservationMacro()
        
        # 날짜 포맷 변환
        weekday = WEEKDAY_MAP[date_obj.weekday()]
        formatted_date = f"{date_obj.year}年{date_obj.month}月{date_obj.day}日（{weekday}）"
        course_time_name = f"{user_data['TIME']}時"
        
        logger.info(f"예약 시작 - 코트: {court_name}, 시간: {course_time_name}")
        
        success = macro.make_reservation(
            course_time_id=course_time_id,
            facility_name=FACILITY_NAME,
            facility_id=FACILITY_ID,
            date=formatted_date,
            equipment=EQUIPMENT,
            course_name=COURSE_NAME,
            course_time_name=course_time_name,
            name=user_data['NAME'],
            tel=user_data['PHONE_NUMBER'],
            email=user_data['E_MAIL']
        )
        
        if success:
            logger.info(f"예약 완료 - 코트: {court_name}")
        
        return success, court_name
        
    except Exception as e:
        logger.error(f"예약 실행 실패: {e}")
        return False, None

def main():
    """메인 실행 함수"""
    start_time = time.time()
    logger.info("=== 니이가타 배드민턴 자동 예약 시작 ===")
    
    try:
        # 1. 사용자 데이터 로드
        user_data = load_user_data()
        if not user_data:
            return False
        
        # 2. 날짜와 시간 정보 파싱
        day, time_slot, date_obj = parse_date_and_time(user_data)
        if not all([day, time_slot, date_obj]):
            return False
        
        # 3. 날짜 ID 가져오기
        logger.info(f"{day}일 배드민턴 예약 날짜 ID 조회 중...")
        date_id = get_badminton_date_id(day)
        if not date_id:
            logger.error(f"{day}일 배드민턴 예약 날짜 ID를 찾을 수 없습니다.")
            return False
        
        # 4. 예약 가능한 코트 ID와 이름 찾기
        logger.info(f"'{time_slot}' 시간대 예약 가능한 코트 조회 중...")
        course_time_id, court_name = find_available_reservation(date_id, time_slot)
        if not course_time_id:
            logger.error(f"'{time_slot}' 시간대에 예약 가능한 코트가 없습니다.")
            return False
        
        # 5. 최종 예약 실행
        logger.info("예약 실행 중...")
        success, reserved_court = make_reservation_with_data(user_data, date_obj, course_time_id, court_name)
        
        # 실행 시간 계산
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        if success:
            logger.info("=== 예약이 성공적으로 완료되었습니다! ===")
            logger.info(f"예약된 코트: {reserved_court}")
            logger.info(f"총 소요 시간: {elapsed_time:.2f}초")
            print(f"[성공] 예약이 성공적으로 완료되었습니다!")
            print(f"예약 코트: {reserved_court}")
            print(f"소요시간: {elapsed_time:.2f}초")
        else:
            logger.error("=== 예약에 실패했습니다 ===")
            logger.info(f"실패까지 소요 시간: {elapsed_time:.2f}초")
            print(f"[실패] 예약에 실패했습니다. 로그를 확인해주세요. (소요시간: {elapsed_time:.2f}초)")
        
        return success
        
    except Exception as e:
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.error(f"예상치 못한 오류 발생: {e}")
        logger.info(f"오류까지 소요 시간: {elapsed_time:.2f}초")
        print(f"[오류] 예상치 못한 오류가 발생했습니다. (소요시간: {elapsed_time:.2f}초)")
        return False

if __name__ == "__main__":
    main()