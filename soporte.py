import pandas as pd
import streamlit as st

# =========================
# Configuración inicial
# =========================
st.set_page_config(page_title="Filtro de Análisis Tlaloc", layout="wide")

st.title("Filtro interactivo – Análisis Tlaloc")

# =========================
# 1. Leer el archivo Excel
# =========================
ruta_excel = "Analisis Tlaloc.xlsx"

df = pd.read_excel(
    ruta_excel,
    skiprows=2  # La fila 3 se convierte en encabezado
)

# Limpieza defensiva de columnas
df.columns = (
    df.columns
    .astype(str)
    .str.strip()
    .str.replace("\n", " ")
)

# Columna Ciclo de la columna R (índice 17)
df["_ciclo_R"] = df.iloc[:, 17]

# =========================
# 2. Filtros interactivos
# =========================
st.sidebar.header("Filtros")

filtro_modalidad = st.sidebar.selectbox(
    "Modalidad / Función",
    sorted(df["Modalidad/Función"].dropna().unique())
)

filtro_estado = st.sidebar.selectbox(
    "Estado",
    sorted(df["Estado"].dropna().unique())
)

filtro_cultivo = st.sidebar.selectbox(
    "Cultivo / Especie",
    sorted(df["Cultivo/Especie"].dropna().unique())
)

filtro_ciclo = st.sidebar.selectbox(
    "Ciclo",
    sorted(df["_ciclo_R"].dropna().unique())
)

# =========================
# 3. Aplicar filtros (AND)
# =========================
df_filtrado = df[
    (df["Modalidad/Función"] == filtro_modalidad) &
    (df["Estado"] == filtro_estado) &
    (df["Cultivo/Especie"] == filtro_cultivo) &
    (df["_ciclo_R"] == filtro_ciclo)
]

# =========================
# 4. Mostrar resultado
# =========================
st.subheader("Resultados filtrados")
st.write(f"Registros encontrados: {len(df_filtrado)}")
st.dataframe(df_filtrado, use_container_width=True)
