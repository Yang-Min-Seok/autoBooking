from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os
import time

# load info.env
load_dotenv(dotenv_path='info.env')

# get URL
TARGET_URL = os.getenv("TARGET_URL")

def test_browser():
    print(f"[TEST] browser test start! target URL : {TARGET_URL}")

    # Set chrome option (show window)
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")

    # execute browser
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(TARGET_URL)
        print("[TEST] access success! quit after 3 sec")
        time.sleep(3)
    except Exception as e:
        print("[TEST] error:", e)
    finally:
        driver.quit()
        print("[TEST] browser test has been done successfully")

if __name__ == "__main__":
    test_browser()