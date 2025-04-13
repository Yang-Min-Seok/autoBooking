# step5_confirm.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def click_final_confirm(driver):
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "c-form-btn"))
    )
    button_container = driver.find_element(By.CLASS_NAME, "c-form-btn")
    first_button = button_container.find_elements(By.TAG_NAME, "button")[0]
    first_button.click()

    print("[SUCCESS] STEP 5: Final confirmation button click success")