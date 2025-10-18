PRESENTADO POR:

ALEXANDRE VEGA PATERNINA
LUIS FERNANDO ARRIETA AGUIRRE
CÉSAR CONTRERAS COLON


---------------Comparador de precios Aguardiente 750 ml (tapa verde)---------------

Proyecto sencillo de scraping + limpieza + tabla comparativa para ver cuánto cuesta el mismo producto en varias tiendas de Colombia.
Tiendas: Éxito, Carulla, Olímpica, La Rebaja, Jumbo, Dislicores y MercadoLibre.
Salida: un CSV unificado y un Excel con tabla formateada listo para mostrar.

---------------¿Qué hicimos (en palabras simples)?---------------
-Hicimos un archivo Python por tienda para extraer nombre y precio del producto.

-En tiendas que cargan el precio con JavaScript (VTEX) usamos Selenium y esperamos a que la página “termine de pintar”.

-En MercadoLibre, como el precio ya viene en el HTML, usamos Requests + BeautifulSoup (sin navegador).

-Limpieza de precios: quitamos $, puntos, espacios, etc. lo pasamos a número y al final lo formateamos ($47.500).

-Unimos todo con pandas en unificar_precios.py y generamos:

-data/resultados_limpio.csv (con ; para que Excel lo abra en columnas)

-data/comparativo_precios.xlsx (tabla con estilo + hoja comparativa por tienda)

---------------Tecnologías y librerías---------------

-Python 3

-Selenium (navegador real en modo headless)

-webdriver-manager (descarga automática de ChromeDriver)

-Requests + BeautifulSoup (solo MercadoLibre)

-pandas (unir, limpiar, ordenar)

-XlsxWriter / openpyxl

-requirements.txt incluye todo:

-selenium, webdriver-manager, pandas, beautifulsoup4, lxml, html5lib, requests, openpyxl, XlsxWriter

---------------Estructura del reposotorio---------------

scraping_aguardiente/
├─ data/                     # aquí quedan los CSV por tienda y los archivos finales
├─ tiendas/                  # un script por tienda (Exito.py, Jumbo.py, etc.)
├─ requirements.txt
├─ unificar_precios.py       # une, limpia y crea el Excel
├─ 00_install_global.bat     # instala librerías (sin venv)
├─ 02_run_all_no_venv.bat    # corre todo (scrapers + unificación)
└─ run_unifier_only.bat      # solo unifica


---------------Dificultades---------------

VTEX parte el precio en varios <span> (ej. Olímpica, Dislicores):
tomamos el contenedor y concatenamos currencyInteger + currencyGroup.

Jumbo: primero agarramos el precio por ml
selector correcto del precio total:
div.tiendasjumboqaio-jumbo-minicart-2-x-price.

NoSuchElementException: el DOM no estaba listo.
usamos WebDriverWait + un sleep corto.

NoSuchDriverException / chromedriver:
webdriver-manager lo descarga y gestiona solo.

CSV se ve “pegado” en una columna en Excel:
exportamos el CSV final con ; (regional ES).

PermissionError al guardar:
Excel abierto. Se cierra y se reintenta.

requirements.txt mal escrito
debe llamarse exactamente requirements.txt.

---------------Qué hace el unificador (unificar_precios.py)---------------

-Lee todos los data/precios_*.csv (uno por tienda).

-Detecta delimitador (, o ;) y filas “raras” (con comas dentro del producto).

-Limpia precio → número → ordena por precio.

Exporta:

resultados_limpio.csv (con ; y precio formateado)

comparativo_precios.xlsx

Hoja Comparativa (tabla con estilos)

Hoja Comparación (tipo pivot: filas = producto, columnas = tienda, resalta el menor)
