import pytest
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.login_page import LoginPage
from pages.checkout_page import CheckoutPage
from pages.payment_page import PaymentPage
from pages.review_page import ReviewPage
from pages.complete_page import CompletePage
import data
# Certifique-se de que a variável CAPABILITIES (com 'deviceName', 'appPackage', etc.)
# e o fixture 'driver' estão definidos corretamente no seu conftest.py

@pytest.fixture(scope="function")
def product_data():
    """Fixture para armazenar dados de preço/quantidade durante o fluxo."""
    return {"quantity": 0, "unit_price": 0.0}

@pytest.mark.mobile
def test_01_product_selection_and_checkout(driver, product_data):
    """
    Passos 1 a 5: Fluxo completo de compra, do produto à conclusão do pedido, com validações.
    """

    # 1. Inicializa as Page Objects
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)
    login_page = LoginPage(driver)
    checkout_page = CheckoutPage(driver)
    payment_page = PaymentPage(driver)
    review_page = ReviewPage(driver)        
    complete_page = CompletePage(driver)    

    print("\n--- INICIANDO TESTE ---")

    # --- PASSO 1: SELEÇÃO DE PRODUTO ---
    print("\n--- INICIANDO PASSO 1: SELEÇÃO DE PRODUTO ---")
    assert home_page.is_home_page_loaded(), "ERRO: A tela inicial de produtos não foi carregada."
    home_page.select_backpack()
    
    # Validações de quantidade (diminuir para 0 desabilita o botão)
    product_page.decrease_quantity()
    assert product_page.is_add_to_cart_enabled() == False
    product_page.increase_quantity()
    assert product_page.is_add_to_cart_enabled() == True
    
    product_page.increase_quantity() # Vai para 2 unidades
    product_page.add_product_to_cart()
    badge_count = product_page.get_cart_badge_count()
    assert badge_count == "2"
    print("Passo 1 OK: 2 unidades adicionadas e badge validado.")
    time.sleep(1)

    # --- PASSO 2: VALIDAÇÃO DINÂMICA NO CARRINHO ---
    print("\n--- INICIANDO PASSO 2: VALIDAÇÃO NO CARRINHO ---")
    cart_page.go_to_cart()
    
    unit_price = cart_page.get_unit_price()
    quantity = cart_page.get_quantity()

    # Salva dados para uso futuro
    product_data["unit_price"] = unit_price
    product_data["quantity"] = quantity

    assert quantity == 2, "ERRO: Quantidade no carrinho não é 2."
    subtotal_calculado = unit_price * quantity
    VALOR_ESPERADO_SUBTOTAL = f"${subtotal_calculado:.2f}"
    
    subtotal_na_tela_limpo = cart_page.get_subtotal_from_screen()
    assert subtotal_na_tela_limpo == VALOR_ESPERADO_SUBTOTAL.replace(" ", ""), "ERRO: Subtotal calculado não bate com o valor na tela."
    print("Passo 2 OK: Subtotal validado dinamicamente.")
    cart_page.click_checkout()
    time.sleep(2)

    # --- PASSO 3: VALIDAÇÕES DE ERRO E LOGIN ---
    print("\n--- INICIANDO PASSO 3: LOGIN E VALIDAÇÕES DE ERRO ---")
    assert login_page.is_login_page_loaded(), "ERRO: A tela 'Login' não foi exibida."
    
    # Validações de erro
    login_page.click_login()
    assert login_page.is_error_username_displayed(), "ERRO: Mensagem de 'Username obrigatório' não apareceu."
    login_page.fill_login_fields(username="user_temp", password="")
    login_page.click_login()
    assert login_page.is_error_password_displayed(), "ERRO: Mensagem de 'Password obrigatória' não apareceu."
    
    # Login com sucesso
    username_lista, password_lista = login_page.get_test_credentials()
    login_page.fill_login_fields(username=username_lista, password=password_lista)
    login_page.click_login()
    print("Passo 3 OK: Login realizado com sucesso após validações de erro.")
    time.sleep(1)

    # --- PASSO 4: PREENCHIMENTO DE ENDEREÇO E PAGAMENTO ---
    print("\n--- INICIANDO PASSO 4: ENDEREÇO E PAGAMENTO ---")

    # Preenche Endereço
    assert checkout_page.is_checkout_page_loaded(), "ERRO: Não carregou a tela de Endereço."
    shipping_data = {
        "USERNAME": data.USERNAME, "ENDERECO_1": data.ENDERECO_1, "ENDERECO_2": data.ENDERECO_2, 
        "CIDADE": data.CIDADE, "ESTADO": data.ESTADO, "ZIP_CODE": data.ZIP_CODE, "PAIS": data.PAIS,
    }
    checkout_page.fill_shipping_address(shipping_data)
    checkout_page.click_to_payment()

    # Preenche Pagamento
    assert payment_page.is_payment_page_loaded(), "ERRO: Não carregou a tela de Pagamento."
    
    # PLUS: Validações de campos obrigatórios (clicar antes de preencher)
    payment_page.click_review_order()
    assert payment_page.is_error_displayed(payment_page.ERROR_FULL_NAME), "ERRO: Validação Nome obrigatório falhou."
    
    card_data = {
        "USERNAME": data.USERNAME, "CARTAO": data.CARTAO, 
        "DATA_CARTAO": data.DATA_CARTAO, "CODIGO_CARTAO": data.CODIGO_CARTAO,
    }
    payment_page.fill_payment_fields(card_data)
    payment_page.click_review_order()

    print("Passo 4 OK: Endereço e Pagamento preenchidos e validados com sucesso.")
    time.sleep(1)

    # --- PASSO 5: REVISÃO DE PREÇOS E FINALIZAÇÃO DO PEDIDO ---
    print("\n--- INICIANDO PASSO 5: REVISÃO E FINALIZAÇÃO ---")

    assert review_page.is_review_page_loaded(), "ERRO: Não carregou a tela de Revisão do Pedido."

    # --- AÇÃO CRUCIAL: ROLAGEM ANTES DE BUSCAR O FRETE/TOTAL ---
    print("Rolando a tela para garantir que Frete e Total estejam visíveis...")
    # Chamamos o método de scroll da BasePage até que o elemento TOTAL_TV seja visível.
    review_page.scroll_to_element(*review_page.TOTAL_TV) 
    time.sleep(1)
    
    # 1. VALOR ESPERADO (Subtotal é calculado, não lido na tela)
    subtotal_calculado = product_data["unit_price"] * product_data["quantity"]
    
    # 2. CAPTURA DO FRETE E TOTAL
    frete_na_tela = review_page.get_shipping_cost()
    
    # 3. VALIDAÇÃO DO CUSTO TOTAL (Subtotal CALCULADO + Frete LIDO = Total LIDO)
    total_calculado = subtotal_calculado + frete_na_tela
    VALOR_ESPERADO_TOTAL = f"${total_calculado:.2f}"
    
    total_na_tela = review_page.get_total_on_screen()
    
    assert total_na_tela == VALOR_ESPERADO_TOTAL, f"ERRO: Total na tela ({total_na_tela}) não corresponde ao calculado ({VALOR_ESPERADO_TOTAL})."

    # 4. FINALIZAÇÃO
    review_page.click_place_order()
    
    # 5. Validação Final
    assert complete_page.is_order_complete_page_loaded(), "ERRO: Não carregou a tela de Pedido Concluído."
    print("Passo 5 OK: Revisão de preços validada e pedido finalizado com sucesso.")
    print("\n--- TESTE CONCLUÍDO COM SUCESSO: Fluxo de Compra Finalizado ---")