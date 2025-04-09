# step4_input_form.py
import os
from selenium.webdriver.common.by import By

def fill_reservation_form(driver):
    form_table = driver.find_element(By.CSS_SELECTOR, "table.c-form01")

    name_input = form_table.find_element(By.CSS_SELECTOR, 'input[type="text"]')
    name_input.clear()
    name_input.send_keys(os.getenv("NAME"))

    phone_input = form_table.find_element(By.CSS_SELECTOR, 'input[type="tel"]')
    phone_input.clear()
    phone_input.send_keys(os.getenv("PHONE_NUMBER"))

    email_input = form_table.find_element(By.CSS_SELECTOR, 'input[type="email"]')
    email_input.clear()
    email_input.send_keys(os.getenv("E_MAIL"))

    print("[SUCCESS] STEP 4: Name, Phone Number, Email input success")

    button_container = driver.find_element(By.CLASS_NAME, "c-form-btn")
    confirm_button = button_container.find_element(By.NAME, "mode")
    confirm_button.click()

    print("[SUCCESS] STEP 4: Send button click success")