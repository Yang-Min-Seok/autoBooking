async def select_time_slot(page):
    print("[INFO] Selecting 9-11 badminton court...")
    await page.wait_for_selector("table.c-table01")
    second_row = page.locator("table.c-table01 tbody tr").nth(2)
    time_cell = second_row.locator("td").nth(1)
    await time_cell.locator("a").click()