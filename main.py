# main.py
from dotenv import load_dotenv
import os

from utils import get_driver
from step1_access_url import access_reservation_page
from step2_select_date import select_target_date
from step3_select_time import select_court_time
from step4_input_form import fill_reservation_form
from step5_confirm import click_final_confirm

# Load .env
load_dotenv("info.env")
URL = os.getenv("TARGET_URL")

def automate_task():
    print(f"[INFO] auto booking start → {URL}")
    driver = get_driver()

    try:
        access_reservation_page(driver, URL)
        select_target_date(driver)
        select_court_time(driver)
        fill_reservation_form(driver)
        click_final_confirm(driver)

    except Exception as e:
        print(f"[ERROR] Booking failed: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    automate_task()