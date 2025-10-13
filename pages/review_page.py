# pages/review_page.py
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage
from .complete_page import CompletePage
import re
import time

class ReviewPage(BasePage):

    class Locators:
        TITLE_REVIEW = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/titleTV")
        SHIPPING_TV = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/countryTV")  # frete
        TOTAL_TV = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/totalAmountTV")
        BTN_PLACE_ORDER = (AppiumBy.ACCESSIBILITY_ID, "Place order button")

    def __init__(self, driver):
        super().__init__(driver)

    def is_review_page_loaded(self):
        return self.is_element_displayed(*self.Locators.TITLE_REVIEW)

    def swipe_up(self, times=1, duration=800):
        """Faz swipe para cima na tela, 'times' vezes."""
        size = self.driver.get_window_size()
        start_y = size['height'] * 0.8
        end_y = size['height'] * 0.2
        x = size['width'] / 2

        for _ in range(times):
            self.driver.swipe(x, start_y, x, end_y, duration)
            time.sleep(0.5)  # pequena pausa para animação

    def scroll_to_element(self, locator, max_swipes=5):
        """Tenta scrollar até o elemento estar visível."""
        for _ in range(max_swipes):
            try:
                el = WebDriverWait(self.driver, 2).until(
                    EC.visibility_of_element_located(locator)
                )
                return el
            except TimeoutException:
                self.swipe_up()
        # última tentativa sem exceção
        return WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(locator)
        )

    def get_shipping_cost(self):
        """Retorna o frete em float, ignorando texto não numérico."""
        el = self.scroll_to_element(self.Locators.SHIPPING_TV)
        price_text = el.text.strip()
        match = re.search(r"[\d,.]+", price_text)
        if not match:
            raise ValueError(f"Não foi possível extrair valor do frete: '{price_text}'")
        price_str = match.group().replace(",", ".")
        return float(price_str)

    def get_total_on_screen(self):
        """Retorna o total em float."""
        el = self.scroll_to_element(self.Locators.TOTAL_TV)
        total_text = el.text.strip()
        match = re.search(r"[\d,.]+", total_text)
        if not match:
            raise ValueError(f"Não foi possível extrair valor total: '{total_text}'")
        total_str = match.group().replace(",", ".")
        return float(total_str)

    def click_place_order(self):
        self.click_element(*self.Locators.BTN_PLACE_ORDER)
        return CompletePage(self.driver)
