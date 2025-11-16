import os
import time
import pandas as pd
import pywhatkit

# ===========================
# CONFIGURACIÓN GENERAL
# ===========================

# Carpeta del proyecto (donde están customers.xlsx y promo.jpg)
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# Archivos de entrada / salida
EXCEL_FILE = os.path.join(BASE_PATH, "customers.xlsx")
SHEET_NAME = "customers"

IMAGE_FILE = os.path.join(BASE_PATH, "promo.jpg")
OUTPUT_FILE = os.path.join(BASE_PATH, "customers_updated.xlsx")

# Nombre de la empresa para personalizar el mensaje
COMPANY_NAME = "Mi Empresa"

# Tiempo entre envíos (segundos)
SEND_DELAY_SECONDS = 25

# Si True, añade una nota de que es mensaje de prueba
TEST_MODE = True


def limpiar_telefono(raw):
    """
    Convierte el número a string, elimina espacios y guiones,
    y añade '+' si no lo tiene.
    """
    numero = str(raw).strip().replace(" ", "").replace("-", "")
    if not numero:
        return ""
    if not numero.startswith("+"):
        numero = "+" + numero
    return numero


def cargar_y_filtrar_clientes():
    """
    Carga el Excel de clientes y filtra solo los que deben recibir mensaje.
    Reglas:
      - SendFlag = 1
      - SentFlag != 1
    """
    df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME, dtype=str)

    # Normalizar flags
    for col in ["SendFlag", "SentFlag"]:
        if col not in df.columns:
            df[col] = "0"
        df[col] = df[col].fillna("0").astype(str).str.strip()

    mask = (df["SendFlag"].isin(["1", "1.0"])) & (~df["SentFlag"].isin(["1", "1.0"]))

    df_filtered = df[mask].copy()

    print("\n=== RESUMEN BASE DE CLIENTES ===")
    print("Total de filas:", len(df))
    print("Clientes a enviar:", len(df_filtered), "\n")

    if not df_filtered.empty:
        cols_preview = [
            c for c in ["Name", "Phone", "City", "Segment", "MessageLabel", "SendFlag", "SentFlag"]
            if c in df_filtered.columns
        ]
        print("Ejemplo de clientes filtrados:")
        print(df_filtered[cols_preview].head(), "\n")

    return df, df_filtered


def construir_mensaje(row):
    """
    Construye un mensaje genérico usando los atributos de la base de clientes.
    Usa:
      - MessageLabel (o Name como fallback)
      - City
      - Segment
      - COMPANY_NAME
    """
    name = str(row.get("Name", "")).strip()
    label = str(row.get("MessageLabel", "")).strip()
    city = str(row.get("City", "")).strip()
    segment = str(row.get("Segment", "")).strip()

    if not label:
        label = name if name else "cliente"

    city_text = f" de **{city}**" if city else ""
    segment_text = f" en el segmento **{segment}**" if segment else ""

    message = (
        f"Hola {label} 👋\n\n"
        f"Te saluda el equipo de **{COMPANY_NAME}**.\n\n"
        f"Queríamos contarte que tenemos una nueva promoción especial para clientes{city_text}{segment_text}.\n\n"
        "Si tienes dudas o quieres más información, puedes responder directamente a este mensaje "
        "y con gusto te ayudamos.\n"
    )

    if TEST_MODE:
        message += "\n_Mensaje automático de prueba_"

    return message


def enviar_mensajes():
    """
    Flujo principal:
      - Carga y filtra clientes
      - Recorre uno a uno
      - Envía una imagen + mensaje de WhatsApp con PyWhatKit
      - Marca SentFlag = 1
      - Guarda el Excel actualizado
    """
    print("\n⚠️ IMPORTANTE:")
    print("- Debes tener abierta una sesión activa de WhatsApp Web en tu navegador (Chrome recomendado).")
    print("- No uses la computadora mientras se envían los mensajes (el script controla el navegador).")
    print("- En macOS / Linux, CopyQ debe estar instalado y corriendo en segundo plano.\n")
    input("Cuando estés listo, presiona ENTER para comenzar...\n")

    df, df_filtered = cargar_y_filtrar_clientes()

    if df_filtered.empty:
        print("No hay clientes para enviar según los filtros (SendFlag=1 y SentFlag!=1).")
        return

    total = len(df_filtered)

    # Para pruebas: si quieres solo unos pocos, descomenta:
    # df_filtered = df_filtered.head(3)

    for idx, (i, row) in enumerate(df_filtered.iterrows(), start=1):
        raw_phone = row.get("Phone", "")
        phone = limpiar_telefono(raw_phone)

        if phone in ["+nan", "+None", "+", "+0"]:
            print(f"[{idx}/{total}] Número inválido ({raw_phone}). Se omite.")
            continue

        message = construir_mensaje(row)

        print(f"[{idx}/{total}] Enviando a {phone}")
        print("Mensaje (inicio):", message[:80], "...\n")

        try:
            pywhatkit.sendwhats_image(
                receiver=phone,
                img_path=IMAGE_FILE,
                caption=message,
                tab_close=True,
                close_time=2
            )

            # Marcar como enviado
            df.loc[i, "SentFlag"] = "1"

            time.sleep(SEND_DELAY_SECONDS)

        except Exception as e:
            print(f"⚠️ Error enviando a {phone}: {e}")
            continue

    print("\nGuardando archivo actualizado...")
    try:
        df.to_excel(OUTPUT_FILE, index=False)
        print("Archivo actualizado guardado en:", OUTPUT_FILE)
    except Exception as e:
        print("⚠️ Error al guardar el Excel actualizado:", e)


if __name__ == "__main__":
    enviar_mensajes()
