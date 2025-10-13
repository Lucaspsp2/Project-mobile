# conftest.py
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

# Configurações de capabilities
capabilities = {
    "android": {
        "platformName": "Android",
        "automationName": "UiAutomator2",
        "deviceName": "Android Emulator",
        "app": "/Users/lpsp/Downloads/mda-2.2.0-25.apk",
        "noReset": True,   # Mantém app instalado/aberto
        "fullReset": False
    },
    "ios": {
        "platformName": "iOS",
        "automationName": "XCUITest",
        "deviceName": "iPhone Simulator",
        "bundleId": "com.saucelabs.mydemoapp.ios"
    }
}

@pytest.fixture(scope="function")
def driver():
    """Inicia e encerra o driver Appium para cada teste."""
    android_caps = capabilities["android"]

    options = UiAutomator2Options()
    options.platform_name = android_caps.get("platformName", "Android")
    options.device_name = android_caps.get("deviceName", "Android Emulator")
    options.app = android_caps.get("app")
    options.automation_name = android_caps.get("automationName", "UiAutomator2")
    options.no_reset = android_caps.get("noReset", True)
    options.full_reset = android_caps.get("fullReset", False)

    # Conexão com Appium 2.x (sem /wd/hub)
    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

    yield driver
    driver.quit()
