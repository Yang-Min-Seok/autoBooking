# auto_booking.py
import asyncio
import os
import time
import argparse
from dotenv import load_dotenv
from datetime import datetime, timedelta
from playwright.async_api import async_playwright
from steps.access_page import access_target_page
from steps.select_date import select_target_date
from steps.select_time import select_time_slot
from steps.fill_form import fill_reservation_form
from steps.confirm_final import confirm_reservation

# Argument Parsing
parser = argparse.ArgumentParser(description="Automated Gym Court Reservation")
parser.add_argument("--env", required=True, help="Path to the .env file")
parser.add_argument("--court", required=True, help="Court number to reserve")
parser.add_argument("--time", required=True, help="Time slot to reserve")
args = parser.parse_args()

# Load environment variables from specified file
if not os.path.exists(args.env):
    print(f"[ERROR] .env file not found: {args.env}")
    exit(1)

load_dotenv(args.env)

# Extract variables
NAME = os.getenv("NAME")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
E_MAIL = os.getenv("E_MAIL")
GYM = os.getenv("GYM")

# Set constants
day_after               = 6
waiting_sec             = 3000

higashi_max_court_no    = 3
kameda_max_court_no     = 11
toyano_max_court_no     = 6
kita_max_court_no       = 3
nishi_max_court_no      = 6

async def main():
    # Validate court number based on gym
    if GYM == "HIGASHI" and int(args.court) > higashi_max_court_no:
        print(f"[ERROR] Higashi Gym has maximum {higashi_max_court_no} courts.")
        return
    elif GYM == "TOYANO" and int(args.court) > toyano_max_court_no:
        print(f"[ERROR] Toyano Gym has maximum {toyano_max_court_no} courts.")
        return
    elif GYM == "KAMEDA" and int(args.court) > kameda_max_court_no:
        print(f"[ERROR] Kameda Gym has maximum {kameda_max_court_no} courts.")
        return
    elif GYM == "KITA" and int(args.court) > kita_max_court_no:
        print(f"[ERROR] Kameda Gym has maximum {kita_max_court_no} courts.")
        return
    elif GYM == "NISHI" and int(args.court) > nishi_max_court_no:
        print(f"[ERROR] Kameda Gym has maximum {nishi_max_court_no} courts.")
        return

    start_time = time.perf_counter()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(locale="ja-JP")
        page = await context.new_page()

        # Step 1: Access target page
        await access_target_page(page, GYM)

        # Calculate target date
        target_date = datetime.today() + timedelta(days=day_after)
        target_day_str = f"{target_date.day}日"

        # Step 2: Select date
        selected = await select_target_date(page, target_day_str)
        if not selected:
            await browser.close()
            return

        # Step 3: Select time slot
        await select_time_slot(page, args.court, args.time)

        # Step 4: Fill in reservation form
        await fill_reservation_form(page, NAME, PHONE_NUMBER, E_MAIL)

        # Step 5: Confirm reservation
        await confirm_reservation(page)

        end_time = time.perf_counter()
        print(f"[TIME] Total execution time ⏱ {end_time - start_time:.2f} sec")

        print("[INFO] Waiting 3 seconds before exit for safety.")
        await page.wait_for_timeout(waiting_sec)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
