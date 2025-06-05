import streamlit as st
import pandas as pd
import pydeck as pdk
import base64

USERS = {"admin": "1234"}

st.set_page_config(page_title="Polaris Web", layout="centered")

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Asegúrate de que 'fondo.jpg' exista en el mismo directorio o proporciona la ruta completa.
try:
    img_base64 = get_base64_of_bin_file("fondo.jpg")
except FileNotFoundError:
    st.error("Error: 'fondo.jpg' no encontrado. Asegúrate de que la imagen esté en el mismo directorio que el script.")
    img_base64 = "" # Para evitar errores si la imagen no se encuentra

# --- Nuevo código para el logo ---
try:
    logo_base64 = get_base64_of_bin_file("adrlogo.png")
except FileNotFoundError:
    st.error("Error: 'adrlogo.png' no encontrado. Asegúrate de que el logo esté en el mismo directorio que el script.")
    logo_base64 = "" # Para evitar errores si la imagen no se encuentra

# --- Fin del nuevo código para el logo ---

st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/jpg;base64,{img_base64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    height: 100vh;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: white;
}}

/* Estilos para el logo */
.logo-container {{
    text-align: center;
    margin-top: 4rem;
    margin-bottom: 2rem;
}}

.logo-container img {{
    max-width: 250px; /* Ajusta esto al tamaño deseado para tu logo */
    height: auto;
    display: block;
    margin: 0 auto;
}}

h1 {{
    color: white;
    text-align: center;
    margin-top: 4rem;
    margin-bottom: 2rem;
}}

.stButton > button {{
    background-color: #1E90FF;
    color: white;
    font-weight: 700;
    font-size: 1.2rem;
    padding: 0.75rem;
    border-radius: 10px;
    border: none;
    width: 100%;
    cursor: pointer;
    transition: background-color 0.3s ease;
}}

.stButton > button:hover {{
    background-color: #1c7ed6;
}}

div.stTextInput > label {{
    font-weight: 600;
    font-size: 1rem;
    margin-bottom: 0.5rem;
    display: block;
    color: white;
}}

div.stTextInput > div > input {{
    width: 100% !important;
    padding: 0.75rem 1rem !important;
    margin-bottom: 1.5rem !important;
    border-radius: 10px !important;
    border: none !important;
    font-size: 1rem !important;
    outline: none !important;
    background-color: rgba(255, 255, 255, 0.25) !important;
    color: white !important;
}}

div.stTextInput > div > input::placeholder {{
    color: rgba(255, 255, 255, 0.7) !important;
}}

</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    # --- Cambio aquí: Sustituye st.title por st.markdown con el logo ---
    if logo_base64: # Solo muestra el logo si se cargó correctamente
        st.markdown(f"""
        <div class="logo-container">
            <img src="data:image/png;base64,{logo_base64}" alt="ADR Logo">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.title("Polaris Web") # Fallback si el logo no se carga
    # --- Fin del cambio ---

    usuario = st.text_input("Nombre de usuario", placeholder="Introduce tu usuario")
    contrasena = st.text_input("Contraseña", type="password", placeholder="Introduce tu contraseña")
    if st.button("Login"):
        if USERS.get(usuario) == contrasena:
            st.session_state.logged_in = True
            st.success("Sesión iniciada correctamente.")
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos.")

def dashboard():
    st.sidebar.title("Menú")
    opcion = st.sidebar.radio("Ir a", ["Inicio", "Mapa", "Gráficos", "Cerrar sesión"])

    if opcion == "Inicio":
        st.title("Sistema de Monitoreo Ambiental")
        st.markdown("Bienvenido a Polaris Web, visualiza y analiza datos ambientales en tiempo real.")
    elif opcion == "Mapa":
        st.subheader("Estaciones en Mapa")
        try:
            df = pd.read_csv("estaciones.csv")
            st.pydeck_chart(pdk.Deck(
                map_style='mapbox://styles/mapbox/light-v9',
                initial_view_state=pdk.ViewState(
                    latitude=df["lat"].mean(),
                    longitude=df["lon"].mean(),
                    zoom=6,
                    pitch=50,
                ),
                layers=[
                    pdk.Layer(
                        'ScatterplotLayer',
                        data=df,
                        get_position='[lon, lat]',
                        get_color='[0, 112, 255, 160]',
                        get_radius=2500,
                    ),
                ],
            ))
        except FileNotFoundError:
            st.error("Error: 'estaciones.csv' no encontrado. No se puede cargar el mapa.")
    elif opcion == "Gráficos":
        st.subheader("Temperatura y Precipitación")
        try:
            df = pd.read_csv("estaciones.csv")
            st.line_chart(df[["temperatura", "precipitacion"]])
        except FileNotFoundError:
            st.error("Error: 'estaciones.csv' no encontrado. No se pueden generar los gráficos.")
    elif opcion == "Cerrar sesión":
        st.session_state.logged_in = False
        st.rerun()

if st.session_state.logged_in:
    dashboard()
else:
    login()
                     
