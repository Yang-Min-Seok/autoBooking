# step3_select_time.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def select_court_time(driver):
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "table.c-table01"))
    )
    table = driver.find_element(By.CSS_SELECTOR, "table.c-table01")
    tbody = table.find_element(By.TAG_NAME, "tbody")
    rows = tbody.find_elements(By.TAG_NAME, "tr")

    if len(rows) < 2:
        raise Exception("table row under 2 or same")

    second_row = rows[1]
    tds = second_row.find_elements(By.TAG_NAME, "td")

    if len(tds) < 2:
        raise Exception("table data under 2 or same")

    reserve_btn = tds[1].find_element(By.TAG_NAME, "a")
    reserve_btn.click()
    print("[SUCCESS] STEP 3: バドミントン2 9-11 予約 click success")