from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
import time

class LoginPage(BasePage):
    # --- LOCALIZADORES ---
    TITLE_LOGIN = AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/loginTV"
    FIELD_USERNAME = AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/nameET"
    FIELD_PASSWORD = AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/passwordET"
    BTN_LOGIN = AppiumBy.ACCESSIBILITY_ID, "Tap to login with given credentials"

    # Mensagens de Erro
    ERROR_USERNAME = AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/nameErrorTV"
    ERROR_PASSWORD = AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/passwordErrorTV"

    # Credenciais de Teste na Tela
    USER_LIST_TV = AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/username1TV"
    PASS_LIST_TV = AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/password1TV"
    
    def __init__(self, driver):
        super().__init__(driver)

    def is_login_page_loaded(self):
        """Verifica se o título 'Login' está visível."""
        return self.is_element_displayed(*self.TITLE_LOGIN)

    def fill_login_fields(self, username, password):
        """Preenche os campos de usuário e senha."""
        # Limpa os campos antes de digitar, garantindo que não há sujeira
        self.find_element(*self.FIELD_USERNAME).clear()
        self.find_element(*self.FIELD_PASSWORD).clear()
        
        self.send_keys_to_element(*self.FIELD_USERNAME, username)
        self.send_keys_to_element(*self.FIELD_PASSWORD, password)

    def click_login(self):
        """Clica no botão de Login."""
        self.click_element(*self.BTN_LOGIN)
        time.sleep(2) # Espera a resposta do servidor/app

    def get_test_credentials(self):
        """Captura as credenciais de teste exibidas na tela."""
        username = self.get_element_text(*self.USER_LIST_TV)
        password = self.get_element_text(*self.PASS_LIST_TV)
        return username, password

    def is_error_username_displayed(self):
        """Verifica se a mensagem de erro do Username está visível."""
        return self.is_element_displayed(*self.ERROR_USERNAME)
    
    def is_error_password_displayed(self):
        """Verifica se a mensagem de erro da Password está visível."""
        return self.is_element_displayed(*self.ERROR_PASSWORD)