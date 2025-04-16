async def fill_reservation_form(page, name, phone, email):
    print("[INFO] Filling out form...")
    await page.wait_for_selector("table.c-form01")

    name_input = page.locator("input[name='name']")
    phone_input = page.locator("input[type='tel']")
    email_input = page.locator("input[type='email']")

    await name_input.fill(name)
    print("[INFO] name filled with:", await name_input.input_value())

    await phone_input.fill(phone)
    print("[INFO] phone filled with:", await phone_input.input_value())

    await email_input.fill(email)
    print("[INFO] email filled with:", await email_input.input_value())

    await page.click(".c-form-btn button[name='mode']")
    print("[INFO] Clicked confirm button")