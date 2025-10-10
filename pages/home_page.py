from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage
import time

class HomePage(BasePage):

    # --- LOCALIZADORES —

    PRODUCT_TITLE_XPATH = '//android.widget.TextView[@content-desc="Product Title" and @text="Sauce Labs Backpack (orange)"]'
    BACKPACK_IV_UIAUTOMATOR = 'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/productIV").instance(2)'
    
    def __init__(self, driver):
        super().__init__(driver)

    def is_home_page_loaded(self):
        """Verifica se a tela inicial carregou."""
        return self.is_element_displayed(AppiumBy.XPATH, self.PRODUCT_TITLE_XPATH)

    def select_backpack(self):
        """Clica na imagem da mochila para ir para a página de detalhes."""
        self.click_element(AppiumBy.ANDROID_UIAUTOMATOR, self.BACKPACK_IV_UIAUTOMATOR)
        time.sleep(2)