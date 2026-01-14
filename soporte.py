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
    # Leer el archivo Excel
    # =========================
    df = pd.read_excel(archivo, skiprows=2)

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.replace("\n", " ")
    )

    # Columna Ciclo (columna R)
    df["_ciclo_R"] = df.iloc[:, 17]

    # =========================
    # FILTRO 1 – Modalidad
    # =========================
    st.sidebar.header("Filtros")

    modalidades = sorted(df["Modalidad/Función"].dropna().unique())
    filtro_modalidad = st.sidebar.selectbox(
        "Modalidad / Función",
        modalidades
    )

    df_m = df[df["Modalidad/Función"] == filtro_modalidad]

    # =========================
    # FILTRO 2 – Estado
    # =========================
    estados = sorted(df_m["Estado"].dropna().unique())
    filtro_estado = st.sidebar.selectbox(
        "Estado",
        estados
    )

    df_me = df_m[df_m["Estado"] == filtro_estado]

    # =========================
    # FILTRO 3 – Cultivo
    # =========================
    cultivos = sorted(df_me["Cultivo/Especie"].dropna().unique())
    filtro_cultivo = st.sidebar.selectbox(
        "Cultivo / Especie",
        cultivos
    )

    df_mec = df_me[df_me["Cultivo/Especie"] == filtro_cultivo]

    # =========================
    # FILTRO 4 – Ciclo
    # =========================
    ciclos = sorted(df_mec["_ciclo_R"].dropna().unique())
    filtro_ciclo = st.sidebar.selectbox(
        "Ciclo",
        ciclos
    )

    df_filtrado = df_mec[df_mec["_ciclo_R"] == filtro_ciclo]

    # =========================
    # Resultados
    # =========================
    st.subheader("Resultados filtrados")
    st.write(f"Registros encontrados: {len(df_filtrado)}")
    st.dataframe(df_filtrado, use_container_width=True)

else:
    st.info("⬆️ Sube un archivo Excel para comenzar.")

