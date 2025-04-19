# Access to target URL
async def access_target_page(page, url):
    print(f"[INFO] Accessing {url}...")
    await page.goto(url)