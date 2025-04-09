from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import time
import os
from dotenv import load_dotenv

# load info.env
load_dotenv(dotenv_path="info.env")
TARGET_URL = os.getenv("TARGET_URL")

def automate_task():
    print(f"[INFO] auto booking start → {TARGET_URL}")

    # set option
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option('prefs', {
        'intl.accept_languages': 'ja',
        'profile.managed_default_content_settings.images': 2  # 이미지 비활성화
    })

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # STEP 1: access to target url
        driver.get(TARGET_URL)
        print("[INFO] access success")

        # STEP 2-1: get target day (today += 7)
        target_date = datetime.today() + timedelta(days=7)
        target_day_str = f"{target_date.day}日"
        print(f"[INFO] target day: {target_day_str}")

        # STEP 2-2: search table
        rows = driver.find_elements(By.CSS_SELECTOR, "table.c-table01 tbody tr")

        found = False
        for row in rows:
            tds = row.find_elements(By.TAG_NAME, "td")
            if not tds:
                continue

            day_cell = tds[0]
            if target_day_str in day_cell.text:
                print(f"[INFO] target day detected : {day_cell.text.strip()}")
                try:
                    # find badminton reservation tag (tds[2] = badminton)
                    a_tag = tds[2].find_element(By.XPATH, ".//a[contains(text(),'予約')]")
                    a_tag.click()
                    print("[SUCCESS] STEP 2: 予約 click success")
                    found = True
                    break
                except Exception as e:
                    print(f"[ERROR] STEP 2 fail: {e}")
                    break

        if not found:
            print("[WARN] couldn't find badminton court on target day (full of booking)")

        # STEP 3: click badminton 2 (9-11)
        try:
            # table.c-table01 > tbody > tr[1] (second table row) > td[1] (second table data)
            table = driver.find_element(By.CSS_SELECTOR, "table.c-table01")
            tbody = table.find_element(By.TAG_NAME, "tbody")
            rows = tbody.find_elements(By.TAG_NAME, "tr")

            if len(rows) < 2:
                raise Exception("table row under 2 or same")

            second_row = rows[1]
            tds = second_row.find_elements(By.TAG_NAME, "td")

            if len(tds) < 2:
                raise Exception("table data under 2 or same")

            # click badminton 2 (9 - 11)
            reserve_btn = tds[1].find_element(By.TAG_NAME, "a")
            reserve_btn.click()

            print("[SUCCESS] STEP 3: バドミントン2 9-11 予約 click success")

        except Exception as e:
            print(f"[ERROR] STEP 3 fail: {e}")

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    automate_task()
