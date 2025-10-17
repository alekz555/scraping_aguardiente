from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import csv
import os


def scrape_carulla():
    url = "https://www.carulla.com/aguardiente-sazucar-verde-718737/p"

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--log-level=3")

    print("🌐 Usando webdriver_manager (descarga automática).")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 15)
    driver.get(url)

    try:
        # Esperar a que el nombre del producto aparezca
        nombre = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.product-title_product-title__heading___mpLA"))
        ).text.strip()

        # Esperar el precio
        precio = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "p.ProductPrice_container__price__XmMWA"))
        ).text.strip()

        # Limpiar y formatear precio (añadir separador de miles)
        precio_num = int(precio.replace("$", "").replace(".", "").strip())
        precio_formateado = f"${precio_num:,.0f}".replace(",", ".")  # Ej: 42700 → 42.700

        print(f"🧾 Producto: {nombre}")
        print(f"💵 Precio: {precio_formateado}")

        # Guardar datos
        os.makedirs("data", exist_ok=True)
        with open("data/precios_carulla.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Producto", "Precio"])
            writer.writerow([nombre, precio_formateado])

        print("✅ Datos guardados correctamente en data/precios_carulla.csv")

    except Exception as e:
        print("❌ Error al obtener datos:", e)

    finally:
        driver.quit()


if __name__ == "__main__":
    scrape_carulla()
