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
import re


def scrape_jumbo():
    url = "https://www.jumbocolombia.com/aguardiente-antioqueno-sin-azucar-24-botella-x-750ml/p"

    # ⚙️ Configurar navegador
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")

    print("🌐 Usando webdriver_manager (descarga automática).")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 20)
    driver.get(url)

    try:
        # Esperar que cargue el sitio completamente
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        time.sleep(4)

        # 🧾 Obtener nombre
        nombre = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "span.vtex-store-components-3-x-productBrand")
            )
        ).text.strip()

        # 💵 Obtener precio principal (no el de mililitros)
        precio_elemento = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.tiendasjumboqaio-jumbo-minicart-2-x-price")
            )
        )
        precio = precio_elemento.text.strip().replace("\xa0", " ")

        # Limpiar y formatear el precio
        match = re.search(r"\d[\d.]*", precio)
        if match:
            valor = match.group(0).replace(".", "")
            precio_formateado = "${:,.0f}".format(int(valor)).replace(",", ".")
        else:
            precio_formateado = "No encontrado"

        print(f"🧾 Producto: {nombre}")
        print(f"💵 Precio: {precio_formateado}")

        # Guardar en CSV
        os.makedirs("data", exist_ok=True)
        with open("data/precios_jumbo.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Producto", "Precio"])
            writer.writerow([nombre, precio_formateado])

        print("✅ Datos guardados correctamente en data/precios_jumbo.csv")

    except Exception as e:
        print(f"❌ Error al obtener datos: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    scrape_jumbo()
