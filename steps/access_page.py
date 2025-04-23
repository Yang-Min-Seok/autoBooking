# Access to target URL
async def access_target_page(page, gym):
    
    if gym == "HIGASHI":
        gym_no = 413
    
    elif gym == "KAMEDA":
        gym_no = 429

    else:
        print("[ERROR] Invalid GYM.")

    url = f"https://niigata-kaikou.jp/facility/{gym_no}/schedule#facility-page-main"

    print(f"[INFO] {url} ...")

    await page.goto(url)