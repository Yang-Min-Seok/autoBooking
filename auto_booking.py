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

async def main():
    start_time = time.perf_counter()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(locale="ja-JP")
        page = await context.new_page()

        await access_target_page(page, TARGET_URL)

        target_date = datetime.today() + timedelta(days=7)
        target_day_str = f"{target_date.day}日"
        selected = await select_target_date(page, target_day_str)
        if not selected:
            await browser.close()
            return

        await select_time_slot(page)
        await fill_reservation_form(page, NAME, PHONE_NUMBER, E_MAIL)
        await confirm_reservation(page)

        end_time = time.perf_counter()
        print(f"[TIME] Total execution time ⏱ {end_time - start_time:.2f} sec")
        
        print("[INFO] Wait for safty exit(3 sec)")
        await page.wait_for_timeout(3000)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
