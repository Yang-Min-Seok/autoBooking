# step2_select_date.py
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def select_target_date(driver):
    target_date = datetime.today() + timedelta(days=7)
    target_day_str = f"{target_date.day}日"
    print(f"[INFO] target day: {target_day_str}")

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "table.c-table01 tbody tr"))
    )
    rows = driver.find_elements(By.CSS_SELECTOR, "table.c-table01 tbody tr")
    found = False

    for row in rows:
        tds = row.find_elements(By.TAG_NAME, "td")
        if not tds:
            continue

        day_cell = tds[0]
        if target_day_str in day_cell.text:
            print(f"[INFO] target day detected : {day_cell.text.strip()}")
            a_tag = tds[2].find_element(By.XPATH, ".//a[contains(text(),'予約')]")
            a_tag.click()
            print("[SUCCESS] STEP 2: 予約 click success")
            found = True
            break

    if not found:
        print("[WARN] couldn't find badminton court on target day (full of booking)")