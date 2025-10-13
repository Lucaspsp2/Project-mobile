# pages/payment_page.py
from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage
from .review_page import ReviewPage

class PaymentPage(BasePage):

    class Locators:
        TITLE_PAYMENT = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/enterPaymentTitleTV")
        FIELD_NAME = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/nameET")
        FIELD_CARD_NUMBER = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cardNumberET")
        FIELD_EXPIRATION_DATE = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/expirationDateET")
        FIELD_SECURITY_CODE = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/securityCodeET")
        BTN_REVIEW_ORDER = (AppiumBy.ACCESSIBILITY_ID, "Saves payment info and launches screen to review checkout data")
        ERROR_CARD_NUMBER = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cardNumberErrorIV")
        ERROR_EXPIRATION = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/expirationDateIV")
        ERROR_SECURITY_CODE = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/securityCodeIV")
        ERROR_FULL_NAME = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/nameErrorTV")

    def __init__(self, driver):
        super().__init__(driver)

    def is_payment_page_loaded(self):
        return self.is_element_displayed(*self.Locators.TITLE_PAYMENT)

    def fill_payment_fields(self, card_data):
        self.send_keys_to_element(*self.Locators.FIELD_NAME, card_data["USERNAME"])
        self.send_keys_to_element(*self.Locators.FIELD_CARD_NUMBER, card_data["CARTAO"])
        self.send_keys_to_element(*self.Locators.FIELD_EXPIRATION_DATE, card_data["DATA_CARTAO"])
        self.send_keys_to_element(*self.Locators.FIELD_SECURITY_CODE, card_data["CODIGO_CARTAO"])
        return self

    def click_review_order(self):
        self.click_element(*self.Locators.BTN_REVIEW_ORDER)
        return ReviewPage(self.driver)

    def is_error_displayed(self, error_locator):
        # recebe um locator tuple, ex: PaymentPage.Locators.ERROR_FULL_NAME
        return self.is_element_displayed(*error_locator)
