import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


@pytest.fixture(scope="function")
def driver():
    options = webdriver.ChromeOptions()

    # ✅ Fix 1: Keep browser open after test finishes
    options.add_experimental_option("detach", True)

    # ✅ Fix 2: Disable the "Change your password" data breach popup
    options.add_argument("--disable-save-password-bubble")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-features=PasswordLeakDetection")
    options.add_argument("--disable-features=SafeBrowsingEnhancedProtection")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("prefs", {
        # Disable password manager completely
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        # Disable password leak detection (the data breach warning)
        "profile.password_manager_leak_detection": False,
        # Disable all notifications
        "profile.default_content_setting_values.notifications": 2,
        # Disable safe browsing warnings
        "safebrowsing.enabled": False,
        "safebrowsing.disable_download_protection": True
    })

    service = Service("chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    driver.implicitly_wait(10)

    yield driver

    driver.quit()