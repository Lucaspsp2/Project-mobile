import time
from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy



username = "KENNY"
endereco1 = "Rua da felicidade, n 7, agua quente"
endereco2 = "Rua da alegira, n 10, agua fia"
cidade = "Gravata"
estado = "Pernambuco"
pais = "Brasil"
cartao = "1234.5678.9012.3456"
data_cartao = "01/26"
codigo_cartao = "123"


# Essas são as instruções que dizem ao Appium ONDE e O QUÊ rodar.
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
    "appWaitDuration": 30000  # opcional, tempo de espera em ms (30s)
})

# Inicia a conexão com o Appium Server
driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
time.sleep(5) 


# Seleção do produto e validação de quantidade

titulo_produtos = driver.find_element(AppiumBy.XPATH, '//android.widget.TextView[@content-desc="Product Title" and @text="Sauce Labs Backpack (orange)"]')


#Esse 'assert' verifica se o elemento está na tela, continua. Se não estiver o teste para.
assert titulo_produtos.is_displayed(), "ERRO: A tela inicial não foi carregada."

# Clica no produto Backpack
produto_backpack = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().resourceId("com.saucelabs.mydemoapp.android:id/productIV").instance(2)')
produto_backpack.click()
time.sleep(2)

# botões de quantidade e botão de adicionar ao carrinho
botao_menos = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Decrease item quantity")
botao_mais = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Increase item quantity")
botao_add_cart = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Tap to add product to cart")

# Diminui a quantidade
botao_menos.click()
time.sleep(0.5)

# Valida que o botão está desativado com 0 unidades
assert botao_add_cart.get_attribute("enabled") == "false", "ERRO: Botão de carrinho deveria estar DESATIVADO com 0 unidades."

# Aumenta para 1 unidade
botao_mais.click()
time.sleep(0.5)

# Valida que o botão está ativado com 1 unidade
assert botao_add_cart.get_attribute("enabled") == "true", "ERRO: Botão de carrinho deveria estar ATIVADO com 1 unidade."

# Aumenta para 2 unidades e adiciona ao carrinho
botao_mais.click()
botao_add_cart.click()
time.sleep(1)

#Valida o círculo (badge) do carrinho
badge_carrinho = driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cartTV")

# Valida se o texto dentro do círculo é "2"
assert badge_carrinho.text == "2", f"ERRO: O círculo do carrinho deve ser '2', mas é '{badge_carrinho.text}'"
print("Passo 2 OK: Validação de quantidade e badge do carrinho funcionou.")

# Abre a tela do carrinho
icone_carrinho = driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cartIV")
icone_carrinho.click()
time.sleep(3)

# Valida o Subtotal no carrinho
VALOR_TOTAL_ESPERADO = "$59.98" # 2 x $29.99

# Encontra o elemento
elemento_total = driver.find_element(AppiumBy.ID, value= "com.saucelabs.mydemoapp.android:id/totalPriceTV")

# Captura o texto, remove espaços das bordas (strip) e remove QUALQUER ESPAÇO no meio (.replace)
# Isso garante que tanto ' $59.98 ' quanto '$ 59.98' sejam lidos como '$59.98'
valor_total_compra_limpo = elemento_total.text.strip().replace(" ", "")

# VALIDAÇÃO ROBUSTA: Garantimos que o valor esperado também está sem espaços.
assert valor_total_compra_limpo == VALOR_TOTAL_ESPERADO.replace(" ", ""), "ERRO: O subtotal no carrinho está errado."

# O comando de print pode ser removido agora, mas vou deixá-lo para que você veja o valor limpo:
print(f"DEBUG: Valor capturado e limpo: '{valor_total_compra_limpo}'")

# Clica em Proceed To Checkout
checkout_btn = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Confirms products for checkout")
checkout_btn.click()
time.sleep(2)

# Validações de Erro na tela de Login
titulo_login = driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/loginTV")
assert titulo_login.is_displayed(), "ERRO: A tela 'Login' não foi exibida."

campo_usuario = driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/nameET")
campo_senha = driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/passwordET") # Adicionado para uso antecipado
botao_login = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Tap to login with given credentials")

# --- TESTE DE ERRO 1: USERNAME VAZIO ---
# Tenta logar sem preencher nada. Username e Password estão vazios.
botao_login.click()
# Valida o erro de 'Username'
erro_username = driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/nameErrorTV")
assert erro_username.is_displayed(), "ERRO: Mensagem de 'Username obrigatório' não apareceu."
print("Validação de erro: Username vazio OK.")

# --- TESTE DE ERRO 2: PASSWORD VAZIO (ISOLADO) ---
# Preenche apenas o Username
campo_usuario.send_keys("testuser") 
# Garante que o campo Senha está vazio (mesmo que estivesse)
campo_senha.clear() 
# Clica para logar
botao_login.click()

# Valida a mensagem de erro de senha
erro_password = driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/passwordErrorTV")
assert erro_password.is_displayed(), "ERRO: Mensagem de 'Password obrigatória' não apareceu."
print("Validação de erro: Password vazio (Username preenchido) OK.")

# --- Logar com credenciais CORRETAS ---

# Rola para cima e preenche os campos
driver.execute_script('mobile: scrollGesture', {'left': 100, 'top': 1500, 'width': 800, 'height': 1500, 'direction': 'up', 'percent': 3.0})

# Captura o username e password da lista no app
username_lista = driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/username1TV")
password_lista = driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/password1TV")

# Limpa o texto temporário 'testuser' e o campo Senha
campo_usuario.clear() 
campo_senha.clear() 

# Digita as credenciais corretas
campo_usuario.send_keys(username_lista.text)
campo_senha.send_keys(password_lista.text)
botao_login.click()
time.sleep(3)
print("Passo 3 OK: Login realizado com sucesso.")


# Preenche Endereço (usamos o Scroll para ver o formulário todo)
assert driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/checkoutTitleTV").is_displayed(), "ERRO: Não carregou a tela de Endereço."
# O comando abaixo rola a tela para baixo
driver.execute_script('mobile: scrollGesture', {'left': 100, 'top': 100, 'width': 800, 'height': 1500, 'direction': 'down', 'percent': 3.0})

# Preenchendo os campos...
driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/fullNameET").send_keys(username)
driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/address1ET").send_keys(endereco1)
driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/address2ET").send_keys(endereco2)
driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cityET").send_keys(cidade)
driver.find_element(AppiumBy.ID,"com.saucelabs.mydemoapp.android:id/stateET").send_keys(estado)
driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/zipET").send_keys("10001")
driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/countryET").send_keys(pais)
driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/paymentBtn").click()
time.sleep(2)

#Preenche Pagamento
driver.execute_script('mobile: scrollGesture', {'left': 100, 'top': 100, 'width': 800, 'height': 1500, 'direction': 'down', 'percent': 3.0})
driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/nameET").send_keys(username)
driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cardNumberET").send_keys(cartao)
driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/expirationDateET").send_keys(data_cartao)
driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/securityCodeET").send_keys(codigo_cartao)
driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Saves payment info and launches screen to review checkout data").click()
time.sleep(2)


# Define o valor esperado (sem espaços para ser o padrão limpo)
VALOR_FINAL_ESPERADO = "$65.97" # $59.98 (Subtotal) + $9.99 (Frete) ou 65.97

# Captura o elemento na tela (que contém o valor)
elemento_total_final = driver.find_element(AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/totalAmountTV")

# Limpa o texto capturado: remove espaços das bordas e espaços no meio
valor_final_na_tela_limpo = elemento_total_final.text.strip().replace(" ", "")

# Faz a validação: compara o valor limpo com o valor esperado (também limpo)
assert valor_final_na_tela_limpo == VALOR_FINAL_ESPERADO.replace(" ", ""), "ERRO: O Total Final está incorreto."
print("Validação do Total Final (R$69.97) OK.")

# Rola e Clica em Place Order
driver.execute_script('mobile: scrollGesture', {'left': 100, 'top': 100, 'width': 800, 'height': 1500, 'direction': 'down', 'percent': 3.0})
driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Completes the process of checkout").click()
time.sleep(3)

