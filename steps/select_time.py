# Select time

# Set Variables

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

    rows = page.locator("table.c-table01 tbody tr")
    row_count = await rows.count()

    target_row_index = -1
    for i in range(row_count):
        first_cell = rows.nth(i).locator("td").first
        row_text = await first_cell.inner_text()
        if court_no in row_text:
            target_row_index = i
            break

    if target_row_index == -1:
        raise Exception(f"[ERROR] Court '{court_no}' not found in table rows.")

    target_row = rows.nth(target_row_index)
    target_time = target_row.locator("td").nth(time_dict[time])

    await target_time.locator("a").click(timeout=5000)