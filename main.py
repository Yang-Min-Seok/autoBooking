from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os
import time

load_dotenv(dotenv_path='info.env')

TARGET_URL = os.getenv("TARGET_URL")
NAME = os.getenv("NAME")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
E_MAIL = os.getenv("E_MAIL")

def automate_task():
    print(f"[INFO] auto booking start → {TARGET_URL}")

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(TARGET_URL)
        print("[INFO] access success")

        # 실제 사이트 구조에 맞게 수정 필요
        driver.find_element(By.XPATH, '//a[text()="첫 번째 링크"]').click()
        driver.find_element(By.XPATH, '//a[text()="두 번째 링크"]').click()

        driver.find_element(By.NAME, "input1").send_keys(NAME)
        driver.find_element(By.NAME, "input2").send_keys(PHONE_NUMBER)
        driver.find_element(By.NAME, "input3").send_keys(E_MAIL)

        driver.find_element(By.XPATH, '//button[text()="버튼1"]').click()
        driver.find_element(By.XPATH, '//button[text()="버튼2"]').click()

        time.sleep(2)
        print("[SUCCESS] booking success!")

    except Exception as e:
        print(f"[ERROR] error : {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    automate_task()
