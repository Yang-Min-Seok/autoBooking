from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
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
    options.add_argument("--headless")
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

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    automate_task()
