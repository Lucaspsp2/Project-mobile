# pages/complete_page.py
from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage

class CompletePage(BasePage):

    class Locators:
        TITLE_COMPLETE = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/completeTV")
        BTN_BACK_TO_PRODUCTS = (AppiumBy.ACCESSIBILITY_ID, "Continue Shopping button")

    def __init__(self, driver):
        super().__init__(driver)

    def is_order_complete(self):
        return self.is_element_displayed(*self.Locators.TITLE_COMPLETE)

    def click_continue_shopping(self):
        self.click_element(*self.Locators.BTN_BACK_TO_PRODUCTS)
        # Import aqui dentro do método para evitar circular import
        from .home_page import HomePage
        return HomePage(self.driver)

