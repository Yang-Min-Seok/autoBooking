# utils.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option('prefs', {
        'intl.accept_languages': 'ja',
        'profile.managed_default_content_settings.images': 2
    })
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)