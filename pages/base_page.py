from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from appium.webdriver.common.appiumby import AppiumBy
import time

class BasePage:
    DEFAULT_TIMEOUT = 15

    def __init__(self, driver, timeout: int = None):
        self.driver = driver
        self.timeout = timeout or self.DEFAULT_TIMEOUT
        self.wait = WebDriverWait(driver, self.timeout)

    # --- Wait helpers ---
    def wait_for_visibility_of_element(self, by, locator, timeout=None):
        return WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.visibility_of_element_located((by, locator))
        )

    def wait_for_presence_of_element(self, by, locator, timeout=None):
        return WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.presence_of_element_located((by, locator))
        )

    def wait_for_element_to_be_clickable(self, by, locator, timeout=None):
        return WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.element_to_be_clickable((by, locator))
        )

    # --- Basic actions ---
    def find_element(self, by, locator):
        try:
            return self.wait_for_presence_of_element(by, locator)
        except TimeoutException:
            raise TimeoutException(f"Elemento não encontrado: {locator}")

    def click_element(self, by, locator):
        el = self.wait_for_element_to_be_clickable(by, locator)
        el.click()
        return el

    def send_keys_to_element(self, by, locator, text):
        el = self.wait_for_visibility_of_element(by, locator)
        el.clear()
        el.send_keys(text)
        return el

    def get_element_text(self, by, locator):
        el = self.wait_for_visibility_of_element(by, locator)
        return el.text

    def is_element_displayed(self, by, locator):
        try:
            el = self.wait_for_visibility_of_element(by, locator)
            return el.is_displayed()
        except TimeoutException:
            return False

    def get_attribute(self, by, locator, attribute):
        el = self.find_element(by, locator)
        return el.get_attribute(attribute)

    # --- Scroll helper ---
    def scroll_to_element(self, by, locator, max_scrolls=5):
        """
        Rola até que o elemento fique visível. Usa tentativa com 'mobile: scroll'.
        Retorna o elemento quando visível.
        """
        for _ in range(max_scrolls):
            try:
                return self.wait_for_visibility_of_element(by, locator, timeout=2)
            except TimeoutException:
                try:
                    # Appium command to scroll; fallback to swipe/execute_script if needed
                    self.driver.execute_script("mobile: scroll", {"direction": "down"})
                except Exception:
                    # última tentativa: usar back/press -- mas preferimos não falhar silenciosamente
                    pass
        raise TimeoutException(f"Elemento não encontrado após {max_scrolls} scrolls: {locator}")

    # --- Notifications & Popups (system-level) ---
    def open_notifications(self):
        try:
            self.driver.open_notifications()
        except Exception:
            # alguns drivers/devices não suportam; ignore se falhar
            pass

    def is_notification_displayed(self, expected_title):
        try:
            self.open_notifications()
            locator = (AppiumBy.XPATH, f"//*[@resource-id='android:id/title' and @text='{expected_title}']")
            self.wait_for_visibility_of_element(*locator)
            return True
        except TimeoutException:
            return False
        finally:
            try:
                self.driver.back()
            except Exception:
                pass

    # --- Handle simple native alert popups ---
    def accept_alert(self):
        try:
            # botão OK padrão
            self.click_element(AppiumBy.ID, "android:id/button1")
        except Exception:
            pass

    def dismiss_alert(self):
        try:
            self.click_element(AppiumBy.ID, "android:id/button2")
        except Exception:
            pass
