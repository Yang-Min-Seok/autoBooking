# step1_access_url.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def access_reservation_page(driver, url):
    driver.get(url)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "table.c-table01"))
    )
    print("[INFO] STEP 1: Access success")