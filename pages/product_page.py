# pages/product_page.py
from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage
from .cart_page import CartPage

class ProductPage(BasePage):

    class Locators:
        BTN_DECREASE = (AppiumBy.ACCESSIBILITY_ID, "Decrease item quantity")
        BTN_INCREASE = (AppiumBy.ACCESSIBILITY_ID, "Increase item quantity")
        BTN_ADD_TO_CART = (AppiumBy.ACCESSIBILITY_ID, "Tap to add product to cart")
        CART_BADGE_TV = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cartTV")
        ICON_CART = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cartIV")

    def __init__(self, driver):
        super().__init__(driver)

    def decrease_quantity(self):
        self.click_element(*self.Locators.BTN_DECREASE)
        return self

    def increase_quantity(self):
        self.click_element(*self.Locators.BTN_INCREASE)
        return self

    def is_add_to_cart_enabled(self):
        return self.get_attribute(*self.Locators.BTN_ADD_TO_CART, "enabled") == "true"

    def add_product_to_cart(self):
        self.click_element(*self.Locators.BTN_ADD_TO_CART)
        return self

    def get_cart_badge_count(self):
        return self.get_element_text(*self.Locators.CART_BADGE_TV)

    def click_cart_icon(self):
        self.click_element(*self.Locators.ICON_CART)
        return CartPage(self.driver)
