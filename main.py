# main.py
import time
from dotenv import load_dotenv
import os

from utils import get_driver
from step1_access_url import access_reservation_page
from step2_select_date import select_target_date
from step3_select_time import select_court_time
from step4_input_form import fill_reservation_form
from step5_confirm import click_final_confirm
from step6_wait import final_wait

# Load .env
load_dotenv("info.env")
URL = os.getenv("TARGET_URL")

def log_step_time(step_name, start_time):
    elapsed = time.time() - start_time
    print(f"[TIME] {step_name} complete ⏱ {elapsed:.2f}sec")
    return elapsed

def automate_task():
    print(f"[INFO] auto booking start → {URL}")
    driver = get_driver()
    total_start = time.time()

    try:
        t1 = time.time()
        access_reservation_page(driver, URL)
        log_step_time("STEP 1", t1)

        t2 = time.time()
        select_target_date(driver)
        log_step_time("STEP 2", t2)

        t3 = time.time()
        select_court_time(driver)
        log_step_time("STEP 3", t3)

        t4 = time.time()
        fill_reservation_form(driver)
        log_step_time("STEP 4", t4)

        t5 = time.time()
        click_final_confirm(driver)
        log_step_time("STEP 5", t5)

        total_elapsed = time.time() - total_start
        print(f"[TIME] total complete ⏱ {total_elapsed:.2f}sec")

        final_wait()

    except Exception as e:
        print(f"[ERROR] Booking failed: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    automate_task()