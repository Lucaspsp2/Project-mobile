from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
import time

class CartPage(BasePage):
    # --- LOCALIZADORES ---
    ICON_CART = AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cartIV" # Ícone para clicar na Home
    PRICE_TV = AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/priceTV" # Preço Unitário
    QUANTITY_TV = AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/noTV" # Quantidade (2)
    TOTAL_PRICE_TV = AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/totalPriceTV" # Subtotal
    BTN_CHECKOUT = AppiumBy.ACCESSIBILITY_ID, "Confirms products for checkout"

    def __init__(self, driver):
        super().__init__(driver)

    def go_to_cart(self):
        """Clica no ícone do carrinho (se o script ainda estiver na ProductPage ou Home)."""
        self.click_element(*self.ICON_CART)
        time.sleep(3) # Espera a tela do carrinho carregar

    def get_unit_price(self):
        """Captura e limpa o preço unitário."""
        price_str = self.get_element_text(*self.PRICE_TV).strip().replace("$", "").replace(" ", "")
        return float(price_str)

    def get_quantity(self):
        """Captura a quantidade do item."""
        return int(self.get_element_text(*self.QUANTITY_TV).strip())

    def get_subtotal_from_screen(self):
        """Captura e limpa o subtotal da tela."""
        return self.get_element_text(*self.TOTAL_PRICE_TV).strip().replace(" ", "")

    def click_checkout(self):
        """Clica no botão Proceed To Checkout."""
        self.click_element(*self.BTN_CHECKOUT)
        time.sleep(2)