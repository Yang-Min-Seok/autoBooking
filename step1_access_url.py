# step1_access.py
def access_reservation_page(driver, url):
    driver.get(url)
    print("[INFO] STEP 1: Access success")