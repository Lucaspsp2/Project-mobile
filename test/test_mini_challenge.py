import time
from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy

# --- VARIÁVEIS DE DADOS (PARA MANUTENIBILIDADE) ---
username = "Robo test"
endereco1 = "Rua da felicidade, n 7, agua quente"
endereco2 = "Rua da alegira, n 10, agua fia"
cidade = "Gravata"
estado = "Pernambuco"
pais = "Brasil"
cartao = "1234567890123456" 
data_cartao = "0126" 
codigo_cartao = "123"

# Variáveis globais para armazenar dados COLETADOS DA TELA
# Elas são globais APENAS por estarem aqui, no topo do script.
PRECO_UNITARIO_REAL = 0.0
QUANTIDADE_REAL = 0
FRETE = 0.0 
# --- FIM DAS VARIÁVEIS DE DADOS ---


# --- CONFIGURAÇÃO INICIAL ---
options = AppiumOptions()
options.load_capabilities({
   "platformName": "Android",
    "appium:deviceName": "emulator-5554",
    "appium:automationName": "UiAutomator2",
    "appium:appPackage": "com.saucelabs.mydemoapp.android",
    "appium:ensureWebviewsHavePages": True,
    "appium:nativeWebScreenshot": True,
    "appium:newCommandTimeout": 3600,
    "appium:connectHardwareKeyboard": True,
    "appWaitActivity": "com.saucelabs.mydemoapp.android.view.activities.MainActivity",
    "appWaitDuration": 30000 
})

# Inicia a conexão com o Appium Server
driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
time.sleep(5) 
print("--- TESTE INICIADO ---")


# --- 1. SELEÇÃO E VALIDAÇÃO DE QUANTIDADE ---

titulo_produtos = driver.find_element(AppiumBy.XPATH, '//android.widget.TextView[@content-desc="Product Title" and @text="Sauce Labs Backpack (orange)"]')
assert titulo_produtos.is_displayed(), "ERRO: A tela inicial não foi carregada."

produto_backpack = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/productIV").instance(2)')
produto_backpack.click()
time.sleep(2)

botao_menos = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Decrease item quantity")
botao_mais = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Increase item quantity")
botao_add_cart = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Tap to add product to cart")

# Validação: 0 unidades = Botão Inativo
botao_menos.click()
time.sleep(0.5)
assert botao_add_cart.get_attribute("enabled") == "false", "ERRO: Botão de carrinho deveria estar DESATIVADO com 0 unidades."

# Validação: 1 unidade = Botão Ativo
botao_mais.click()
time.sleep(0.5)
assert botao_add_cart.get_attribute("enabled") == "true", "ERRO: Botão de carrinho deveria estar ATIVADO com 1 unidade."

# Adiciona 2 unidades
botao_mais.click()
botao_add_cart.click()
time.sleep(1)

# Valida o badge
badge_carrinho = driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cartTV")
assert badge_carrinho.text == "2", f"ERRO: O círculo do carrinho deve ser '2', mas é '{badge_carrinho.text}'"
print("Passo 1 OK: 2 unidades adicionadas e badge validado.")


# --- 2. VALIDAÇÃO DINÂMICA NO CARRINHO (COLETA DE DADOS) ---

icone_carrinho = driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cartIV")
icone_carrinho.click()
time.sleep(3)

# --- 2. VALIDAÇÃO DINÂMICA NO CARRINHO (COLETA DE DADOS) ---

icone_carrinho = driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cartIV")
icone_carrinho.click()
time.sleep(3)

# 1. CAPTURA: Preço Unitário
# CORREÇÃO AQUI: Mudando de ACCESSIBILITY_ID para ID de Recurso
elemento_preco_unitario = driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/priceTV")
preco_unitario_str = elemento_preco_unitario.text.strip().replace("$", "").replace(" ", "")
PRECO_UNITARIO_REAL = float(preco_unitario_str)

# 2. CAPTURA: Quantidade (USANDO ID FORNECIDO: noTV)
elemento_quantidade = driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/noTV") 
QUANTIDADE_REAL = int(elemento_quantidade.text.strip()) 
assert QUANTIDADE_REAL == 2, "ERRO: Quantidade no carrinho não é 2."

# --- VALIDAÇÃO DO SUBTOTAL (Cálculo Dinâmico) ---
subtotal_calculado = PRECO_UNITARIO_REAL * QUANTIDADE_REAL
VALOR_ESPERADO_SUBTOTAL = f"${subtotal_calculado:.2f}" 
# ... (o resto do Passo 2 continua igual)

elemento_subtotal_na_tela = driver.find_element(AppiumBy.ID, value= "com.saucelabs.mydemoapp.android:id/totalPriceTV")
subtotal_na_tela_limpo = elemento_subtotal_na_tela.text.strip().replace(" ", "")

# Asserção Robusta
assert subtotal_na_tela_limpo == VALOR_ESPERADO_SUBTOTAL.replace(" ", ""), "ERRO: Subtotal calculado não bate com o valor na tela."
print("Passo 2 OK: Subtotal validado dinamicamente.")

# Clica em Proceed To Checkout
checkout_btn = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Confirms products for checkout")
checkout_btn.click()
time.sleep(2)


# --- 3. VALIDAÇÕES DE ERRO E LOGIN ---

titulo_login = driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/loginTV")
assert titulo_login.is_displayed(), "ERRO: A tela 'Login' não foi exibida."

campo_usuario = driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/nameET")
campo_senha = driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/passwordET") 
botao_login = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Tap to login with given credentials")

# TESTE DE ERRO 1: USERNAME VAZIO
botao_login.click()
erro_username = driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/nameErrorTV")
assert erro_username.is_displayed(), "ERRO: Mensagem de 'Username obrigatório' não apareceu."

# TESTE DE ERRO 2: PASSWORD VAZIO (ISOLADO)
campo_usuario.send_keys("testuser") 
campo_senha.clear() 
botao_login.click()
erro_password = driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/passwordErrorTV")
assert erro_password.is_displayed(), "ERRO: Mensagem de 'Password obrigatória' não apareceu."

# 3. PLUS: TESTE DE CREDENCIAIS INVÁLIDAS (Senha Incorreta)
campo_usuario.clear()
campo_senha.send_keys("123") 
botao_login.click()
time.sleep(2) # Espera maior para a resposta do servidor/app
erro_username = driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/nameErrorTV")
assert erro_username.is_displayed(), "ERRO: Mensagem de 'Username obrigatório' não apareceu."

# Logar com credenciais CORRETAS
#driver.execute_script('mobile: scrollGesture', {'left': 100, 'top': 1500, 'width': 800, 'height': 1500, 'direction': 'up', 'percent': 3.0})
campo_senha.clear()
username_lista = driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/username1TV")
password_lista = driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/password1TV")
campo_usuario.clear() 
campo_senha.clear() 
campo_usuario.send_keys(username_lista.text)
campo_senha.send_keys(password_lista.text)
botao_login.click()
time.sleep(3)
print("Passo 3 OK: Login realizado com sucesso.")



# --- 4. PREENCHIMENTO DE ENDEREÇO E PAGAMENTO ---

# Preenche Endereço
assert driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/checkoutTitleTV").is_displayed(), "ERRO: Não carregou a tela de Endereço."
# driver.execute_script('mobile: scrollGesture', {'left': 100, 'top': 100, 'width': 800, 'height': 1500, 'direction': 'down', 'percent': 3.0})

driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/fullNameET").send_keys(username)
driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/address1ET").send_keys(endereco1)
driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/address2ET").send_keys(endereco2)
driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cityET").send_keys(cidade)
driver.find_element(AppiumBy.ID,"com.saucelabs.mydemoapp.android:id/stateET").send_keys(estado)
driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/zipET").send_keys("10001")
driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/countryET").send_keys(pais)
driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/paymentBtn").click()
time.sleep(2)

# Click Review Order
el16 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Saves payment info and launches screen to review checkout data')
el16.click()
time.sleep(2)

# Plus: Validate Requireds
full_name_validate = driver.find_element(by=AppiumBy.ID, value="com.saucelabs.mydemoapp.android:id/nameErrorTV")
assert full_name_validate.is_displayed()
card_number_validate = driver.find_element(by=AppiumBy.ID, value="com.saucelabs.mydemoapp.android:id/cardNumberErrorIV")
assert card_number_validate.is_displayed()
expiration_date_validate = driver.find_element(by=AppiumBy.ID, value="com.saucelabs.mydemoapp.android:id/expirationDateIV")
assert expiration_date_validate.is_displayed()
security_code_validate = driver.find_element(by=AppiumBy.ID, value="com.saucelabs.mydemoapp.android:id/securityCodeIV")
assert security_code_validate.is_displayed()

# Validate Checkout Payment
checkout_validate = driver.find_element(by=AppiumBy.ID, value="com.saucelabs.mydemoapp.android:id/enterPaymentTitleTV")
assert checkout_validate.is_enabled(), "Activate"

# Validate Payment
shipping_adress = driver.find_element(by=AppiumBy.ID, value="com.saucelabs.mydemoapp.android:id/enterPaymentMethodTV")
assert shipping_adress.is_enabled(), "Activate"



# Preenche Pagamento
driver.execute_script('mobile: scrollGesture', {'left': 100, 'top': 100, 'width': 800, 'height': 1500, 'direction': 'down', 'percent': 3.0})
driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/nameET").send_keys(username)
driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cardNumberET").send_keys(cartao)
driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/expirationDateET").send_keys(data_cartao)
driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/securityCodeET").send_keys(codigo_cartao)
driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Saves payment info and launches screen to review checkout data").click()
time.sleep(2)
print("Passo 4 OK: Login realizado com sucesso.")

# --- 5. VALIDAÇÃO TOTAL FINAL DINÂMICA (REVISÃO) ---

# 1. VALOR DO FRETE FIXO: Define o frete fixo em 5.99
# Isso remove a necessidade de buscar o elemento FRETE na tela.
FRETE = 5.99

# ROLAGEM NECESSÁRIA: Rola para baixo para garantir que o Total Final esteja visível,
# mesmo que o frete não precise ser capturado.
driver.execute_script('mobile: scrollGesture', {'left': 100, 'top': 1500, 'width': 800, 'height': 1500, 'direction': 'down', 'percent': 3.0})
time.sleep(1) 

# 2. CAPTURA: Valor Total Final (na tela)
elemento_total_final = driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/totalAmountTV")
valor_final_na_tela_limpo = elemento_total_final.text.strip().replace(" ", "")

# --- CÁLCULO E VALIDAÇÃO FINAL ---
# FÓRMULA CORRETA: (PREÇO * QUANTIDADE) + FRETE FIXO
total_final_calculado = (PRECO_UNITARIO_REAL * QUANTIDADE_REAL) + FRETE
VALOR_FINAL_ESPERADO = f"${total_final_calculado:.2f}" 

assert valor_final_na_tela_limpo == VALOR_FINAL_ESPERADO.replace(" ", ""), "ERRO: O Total Final Calculado não bate com o valor na tela."
print(f"Passo 5 OK: Total Final validado dinamicamente: {VALOR_FINAL_ESPERADO}.")

# Clica em Place Order
driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Completes the process of checkout").click()
time.sleep(3)


# --- 6. CONCLUSÃO E LIMPEZA ---
assert driver.find_element(AppiumBy.XPATH, "//android.widget.TextView[@text='Checkout Complete']").is_displayed(), "ERRO: Tela de conclusão não apareceu."
driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Tap to open catalog").click()
time.sleep(2)
assert driver.find_element(AppiumBy.ACCESSIBILITY_ID, "View cart").is_displayed(), "ERRO: Não retornou à tela 'Products'."

driver.quit()
print("--- TESTE FINALIZADO COM SUCESSO! ---")