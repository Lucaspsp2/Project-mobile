# pages/cart_page.py
from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage
from .login_page import LoginPage

class CartPage(BasePage):

    class Locators:
        ICON_CART = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cartIV")
        PRICE_TV = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/priceTV")
        QUANTITY_TV = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/noTV")
        TOTAL_PRICE_TV = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/totalPriceTV")
        BTN_CHECKOUT = (AppiumBy.ACCESSIBILITY_ID, "Confirms products for checkout")

    def __init__(self, driver):
        super().__init__(driver)

    def go_to_cart(self):
        self.click_element(*self.Locators.ICON_CART)
        return self

    def get_unit_price(self):
        price_str = self.get_element_text(*self.Locators.PRICE_TV).strip().replace("$", "").replace(" ", "")
        return float(price_str)

    def get_quantity(self):
        return int(self.get_element_text(*self.Locators.QUANTITY_TV).strip())

    def get_subtotal_from_screen(self):
        return self.get_element_text(*self.Locators.TOTAL_PRICE_TV).strip().replace(" ", "")

    def click_checkout(self):
        self.click_element(*self.Locators.BTN_CHECKOUT)
        return LoginPage(self.driver)
