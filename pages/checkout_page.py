from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
import time

class CheckoutPage(BasePage):
    # --- LOCALIZADORES DE ENDEREÇO ---
    TITLE_CHECKOUT = AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/checkoutTitleTV"
    FIELD_FULL_NAME = AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/fullNameET"
    FIELD_ADDRESS_1 = AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/address1ET"
    FIELD_ADDRESS_2 = AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/address2ET"
    FIELD_CITY = AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cityET"
    FIELD_STATE = AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/stateET"
    FIELD_ZIP = AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/zipET"
    FIELD_COUNTRY = AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/countryET"
    BTN_TO_PAYMENT = AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/paymentBtn"

    def __init__(self, driver):
        super().__init__(driver)
        
    def is_checkout_page_loaded(self):
        """Verifica se o título da tela de Endereço está visível."""
        return self.is_element_displayed(*self.TITLE_CHECKOUT)

    def fill_shipping_address(self, user_data):
        """Preenche todos os campos de endereço usando o dicionário de dados."""
        # Se for necessário rolar, o driver está em self.driver
        # Ex: self.driver.execute_script('mobile: scrollGesture', {'direction': 'down'})
        
        self.send_keys_to_element(*self.FIELD_FULL_NAME, user_data["USERNAME"])
        self.send_keys_to_element(*self.FIELD_ADDRESS_1, user_data["ENDERECO_1"])
        self.send_keys_to_element(*self.FIELD_ADDRESS_2, user_data["ENDERECO_2"])
        self.send_keys_to_element(*self.FIELD_CITY, user_data["CIDADE"])
        self.send_keys_to_element(*self.FIELD_STATE, user_data["ESTADO"])
        self.send_keys_to_element(*self.FIELD_ZIP, user_data["ZIP_CODE"])
        self.send_keys_to_element(*self.FIELD_COUNTRY, user_data["PAIS"])
        
    def click_to_payment(self):
        """Clica no botão para ir para a próxima tela."""
        self.click_element(*self.BTN_TO_PAYMENT)
        time.sleep(2)