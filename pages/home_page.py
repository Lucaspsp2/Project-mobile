# pages/home_page.py
from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage
from .product_page import ProductPage

class HomePage(BasePage):

    class Locators:
        PRODUCT_TITLE_XPATH = (AppiumBy.XPATH, '//android.widget.TextView[@content-desc="Product Title" and @text="Sauce Labs Backpack (orange)"]')
        BACKPACK_IV_UIAUTOMATOR = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/productIV").instance(2)')
        # popup locators (system)
        POPUP_TITLE = (AppiumBy.ID, "android:id/alertTitle")
        POPUP_MESSAGE = (AppiumBy.ID, "android:id/message")
        OK_BUTTON = (AppiumBy.ID, "android:id/button1")
        CANCEL_BUTTON = (AppiumBy.ID, "android:id/button2")

    def __init__(self, driver):
        super().__init__(driver)

    def is_home_page_loaded(self):
        return self.is_element_displayed(*self.Locators.PRODUCT_TITLE_XPATH)

    def select_backpack(self):
        # retorna ProductPage (fluent)
        self.click_element(*self.Locators.BACKPACK_IV_UIAUTOMATOR)
        return ProductPage(self.driver)

    # popup helpers using base methods
    def accept_popup(self):
        self.click_element(*self.Locators.OK_BUTTON)

    def dismiss_popup(self):
        self.click_element(*self.Locators.CANCEL_BUTTON)
