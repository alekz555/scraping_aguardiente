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


def scrape_larebaja():
    url = "https://www.larebajavirtual.com/aguardiente-antioqueno-verde-116475/p"

    # 🧩 Configuración del navegador
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")

    print("🌐 Usando webdriver_manager (descarga automática).")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 15)

    driver.get(url)

    try:
        # Esperar a que cargue completamente
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        time.sleep(2)

        # 🧾 Nombre del producto
        nombre = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "span.vtex-store-components-3-x-productBrand")
            )
        ).text.strip()

        # 💵 Precio del producto
        precio = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "span.copservir-larebaja-theme-7-x-productPriceValue")
            )
        ).text.strip()

        # Limpiar formato del precio
        precio_num = precio.replace("$", "").replace(".", "").strip()
        if precio_num.isdigit():
            precio_formateado = "${:,.0f}".format(int(precio_num)).replace(",", ".")
        else:
            precio_formateado = precio

        print(f"🧾 Producto: {nombre}")
        print(f"💵 Precio: {precio_formateado}")

        # Guardar en CSV
        os.makedirs("data", exist_ok=True)
        with open("data/precios_larebaja.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Producto", "Precio"])
            writer.writerow([nombre, precio_formateado])

        print("✅ Datos guardados correctamente en data/precios_larebaja.csv")

    except Exception as e:
        print(f"❌ Error al obtener datos: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    scrape_larebaja()
