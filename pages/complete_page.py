from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
import time

class CompletePage(BasePage):
    # --- LOCALIZADORES ---
    TITLE_COMPLETE = AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/completeTV"
    BTN_BACK_TO_PRODUCTS = AppiumBy.ACCESSIBILITY_ID, "Continue Shopping button"

    def __init__(self, driver):
        super().__init__(driver)

    def is_order_complete(self):
        """Verifica se a mensagem de conclusão do pedido está visível."""
        return self.is_element_displayed(*self.TITLE_COMPLETE)

    def click_continue_shopping(self):
        """Clica no botão para voltar para a Home."""
        self.click_element(*self.BTN_BACK_TO_PRODUCTS)
        time.sleep(2)