from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
import time

class ReviewPage(BasePage):
    # --- LOCALIZADORES ---
    TITLE_REVIEW = AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/titleTV"
    
    # Custo de Frete (ID que você encontrou)
    SHIPPING_TV = AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/amountTV"
    
    # Total Geral (ID que você encontrou)
    TOTAL_TV = AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/totalAmountTV"
    
    BTN_PLACE_ORDER = AppiumBy.ACCESSIBILITY_ID, "Place order button"

    def __init__(self, driver):
        super().__init__(driver)

    def is_review_page_loaded(self):
        """Verifica se o título da tela de Revisão está visível."""
        return self.is_element_displayed(*self.TITLE_REVIEW)
        
    def get_shipping_cost(self):
        """Captura e limpa o custo de envio (frete)."""
        # IMPORTANTE: O scroll para este elemento deve ser feito no arquivo de teste.
        price_str = self.get_element_text(*self.SHIPPING_TV).strip().replace("$", "").replace(" ", "")
        return float(price_str)

    def get_total_on_screen(self):
        """Captura e limpa o Total Geral na tela."""
        # Retorna o texto bruto para comparação no teste (ex: "$65.97")
        return self.get_element_text(*self.TOTAL_TV).strip() 

    def click_place_order(self):
        """Clica no botão Place Order (Finalizar Pedido)."""
        self.click_element(*self.BTN_PLACE_ORDER)
        # Não precisa de time.sleep() aqui, a validação da próxima página o cobrirá