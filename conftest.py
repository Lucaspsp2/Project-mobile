import pytest
from appium import webdriver
from appium.options.common.base import AppiumOptions
import time

CAPABILITIES = {
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
}

# 1. FIXTURE DE DADOS (SCOPE="SESSION" - MANTÉM OS DADOS DURANTE TODOS OS TESTES)
@pytest.fixture(scope="session") 
def product_data():
    """Fixture para armazenar dados dinâmicos do produto entre os testes."""
    return {
        "unit_price": 0.0,
        "quantity": 0
    }

# 2. FIXTURE DO DRIVER (SCOPE="FUNCTION" - RECRIA O DRIVER PARA CADA TESTE)
@pytest.fixture(scope="function")
def driver():

    # --- SETUP (Configuração: Antes do Teste) ---
    options = AppiumOptions()
    options.load_capabilities(CAPABILITIES)
    
    _driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    time.sleep(5) 
    print("\n--- INICIANDO TESTE ---")
    
    # O Pytest passa o controle para a função de teste
    yield _driver
    
    # --- TEARDOWN (Limpeza: Depois do Teste) ---
    # Este bloco é executado após o teste
    print("--- ENCERRANDO DRIVER ---")
    _driver.quit()