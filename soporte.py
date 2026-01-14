import pandas as pd
import streamlit as st
from io import BytesIO

# =========================
# Configuración inicial
# =========================
st.set_page_config(
    page_title="Filtro de Análisis Tlaloc",
    layout="wide"
)

st.title("Filtro interactivo – Análisis Tlaloc")

# =========================
# 1. Subir archivo Excel
# =========================
archivo = st.file_uploader(
    "Sube el archivo Excel",
    type=["xlsx"]
)

if archivo is None:
    st.info("⬆️ Sube un archivo Excel para comenzar")
    st.stop()

# =========================
# 2. Leer Excel
# =========================
df = pd.read_excel(
    archivo,
    skiprows=2
)

# Limpieza defensiva
df.columns = (
    df.columns
    .astype(str)
    .str.strip()
    .str.replace("\n", " ")
)

# Columna ciclo (R)
df["_ciclo_R"] = df.iloc[:, 17]

# =========================
# 3. Filtros dinámicos
# =========================
st.sidebar.header("Filtros")

df_f = df.copy()

def filtro_multiselect(df, columna, etiqueta):
    opciones = sorted(df[columna].dropna().unique())
    seleccion = st.sidebar.multiselect(
        etiqueta,
        ["Todos"] + opciones,
        default=["Todos"]
    )
    if "Todos" not in seleccion:
        df = df[df[columna].isin(seleccion)]
    return df

df_f = filtro_multiselect(df_f, "Modalidad/Función", "Modalidad / Función")
df_f = filtro_multiselect(df_f, "Estado", "Estado")
df_f = filtro_multiselect(df_f, "Cultivo/Especie", "Cultivo / Especie")
df_f = filtro_multiselect(df_f, "_ciclo_R", "Ciclo")

# =========================
# 4. Resultados
# =========================
st.subheader("Resultados filtrados")
st.write(f"Registros encontrados: **{len(df_f)}**")

st.dataframe(df_f, use_container_width=True)

# =========================
# 5. Descargar Excel
# =========================
def convertir_excel(df):
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Resultados")
    buffer.seek(0)
    return buffer

st.download_button(
    label="📥 Descargar resultados en Excel",
    data=convertir_excel(df_f),
    file_name="resultados_tlaloc.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)


