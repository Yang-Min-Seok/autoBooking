# auto_booking_playwright.py
import asyncio
import os
import time
from dotenv import load_dotenv
from datetime import datetime, timedelta
from playwright.async_api import async_playwright
from steps.access_page import access_target_page
from steps.select_date import select_target_date
from steps.select_time import select_time_slot
from steps.fill_form import fill_reservation_form
from steps.confirm_final import confirm_reservation

# Load environment variables
load_dotenv("info.env")
TARGET_URL = os.getenv("TARGET_URL")
NAME = os.getenv("NAME")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
E_MAIL = os.getenv("E_MAIL")
COURT_NO = os.getenv("COURT_NO")
TIME = os.getenv("TIME")

# Set variables
day_after = 7
waiting_sec = 3000

async def main():
    start_time = time.perf_counter()

    async with async_playwright() as p:

        # Set playwright options
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(locale="ja-JP")
        page = await context.new_page()

        # STEP1 : Access to target URL
        await access_target_page(page, TARGET_URL)

        # Calc target date
        target_date = datetime.today() + timedelta(days=day_after)
        target_day_str = f"{target_date.day}日"

        # STEP2 : Select date
        selected = await select_target_date(page, target_day_str)
        if not selected:
            await browser.close()
            return

        # STEP3 : Select time
        await select_time_slot(page, COURT_NO, TIME)

        # STEP4 : Fill up form
        await fill_reservation_form(page, NAME, PHONE_NUMBER, E_MAIL)

        # STEP5 : Confirm reservation
        await confirm_reservation(page)

        # For performance test
        end_time = time.perf_counter()
        print(f"[TIME] Total execution time ⏱ {end_time - start_time:.2f} sec")
        
        # For safety exit
        print("[INFO] Wait for safty exit(3 sec)")
        await page.wait_for_timeout(waiting_sec)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
