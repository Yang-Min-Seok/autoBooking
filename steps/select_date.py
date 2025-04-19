# Select date

# Set variables
date_pos                   = 0
badmintod_reserve_btn_pos  = 2

async def select_target_date(page, target_day_str):
    
    print(f"[INFO] Looking for day: {target_day_str}")
    rows = await page.locator("table.c-table01 tbody tr").all()
    
    for row in rows:
        day_cell = await row.locator("td").nth(date_pos).inner_text()
        if target_day_str in day_cell:
            print(f"[INFO] Found matching row: {day_cell.strip()}")
            reserve_button = row.locator("td").nth(badmintod_reserve_btn_pos).locator("a:has-text('予約')")
            if await reserve_button.count() > 0:
                await reserve_button.click()
                return True
            else:
                print("[WARN] No '予約' button found in this row.(Date was found but booking unavaliable)")
                return False
            
    print("[WARN] Failed to detect target date.")
    return False