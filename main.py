from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv(dotenv_path="info.env")
TARGET_URL = os.getenv("TARGET_URL")

def automate_task():
    print(f"[INFO] auto booking start → {TARGET_URL}")

    # 옵션 설정 (GUI 모드)
    options = webdriver.ChromeOptions()
    
    # GUI 모드를 테스트 용으로 활성화
    # 배포 시 아래 주석을 해제하고 실행하면 Headless 모드로 변경됩니다.
    # options.add_argument("--headless")  # 배포 시 Headless 모드로 실행
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option('prefs', {'intl.accept_languages': 'ja'})

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # STEP 1: 예약 페이지 접속
        driver.get(TARGET_URL)
        print("[INFO] access success")
        time.sleep(2)

        # STEP 2: 첫 번째 토요일의 배드민턴 ○予約 클릭
        rows = driver.find_elements(By.CSS_SELECTOR, "table.c-table01 tbody tr")
        saturday_count = 0
        target_a = None

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) < 3:
                continue

            if "土" in cells[1].text:
                saturday_count += 1
                if saturday_count == 1:  # 테스트용 첫 번째 토요일
                    try:
                        target_a = cells[2].find_element(By.TAG_NAME, "a")
                        print("[INFO] clicking first <a> (Saturday badminton) - TEST")
                        target_a.click()
                        break
                    except Exception as e:
                        print("[ERROR] 첫 번째 <a> 클릭 실패:", e)
                        return

        # 배포 시에는 두 번째 토요일을 선택해야 함
        if not target_a:
            raise Exception("No Saturday badminton slot found.")
        
        time.sleep(2)

        print("[SUCCESS] STEP 2 complete - First Saturday badminton selected! (TEST)")

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    automate_task()
