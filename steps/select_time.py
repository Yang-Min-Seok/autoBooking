# Select time

# Set Variables
court_dict = {
    "1"     : 0,
    "2"     : 1,
    "3"     : 2,
    "4"     : 3,
    "5"     : 4,
    "6"     : 5,
    "7"     : 6,
    "8"     : 7,
    "9"     : 8,
    "10"    : 9,
    "11"    : 10,
}

time_dict = {
    "9-11" : 1,
    "11-13" : 2,
    "13-15" : 3,
    "15-17" : 4,
    "17-19" : 5,
    "19-21" : 6,
}

async def select_time_slot(page, court_no, time):
    print("[INFO] Selecting target badminton court...")
    await page.wait_for_selector("table.c-table01")
    target_row = page.locator("table.c-table01 tbody tr").nth(court_dict[court_no])
    target_time = target_row.locator("td").nth(time_dict[time])
    await target_time.locator("a").click(timeout=5000)