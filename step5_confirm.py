# step5_confirm.py
from selenium.webdriver.common.by import By

def click_final_confirm(driver):
    button_wrapper = driver.find_element(By.CLASS_NAME, "c-form-btn")
    send_button = button_wrapper.find_element(By.CSS_SELECTOR, 'button[value="send"]')
    send_button.click()
    print("[SUCCESS] STEP 5: Final confirmation button click success")
