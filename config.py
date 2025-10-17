# config.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Ruta local del driver
CHROMEDRIVER_PATH = r"C:\Users\ALEXANDRE VEGA\Desktop\scraping_aguardiente\chromedriver.exe"

def get_chrome_driver():
    """Configura y devuelve una instancia del driver de Chrome."""
    options = Options()
    # Si quieres ver la ventana del navegador, comenta esta línea:
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")

    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    return driver
