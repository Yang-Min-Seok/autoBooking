async def select_target_date(page, target_day_str):
    print(f"[INFO] Looking for day: {target_day_str}")
    rows = await page.locator("table.c-table01 tbody tr").all()
    for row in rows:
        day_cell = await row.locator("td").nth(0).inner_text()
        if target_day_str in day_cell:
            print(f"[INFO] Found matching row: {day_cell.strip()}")
            reserve_button = row.locator("td").nth(2).locator("a:has-text('予約')")
            if await reserve_button.count() > 0:
                await reserve_button.click()
                return True
            else:
                print("[WARN] No '予約' button found in this row.")
    print("[WARN] No reservable court found for target date.")
    return False