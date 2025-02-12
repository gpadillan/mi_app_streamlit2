import streamlit as st
import pandas as pd
import requests  
from fpdf import FPDF

# Configurar la página
st.set_page_config(page_title="Mi Aplicación Streamlit", layout="centered")

# Estado de sesión para autenticación
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def login():
    st.title("🔒 Iniciar Sesión")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Login"):
        if username == "admin" and password == "admin":
            st.session_state.authenticated = True
            st.success("Inicio de sesión exitoso")
            st.rerun()
        else:
            st.error("Credenciales incorrectas")

if not st.session_state.authenticated:
    login()
    st.stop()

st.sidebar.success("✅ Sesión iniciada")
st.title("🎉 Bienvenido a la Aplicación")
st.write("¡Bienvenido a la aplicación de fútbol! Selecciona una competición para ver los partidos.")

# Mapa de competiciones y sus códigos
competicion_codes = {
    "Premier League": "PL",
    "LaLiga": "PD",  # Código para LaLiga (Primera Division)
    "Serie A": "SA",  # Código para Serie A
    "Bundesliga": "BL1",  # Código para Bundesliga
    "Ligue 1": "FL1",  # Código para Ligue 1
    "FIFA World Cup": "WC",  # Código para la Copa del Mundo
    "UEFA Champions League": "CL",  # Código para la Champions League
    "Eredivisie": "DED",  # Código para Eredivisie
    "Campeonato Brasileiro Série A": "BSA",  # Código para Brasileirão
    "Copa Libertadores": "CLI",  # Código para Copa Libertadores
    "European Championship": "EC",  # Código para Eurocopa
    "Primeira Liga": "PPL",  # Código para Primeira Liga
    "Championship": "ELC"  # Código para Championship
}

# Selección de competición
competicion = st.sidebar.selectbox("Selecciona la competición:", list(competicion_codes.keys()))

# Mostrar los partidos de la competición seleccionada
st.write(f"📅 Partidos de la {competicion}")
competicion_code = competicion_codes.get(competicion)

@st.cache_data
def obtener_partidos(competicion="PL"):
    url = f"https://api.football-data.org/v4/competitions/{competicion}/matches"
    headers = {"X-Auth-Token": "2237852967a142e9ad6302f2ed07c45f"}  # Asegúrate de poner tu API key aquí
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # Devuelve los datos en formato JSON
    else:
        st.error(f"Error {response.status_code}: {response.text}")
        return None

if competicion_code:
    datos = obtener_partidos(competicion=competicion_code)

    if datos and "matches" in datos:
        partidos_lista = []
        for partido in datos["matches"]:
            partidos_lista.append({
                "Fecha": partido["utcDate"],
                "Local": partido["homeTeam"]["name"],
                "Visitante": partido["awayTeam"]["name"]
            })

        df_partidos = pd.DataFrame(partidos_lista)
        st.dataframe(df_partidos)

        # Función para exportar a PDF con fpdf
        def exportar_a_pdf(df_partidos):
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()

            pdf.set_font("Arial", size=12)

            # Título
            pdf.cell(200, 10, txt="Partidos de Fútbol", ln=True, align="C")

            # Añadir los datos de la tabla
            for index, row in df_partidos.iterrows():
                pdf.cell(200, 10, txt=f"{row['Fecha']} - {row['Local']} vs {row['Visitante']}", ln=True)

            # Guardar el PDF
            pdf.output("partidos.pdf")

            st.success("PDF generado correctamente. Haz clic para descargar.")
            st.download_button(
                label="Descargar PDF",
                data=open("partidos.pdf", "rb").read(),
                file_name="partidos.pdf",
                mime="application/pdf"
            )

        # Añadir el botón de exportar a PDF
        if st.button("Exportar a PDF"):
            exportar_a_pdf(df_partidos)

        # Botón para imprimir la página
        if st.button("Imprimir la página"):
            js_code = """
                window.print();
            """
            st.components.v1.html(f'<script>{js_code}</script>', height=0, width=0)

    else:
        st.error("No se pudieron obtener los datos de los partidos.")
else:
    st.error("Competición no válida.")

if st.sidebar.button("Cerrar Sesión"):
    st.session_state.authenticated = False
    st.rerun()
