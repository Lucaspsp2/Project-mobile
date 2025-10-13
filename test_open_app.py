# import time
# from appium import webdriver
# from appium.options.common.base import AppiumOptions
# from appium.webdriver.common.appiumby import AppiumBy


# options = AppiumOptions()
# options.load_capabilities({
#     "platformName": "Android",
#     "appium:deviceName": "emulator-5554",
#     "appium:automationName": "UiAutomator2",
#     "appium:appPackage": "com.saucelabs.mydemoapp.android",
#     "appium:ensureWebviewsHavePages": True,
#     "appium:nativeWebScreenshot": True,
#     "appium:newCommandTimeout": 3600,
#     "appium:connectHardwareKeyboard": True,
#     "appWaitActivity": "com.saucelabs.mydemoapp.android.view.activities.MainActivity",
#     "appWaitDuration": 30000  # opcional, tempo de espera em ms (30s)
# })

# driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
# time.sleep(4)

# produto_backpack = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().resourceId(\"com.saucelabs.mydemoapp.android:id/productIV\").instance(0)")
# produto_backpack.click()
# time.sleep(1)

# cor_verde_btn = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Green color")
# cor_verde_btn.click()

# adicionar_carrinho_btn = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Tap to add product to cart")
# adicionar_carrinho_btn.click()
# time.sleep(1)

# abrir_carrinho_btn = driver.find_element(by=AppiumBy.ID, value="com.saucelabs.mydemoapp.android:id/cartIV")
# abrir_carrinho_btn.click()
# time.sleep(2)

# # --- CHECKOUT: CARRINHO E LOGIN ---
# prosseguir_checkout_btn = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Confirms products for checkout")
# prosseguir_checkout_btn.click()
# time.sleep(2)

# # endereco_email1 = driver.find_element(by=AppiumBy.ID, value="com.saucelabs.mydemoapp.android:id/username2TV")
# # botao_login = driver.find_element(by=AppiumBy.ID, value="com.saucelabs.mydemoapp.android:id/loginBtn")

# # endereco_email2 = driver.find_element(by=AppiumBy.ID, value="com.saucelabs.mydemoapp.android:id/username1TV")
# # botao_login2 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Tap to login with given credentials")

# endereco_email3 = driver.find_element(by=AppiumBy.ID, value="com.saucelabs.mydemoapp.android:id/username3TV")
# botao_login3 = driver.find_element(by=AppiumBy.XPATH, value='//android.widget.Button[@content-desc="Tap to login with given credentials"]')


# # campo_usuario = driver.find_element(by=AppiumBy.ID, value="com.saucelabs.mydemoapp.android:id/nameET")
# # campo_senha = driver.find_element(by=AppiumBy.ID, value="com.saucelabs.mydemoapp.android:id/passwordET")
# # botao_login = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Tap to login with given credentials")

# # campo_usuario.send_keys("UserTest")
# # campo_senha.send_keys("PasswordTest")
# # botao_login.click()
# endereco_email3.click()
# botao_login3.click()
# time.sleep(2)

# # --- TELA DE INFORMAÇÕES DE ENVIO ---
# # driver.execute_script('mobile: scrollGesture', {'left': 100, 'top': 100, 'width': 800, 'height': 1500, 'direction': 'down', 'percent': 3.0})

# driver.find_element(by=AppiumBy.ID, value="com.saucelabs.mydemoapp.android:id/fullNameET").send_keys("test")
# driver.find_element(by=AppiumBy.ID, value="com.saucelabs.mydemoapp.android:id/address1ET").send_keys("rua test, n 7, bairro test")
# driver.find_element(by=AppiumBy.ID, value="com.saucelabs.mydemoapp.android:id/cityET").send_keys("recife")
# driver.find_element(by=AppiumBy.ID, value="com.saucelabs.mydemoapp.android:id/stateET").send_keys("PE")
# driver.find_element(by=AppiumBy.ID, value="com.saucelabs.mydemoapp.android:id/zipET").send_keys("90777")
# driver.find_element(by=AppiumBy.ID, value="com.saucelabs.mydemoapp.android:id/countryET").send_keys("test")

# prosseguir_pagamento_btn = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Saves user info for checkout")
# prosseguir_pagamento_btn.click()
# time.sleep(2)

# # --- TELA DE PAGAMENTO---
# # driver.execute_script('mobile: scrollGesture', {'left': 100, 'top': 100, 'width': 800, 'height': 1500, 'direction': 'down', 'percent': 3.0})

# driver.find_element(by=AppiumBy.ID, value="com.saucelabs.mydemoapp.android:id/nameET").send_keys("robo test")
# driver.find_element(by=AppiumBy.ID, value="com.saucelabs.mydemoapp.android:id/cardNumberET").send_keys("4077809977998899")
# driver.find_element(by=AppiumBy.ID, value="com.saucelabs.mydemoapp.android:id/expirationDateET").send_keys("01/26")
# driver.find_element(by=AppiumBy.ID, value="com.saucelabs.mydemoapp.android:id/securityCodeET").send_keys("321")

# revisar_pedido_btn = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Saves payment info and launches screen to review checkout data")
# revisar_pedido_btn.click()
# time.sleep(2)

# # --- TELA DE REVISÃO E CONCLUSÃO ---
# # driver.execute_script('mobile: scrollGesture', {'left': 100, 'top': 100, 'width': 800, 'height': 1500, 'direction': 'down', 'percent': 3.0})

# finalizar_pedido_btn = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Completes the process of checkout")
# finalizar_pedido_btn.click()
# time.sleep(5)

# # --- FINALIZAÇÃO ---
# driver.quit()#