from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import csv
import os
import time

def get_chrome_service():
    """
    Retorna el servicio de Chrome usando chromedriver local si existe,
    o webdriver_manager si no.
    """
    local_driver = "C:\\chromedriver\\chromedriver.exe"
    if os.path.exists(local_driver):
        print("✅ Usando chromedriver local.")
        return Service(local_driver)
    else:
        print("🌐 Usando webdriver_manager (descarga automática).")
        return Service(ChromeDriverManager().install())

def scrape_olimpica():
    url = "https://www.olimpica.com/aguardiente-antioqueno-sin-azucar-750-ml-7702049001644-1492643/p"

    # Configuración del navegador
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")

    # Inicializar Chrome con detección automática del driver
    service = get_chrome_service()
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    wait = WebDriverWait(driver, 15)

    try:
        # Esperar carga completa de la página
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        time.sleep(3)

        # Extraer nombre del producto
        nombre = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[contains(@class,'productBrand')]")
            )
        ).text.strip()

        # Bloque de precio
        bloque_precio = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'productPriceClass')] | //div[contains(@class,'priceContainer')]")
            )
        )

        # Buscar las partes del precio
        partes_precio = bloque_precio.find_elements(
            By.XPATH,
            ".//span[contains(@class,'currencyInteger') or contains(@class,'currencyGroup')]"
        )

        if not partes_precio:
            # fallback: buscar el primer span con número
            partes_precio = driver.find_elements(
                By.XPATH,
                "//span[contains(@class,'currencyInteger')]"
            )

        precio = "".join([p.text for p in partes_precio if p.text.strip()])
        precio = f"$ {precio}"

        # Crear carpeta y guardar CSV
        os.makedirs("data", exist_ok=True)
        with open("data/precios_olimpica.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Tienda", "Producto", "Precio"])
            writer.writerow(["Olímpica", nombre, precio])

        print("✅ Datos guardados correctamente en data/precios_olimpica.csv")
        print(f"🧾 Producto: {nombre}")
        print(f"💵 Precio: {precio}")

    except Exception as e:
        print(f"❌ Error al obtener datos: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    scrape_olimpica()