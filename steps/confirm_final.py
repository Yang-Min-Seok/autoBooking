async def confirm_reservation(page):
    await page.wait_for_selector(".c-form-btn button")
    final_button = page.locator(".c-form-btn button").first
    await final_button.click()
    print("[SUCCESS] Final reservation button clicked")