# test_mini_challenge.py
import sys
import os
import pytest

# Adiciona a pasta raiz ao sys.path para achar a pasta 'data'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.login_page import LoginPage
from pages.checkout_page import CheckoutPage
from pages.payment_page import PaymentPage
from pages.review_page import ReviewPage
from pages.complete_page import CompletePage

from data.data import VALID_USER, PRODUCTS  # <- ajustado para pasta 'data'

@pytest.mark.mobile
def test_01_product_selection_and_checkout(driver):
    """
    Fluxo: Home -> Product -> Add -> Cart -> Checkout -> Payment -> Review -> Complete
    Utiliza fluent interface retornando as páginas.
    """

    home = HomePage(driver)
    assert home.is_home_page_loaded(), "Home não carregou"

    # Passo 1: selecionar produto -> ProductPage
    product_page = home.select_backpack()

    # Validações de quantidade
    product_page.decrease_quantity()
    assert product_page.is_add_to_cart_enabled() is False
    product_page.increase_quantity()
    assert product_page.is_add_to_cart_enabled() is True

    product_page.increase_quantity()  # agora 2 unidades
    product_page.add_product_to_cart()
    badge_count = product_page.get_cart_badge_count()
    assert badge_count == "2", "Badge não informa 2"

    # ir para cart
    cart_page = product_page.click_cart_icon()

    unit_price = cart_page.get_unit_price()
    quantity = cart_page.get_quantity()
    assert quantity == 2

    subtotal_calculado = unit_price * quantity
    expected_subtotal_text = f"${subtotal_calculado:.2f}"
    subtotal_na_tela = cart_page.get_subtotal_from_screen()
    assert subtotal_na_tela == expected_subtotal_text.replace(" ", ""), "Subtotal divergente"

    # Proceed to login/checkout
    login_page = cart_page.click_checkout()
    assert login_page.is_login_page_loaded()

    # validações de erro
    login_page.click_login()
    assert login_page.is_error_username_displayed()
    login_page.enter_username("user_temp").enter_password("")
    login_page.click_login()
    assert login_page.is_error_password_displayed()

    # login com credenciais da tela (test credentials)
    username_lista, password_lista = login_page.get_test_credentials()
    checkout_page = login_page.login(username_lista, password_lista)
    assert checkout_page.is_checkout_page_loaded()

    # preencher endereço com dados de data.py
    checkout_page.fill_shipping_address(VALID_USER)
    payment_page = checkout_page.click_to_payment()
    assert payment_page.is_payment_page_loaded()

    # validação de obrigatoriedade
    payment_page.click_review_order()
    assert payment_page.is_error_displayed(payment_page.Locators.ERROR_FULL_NAME)

    # preencher pagamento com dados de data.py
    payment_page.fill_payment_fields(VALID_USER)
    review_page = payment_page.click_review_order()
    assert review_page.is_review_page_loaded()

    # certificar que TOTAL visível (scroll)
    review_page.scroll_to_element(review_page.Locators.TOTAL_TV)

    # finalizar pedido
    complete_page = review_page.click_place_order()
    assert complete_page.is_complete_page_loaded()
