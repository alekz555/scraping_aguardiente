import os, csv, re, datetime
import pandas as pd

# ========= CONFIG =========
CARPETA = "data"
PATRON = r"precios_.*\.csv"  # todos los archivos por tienda
# =========================

def leer_csv_flexible(ruta):
    """Lee un CSV de tienda y devuelve lista de (producto, precio_num) robusto."""
    registros = []

    # Detectar si el archivo tiene encabezado estándar (Fecha,Tienda,Producto,Precio) – ej. MercadoLibre
    with open(ruta, "r", encoding="utf-8") as f:
        primera = f.readline().strip()

    if all(h in primera for h in ["Fecha", "Tienda", "Producto", "Precio"]):
        # Dejar que pandas infiera el separador
        df = pd.read_csv(ruta, sep=None, engine="python")
        if "Producto" in df.columns and "Precio" in df.columns:
            for _, row in df.iterrows():
                prod = str(row["Producto"]).strip()
                precio_raw = str(row["Precio"]).strip()
                precio = limpiar_precio(precio_raw)
                registros.append((prod, precio))
        return registros

    # Si no es el formato de ML, hacemos lectura manual con delimitador detectado
    with open(ruta, "r", encoding="utf-8") as f:
        contenido = f.read().strip()
    delim = ";" if (";" in contenido and "," not in contenido) else ","
    reader = csv.reader(contenido.splitlines(), delimiter=delim)
    next(reader, None)  # saltar encabezado

    for fila in reader:
        if not fila:
            continue
        # Si hay más de 2 columnas, asumimos que la última es precio y el resto forman el producto
        if len(fila) > 2:
            producto = " ".join(fila[:-1]).strip()
            precio_raw = fila[-1].strip()
        elif len(fila) == 2:
            producto, precio_raw = fila[0].strip(), fila[1].strip()
        else:
            continue
        registros.append((producto, limpiar_precio(precio_raw)))
    return registros

def limpiar_precio(precio_raw: str):
    """Devuelve precio como int (o None) desde '$ 47.500', '47,500', etc."""
    if precio_raw is None:
        return None
    # extraer solo dígitos
    solo_digitos = re.sub(r"[^\d]", "", str(precio_raw))
    return int(solo_digitos) if solo_digitos.isdigit() else None

def main():
    archivos = [f for f in os.listdir(CARPETA) if re.fullmatch(PATRON, f)]
    if not archivos:
        print("❌ No se encontraron archivos 'precios_*.csv' en data/")
        return

    fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filas = []

    for archivo in archivos:
        ruta = os.path.join(CARPETA, archivo)
        tienda = os.path.splitext(archivo)[0].replace("precios_", "").capitalize()

        try:
            for producto, precio in leer_csv_flexible(ruta):
                if not producto:
                    continue
                filas.append({
                    "Fecha": fecha_actual,
                    "Tienda": tienda,
                    "Producto": producto,
                    "Precio_num": precio
                })
            print(f"✅ Cargado: {archivo}")
        except Exception as e:
            print(f"⚠️ Error leyendo {archivo}: {e}")

    if not filas:
        print("❌ No se pudieron extraer registros.")
        return

    df = pd.DataFrame(filas, columns=["Fecha", "Tienda", "Producto", "Precio_num"])
    # limpiar básicos
    df["Tienda"] = df["Tienda"].str.strip().str.capitalize()
    df["Producto"] = (
        df["Producto"]
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    # Guardar CSV “crudo” pero legible por Excel ES (separador ;)
    df_csv = df.copy()
    df_csv["Precio"] = df_csv["Precio_num"].map(lambda x: f"${x:,.0f}".replace(",", ".") if pd.notna(x) else "")
    df_csv = df_csv.drop(columns=["Precio_num"])
    salida_csv_limpio = os.path.join(CARPETA, "resultados_limpio.csv")
    df_csv.to_csv(salida_csv_limpio, sep=";", index=False, encoding="utf-8-sig")
    print(f"📁 CSV limpio (con ;) -> {salida_csv_limpio}")

    # ---- Excel bonito con tabla y hoja comparativa ----
    try:
        with pd.ExcelWriter(os.path.join(CARPETA, "comparativo_precios.xlsx"),
                            engine="xlsxwriter") as writer:
            # Hoja 1: Comparativa (en formato de tabla)
            df_excel = df.copy()
            df_excel = df_excel.sort_values(by="Precio_num").reset_index(drop=True)
            df_excel.rename(columns={"Precio_num": "Precio"}, inplace=True)
            df_excel.to_excel(writer, sheet_name="Comparativa", index=False)

            wb  = writer.book
            ws1 = writer.sheets["Comparativa"]

            # Formatos
            fmt_header = wb.add_format({"bold": True, "font_color": "white", "align": "center", "valign": "vcenter", "bg_color": "#4F81BD"})
            fmt_border = wb.add_format({"border": 1})
            fmt_price  = wb.add_format({"num_format": "#,##0", "align": "right", "border": 1})
            fmt_text   = wb.add_format({"align": "left", "border": 1})

            # Convertir a tabla
            filas, cols = df_excel.shape
            ws1.add_table(0, 0, filas, cols-1, {
                "name": "TablaComparativa",
                "style": "Table Style Medium 9",
                "columns": [{"header": c} for c in df_excel.columns]
            })

            # Anchos y formatos de columnas
            ws1.set_column("A:A", 19, fmt_text)   # Fecha
            ws1.set_column("B:B", 14, fmt_text)   # Tienda
            ws1.set_column("C:C", 60, fmt_text)   # Producto
            ws1.set_column("D:D", 12, fmt_price)  # Precio

            # Hoja 2: Pivot por producto vs tienda
            pivot = df_excel.pivot_table(index="Producto", columns="Tienda", values="Precio", aggfunc="min")
            pivot = pivot.reset_index()
            pivot.to_excel(writer, sheet_name="Comparación", index=False)
            ws2 = writer.sheets["Comparación"]
            ws2.set_column(0, 0, 60, fmt_text)  # Producto
            # resto columnas como moneda
            for col_idx in range(1, pivot.shape[1]):
                ws2.set_column(col_idx, col_idx, 12, fmt_price)

            # resaltar el mínimo por fila (más barato)
            from xlsxwriter.utility import xl_col_to_name
            if pivot.shape[0] > 0 and pivot.shape[1] > 1:
                last_col_letter = xl_col_to_name(pivot.shape[1]-1)
                rng_data = f"B2:{last_col_letter}{pivot.shape[0]+1}"
                ws2.conditional_format(rng_data, {
                    "type": "formula",
                    "criteria": f'=B2=MIN($B2:${last_col_letter}2)',
                    "format": wb.add_format({"bg_color": "#C6EFCE", "font_color": "#006100"})
                })

        print(f"✨ Excel formateado -> {os.path.join(CARPETA, 'comparativo_precios.xlsx')}")
    except Exception as e:
        print(f"⚠️ No se pudo crear el Excel formateado (instala xlsxwriter con 'pip install xlsxwriter'). Detalle: {e}")

if __name__ == "__main__":
    main()
