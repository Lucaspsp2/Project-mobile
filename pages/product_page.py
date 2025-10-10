from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
import time

class ProductPage(BasePage):
    # --- LOCALIZADORES ---
    BTN_DECREASE = AppiumBy.ACCESSIBILITY_ID, "Decrease item quantity"
    BTN_INCREASE = AppiumBy.ACCESSIBILITY_ID, "Increase item quantity"
    BTN_ADD_TO_CART = AppiumBy.ACCESSIBILITY_ID, "Tap to add product to cart"
    CART_BADGE_TV = AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cartTV"
    
    def __init__(self, driver):
        super().__init__(driver)

    def decrease_quantity(self):
        self.click_element(*self.BTN_DECREASE)
        time.sleep(0.5)

    def increase_quantity(self):
        self.click_element(*self.BTN_INCREASE)
        time.sleep(0.5)

    def is_add_to_cart_enabled(self):
        return self.find_element(*self.BTN_ADD_TO_CART).get_attribute("enabled") == "true"
        
    def add_product_to_cart(self):
        self.click_element(*self.BTN_ADD_TO_CART)
        time.sleep(1)

    def get_cart_badge_count(self):
        return self.get_element_text(*self.CART_BADGE_TV)