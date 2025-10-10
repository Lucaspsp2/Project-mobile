from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
import time

class PaymentPage(BasePage):
    # --- LOCALIZADORES DE PAGAMENTO ---
    TITLE_PAYMENT = AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/enterPaymentTitleTV"
    FIELD_NAME = AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/nameET"
    FIELD_CARD_NUMBER = AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cardNumberET"
    FIELD_EXPIRATION_DATE = AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/expirationDateET"
    FIELD_SECURITY_CODE = AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/securityCodeET"
    BTN_REVIEW_ORDER = AppiumBy.ACCESSIBILITY_ID, "Saves payment info and launches screen to review checkout data"

    # Mensagens de Erro
    ERROR_CARD_NUMBER = AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cardNumberErrorIV"
    ERROR_EXPIRATION = AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/expirationDateIV"
    ERROR_SECURITY_CODE = AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/securityCodeIV"
    ERROR_FULL_NAME = AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/nameErrorTV"

    def __init__(self, driver):
        super().__init__(driver)

    def is_payment_page_loaded(self):
        """Verifica se o título da tela de Pagamento está visível."""
        return self.is_element_displayed(*self.TITLE_PAYMENT)

    def fill_payment_fields(self, card_data):
        """Preenche os campos de pagamento com os dados do cartão."""
        # Se for necessário rolar, o driver está em self.driver
        # Ex: self.driver.execute_script('mobile: scrollGesture', {'direction': 'down'})

        self.send_keys_to_element(*self.FIELD_NAME, card_data["USERNAME"])
        self.send_keys_to_element(*self.FIELD_CARD_NUMBER, card_data["CARTAO"])
        self.send_keys_to_element(*self.FIELD_EXPIRATION_DATE, card_data["DATA_CARTAO"])
        self.send_keys_to_element(*self.FIELD_SECURITY_CODE, card_data["CODIGO_CARTAO"])
        
    def click_review_order(self):
        """Clica no botão para Revisar o Pedido."""
        self.click_element(*self.BTN_REVIEW_ORDER)
        time.sleep(2)

    # Métodos de Validação de Erro
    def is_error_displayed(self, error_locator):
        """Método genérico para checar se uma mensagem de erro está visível."""
        return self.is_element_displayed(AppiumBy.ID, error_locator[1]) # Passa apenas o ID