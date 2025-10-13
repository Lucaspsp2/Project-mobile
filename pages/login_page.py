# pages/login_page.py
from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage
from .checkout_page import CheckoutPage

class LoginPage(BasePage):

    class Locators:
        TITLE_LOGIN = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/loginTV")
        FIELD_USERNAME = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/nameET")
        FIELD_PASSWORD = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/passwordET")
        BTN_LOGIN = (AppiumBy.ACCESSIBILITY_ID, "Tap to login with given credentials")
        ERROR_USERNAME = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/nameErrorTV")
        ERROR_PASSWORD = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/passwordErrorTV")
        USER_LIST_TV = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/username1TV")
        PASS_LIST_TV = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/password1TV")

    def __init__(self, driver):
        super().__init__(driver)

    def is_login_page_loaded(self):
        return self.is_element_displayed(*self.Locators.TITLE_LOGIN)

    def enter_username(self, username):
        self.send_keys_to_element(*self.Locators.FIELD_USERNAME, username)
        return self

    def enter_password(self, password):
        self.send_keys_to_element(*self.Locators.FIELD_PASSWORD, password)
        return self

    def click_login(self):
        self.click_element(*self.Locators.BTN_LOGIN)
        return self

    def login(self, username=None, password=None):
        if username is not None:
            self.enter_username(username)
        if password is not None:
            self.enter_password(password)
        self.click_login()
        return CheckoutPage(self.driver)

    def get_test_credentials(self):
        username = self.get_element_text(*self.Locators.USER_LIST_TV)
        password = self.get_element_text(*self.Locators.PASS_LIST_TV)
        return username, password

    def is_error_username_displayed(self):
        return self.is_element_displayed(*self.Locators.ERROR_USERNAME)

    def is_error_password_displayed(self):
        return self.is_element_displayed(*self.Locators.ERROR_PASSWORD)
