# pages/checkout_page.py
from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage
from .payment_page import PaymentPage

class CheckoutPage(BasePage):

    class Locators:
        TITLE_CHECKOUT = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/checkoutTitleTV")
        FIELD_FULL_NAME = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/fullNameET")
        FIELD_ADDRESS_1 = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/address1ET")
        FIELD_ADDRESS_2 = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/address2ET")
        FIELD_CITY = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cityET")
        FIELD_STATE = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/stateET")
        FIELD_ZIP = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/zipET")
        FIELD_COUNTRY = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/countryET")
        BTN_TO_PAYMENT = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/paymentBtn")

    def __init__(self, driver):
        super().__init__(driver)

    def is_checkout_page_loaded(self):
        return self.is_element_displayed(*self.Locators.TITLE_CHECKOUT)

    def fill_shipping_address(self, user_data):
        self.send_keys_to_element(*self.Locators.FIELD_FULL_NAME, user_data["USERNAME"])
        self.send_keys_to_element(*self.Locators.FIELD_ADDRESS_1, user_data["ENDERECO_1"])
        self.send_keys_to_element(*self.Locators.FIELD_ADDRESS_2, user_data["ENDERECO_2"])
        self.send_keys_to_element(*self.Locators.FIELD_CITY, user_data["CIDADE"])
        self.send_keys_to_element(*self.Locators.FIELD_STATE, user_data["ESTADO"])
        self.send_keys_to_element(*self.Locators.FIELD_ZIP, user_data["ZIP_CODE"])
        self.send_keys_to_element(*self.Locators.FIELD_COUNTRY, user_data["PAIS"])
        return self

    def click_to_payment(self):
        self.click_element(*self.Locators.BTN_TO_PAYMENT)
        return PaymentPage(self.driver)
