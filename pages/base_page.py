from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from appium.webdriver.common.appiumby import AppiumBy
import time

class BasePage:
    # Tempo limite padrão para a espera explícita
    DEFAULT_TIMEOUT = 15

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.DEFAULT_TIMEOUT)

    def find_element(self, by, locator):
        """Espera a presença do elemento e o retorna."""
        try:
            return self.wait.until(EC.presence_of_element_located((by, locator)))
        except TimeoutException:
            # Você pode personalizar o erro aqui se quiser
            raise TimeoutException(f"Elemento não encontrado: {locator}")

    def click_element(self, by, locator):
        """Espera o elemento ser clicável e clica."""
        element = self.wait.until(EC.element_to_be_clickable((by, locator)))
        element.click()

    def send_keys_to_element(self, by, locator, text):
        """Espera o elemento e envia o texto."""
        element = self.find_element(by, locator)
        element.clear()
        element.send_keys(text)

    def get_element_text(self, by, locator):
        """Retorna o texto de um elemento."""
        return self.find_element(by, locator).text

    def is_element_displayed(self, by, locator):
        """Verifica se um elemento está visível na tela (sem lançar exceção)."""
        try:
            return self.find_element(by, locator).is_displayed()
        except TimeoutException:
            return False

    def get_attribute(self, by, locator, attribute):
        """Retorna o valor de um atributo do elemento."""
        return self.find_element(by, locator).get_attribute(attribute)

    # --- Método de Scroll (Necessário para o Passo 5) ---
    def scroll_to_element(self, by, locator, max_scrolls=5):
        """
        Rola a tela para baixo até que o elemento seja encontrado ou atinja o max_scrolls.
        Retorna o elemento se encontrado.
        """
        for _ in range(max_scrolls):
            try:
                # Tenta encontrar o elemento (usa visibilidade para ser mais preciso)
                element = self.wait.until(EC.visibility_of_element_located((by, locator)))
                return element
            except TimeoutException:
                # Se não encontrou, realiza o scroll
                # Comando Appium para rolar a tela para baixo
                self.driver.execute_script("mobile: scroll", {"direction": "down"})
                time.sleep(1) # Pequena pausa para a animação

        # Lança exceção se não encontrou após todas as tentativas
        raise TimeoutException(f"Elemento não encontrado após {max_scrolls} scrolls: {locator}")