import pandas as pd
import streamlit as st

# =========================
# Configuración inicial
# =========================
st.set_page_config(page_title="Filtro dinámico – Análisis Tlaloc", layout="wide")
st.title("Filtro dinámico – Análisis Tlaloc")

# =========================
# Subir archivo Excel
# =========================
archivo = st.file_uploader(
    "Sube el archivo Excel",
    type=["xlsx"]
)

if archivo is not None:

    # =========================
    # Leer Excel
    # =========================
    df = pd.read_excel(archivo, skiprows=2)

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.replace("\n", " ")
    )

    # Columna Ciclo (R)
    df["_ciclo_R"] = df.iloc[:, 17]

    st.sidebar.header("Filtros")

    # =========================
    # FILTRO 1 – Modalidad
    # =========================
    opciones_modalidad = ["Todos"] + sorted(df["Modalidad/Función"].dropna().unique())
    modalidad = st.sidebar.multiselect(
        "Modalidad / Función",
        opciones_modalidad,
        default="Todos"
    )

    df_f = df if "Todos" in modalidad else df[df["Modalidad/Función"].isin(modalidad)]

    # =========================
    # FILTRO 2 – Estado
    # =========================
    opciones_estado = ["Todos"] + sorted(df_f["Estado"].dropna().unique())
    estado = st.sidebar.multiselect(
        "Estado",
        opciones_estado,
        default="Todos"
    )

    if "Todos" not in estado:
        df_f = df_f[df_f["Estado"].isin(estado)]

    # =========================
    # FILTRO 3 – Cultivo
    # =========================
    opciones_cultivo = ["Todos"] + sorted(df_f["Cultivo/Especie"].dropna().unique())
    cultivo = st.sidebar.multiselect(
        "Cultivo / Especie",
        opciones_cultivo,
        default="Todos"
    )

    if "Todos" not in cultivo:
        df_f = df_f[df_f["Cultivo/Especie"].isin(cultivo)]

    # =========================
    # FILTRO 4 – Ciclo
    # =========================
    opciones_ciclo = ["Todos"] + sorted(df_f["_ciclo_R"].dropna().unique())
    ciclo = st.sidebar.multiselect(
        "Ciclo",
        opciones_ciclo,
        default="Todos"
    )

    if "Todos" not in ciclo:
        df_f = df_f[df_f["_ciclo_R"].isin(ciclo)]

    # =========================
    # Resultados
    # =========================
    st.subheader("Resultados filtrados")
    st.write(f"Registros encontrados: {len(df_f)}")
    st.dataframe(df_f, use_container_width=True)

    # =========================
    # Botón de descarga
    # =========================
    @st.cache_data
    def convertir_excel(df):
        return df.to_excel(index=False)

    st.download_button(
        label="⬇️ Descargar resultados en Excel",
        data=convertir_excel(df_f),
        file_name="resultado_filtrado.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:
    st.info("⬆️ Sube un archivo Excel para comenzar.")

