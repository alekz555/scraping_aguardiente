from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os

def scrape_exito():
    # URL del producto
    url = "https://www.exito.com/aguardiente-sazucar-verde-718737/p"

    # Configurar opciones del navegador
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # ejecuta sin abrir ventana (puedes quitarlo si quieres ver)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Inicializar Chrome automáticamente
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    try:
        wait = WebDriverWait(driver, 15)  # espera máxima de 15 segundos

        # Esperar hasta que el nombre del producto sea visible
        nombre_elem = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "h1.product-title_product-title__heading___mpLA")
        ))
        nombre = nombre_elem.text.strip()

        # Esperar hasta que el precio sea visible
        precio_elem = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "p.ProductPrice_container__price__XmMWA.ProductPrice_text20__jR3lE")
        ))
        precio = precio_elem.text.strip()

        print(f"🧾 Producto: {nombre}")
        print(f"💵 Precio: {precio}")

        # Crear DataFrame con los datos
        df = pd.DataFrame({
            "Tienda": ["Éxito"],
            "Producto": [nombre],
            "Precio": [precio]
        })

        # Guardar resultados
        os.makedirs("data", exist_ok=True)
        df.to_csv("data/precios_exito.csv", index=False, encoding="utf-8-sig")
        print("✅ Datos guardados correctamente en data/precios_exito.csv")

    except Exception as e:
        print(f"❌ Error al obtener datos: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_exito()
