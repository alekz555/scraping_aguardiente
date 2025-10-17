import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os

# URL del producto
url = "https://www.mercadolibre.com.co/aguardiente-antioqueno-verde-bo-ml-a-80/p/MCO21772986#polycard_client=search-nordic&search_layout=stack&position=6&type=product&tracking_id=74af4ff9-d35d-46f2-8aa1-780d7000aa6e&wid=MCO1704648438&sid=search"

# Obtener contenido de la página
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Extraer nombre y precio
nombre = soup.find("h1", class_="ui-pdp-title")
precio = soup.find("span", class_="andes-money-amount__fraction")

nombre_producto = nombre.text.strip() if nombre else "No encontrado"
precio_producto = precio.text.strip().replace(".", "") if precio else "0"

# Convertir a número si es posible
try:
    precio_producto = int(precio_producto)
except:
    precio_producto = 0

# Crear carpeta de datos si no existe
os.makedirs("data", exist_ok=True)

# Guardar en CSV
archivo_csv = "data/precios_mercadolibre.csv"
existe = os.path.isfile(archivo_csv)

with open(archivo_csv, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    if not existe:
        writer.writerow(["Fecha", "Tienda", "Producto", "Precio"])
    writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "MercadoLibre", nombre_producto, precio_producto])

print(f"🛒 Producto: {nombre_producto}")
print(f"💰 Precio: ${precio_producto:,}")
print(f"✅ Guardado correctamente en {archivo_csv}")
