import streamlit as st
import pandas as pd
from database.api_futbol import obtener_partidos
import weasyprint

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
st.write("Aquí irá el contenido principal de la app.")

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

        # Función para exportar a PDF
        def exportar_a_pdf(df_partidos):
            html_content = df_partidos.to_html()  # Convertir el DataFrame en HTML
            pdf = weasyprint.HTML(string=html_content).write_pdf()  # Convertir HTML a PDF
            
            # Guardar el archivo PDF en la carpeta del proyecto
            with open("partidos.pdf", "wb") as f:
                f.write(pdf)

            st.success("PDF generado correctamente. Haz clic para descargar.")
            st.download_button(
                label="Descargar PDF",
                data=pdf,
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

