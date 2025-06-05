import streamlit as st
import pandas as pd
import pydeck as pdk
import base64

# Usuarios para login
USERS = {"admin": "1234"}

st.set_page_config(page_title="Polaris Web", layout="centered")

# Carga imagen y la convierte a base64 para usar en CSS
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_base64 = get_base64_of_bin_file("fondo.jpg")

# Estilos CSS para fondo y cuadro de login
st.markdown(f"""
<style>
/* Fondo de toda la página */
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/jpg;base64,{img_base64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    height: 100vh;
    font-family: 'Roboto', sans-serif;
}}

/* Cuadro oscuro centrado */
.login-box {{
    background-color: rgba(0, 0, 0, 0.75);
    padding: 2.5rem 2rem;
    border-radius: 15px;
    box-shadow: 0 0 20px rgba(0,0,0,0.6);
    color: white;
    max-width: 400px;
    margin: 0 auto;
    text-align: center;
}}

/* Título */
.login-box h1 {{
    color: #1E90FF;
    font-weight: 700;
    margin-bottom: 2rem;
}}

/* Inputs */
div.stTextInput > label {{
    display: none;
}}

div.stTextInput > div > input {{
    width: 100% !important;
    padding: 0.75rem 1rem !important;
    margin-bottom: 1.2rem !important;
    border-radius: 8px !important;
    border: none !important;
    font-size: 1rem !important;
    outline: none !important;
    box-shadow: none !important;
    transition: box-shadow 0.3s ease !important;
}}

div.stTextInput > div > input:focus {{
    box-shadow: 0 0 8px 2px #1E90FF !important;
}}

/* Botón */
div.stButton > button {{
    width: 100% !important;
    padding: 0.75rem 1rem !important;
    background-color: #1E90FF !important;
    border: none !important;
    border-radius: 8px !important;
    color: white !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    cursor: pointer !important;
    transition: background-color 0.3s ease !important;
}}

div.stButton > button:hover {{
    background-color: #1c7ed6 !important;
}}
</style>
""", unsafe_allow_html=True)

def login():
    # Centramos verticalmente usando columnas vacías a izquierda y derecha
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Usamos un contenedor con clase login-box para el cuadro oscuro
        st.markdown('<div class="login-box">', unsafe_allow_html=True)

        st.markdown("<h1>Polaris Web</h1>", unsafe_allow_html=True)

        usuario = st.text_input("Usuario", key="user")
        contrasena = st.text_input("Contraseña", type="password", key="pwd")
        boton = st.button("Iniciar sesión")

        if boton:
            if USERS.get(usuario) == contrasena:
                st.session_state.logged_in = True
                st.success("Sesión iniciada correctamente.")
                st.experimental_rerun()
            else:
                st.error("Usuario o contraseña incorrectos.")

        st.markdown("</div>", unsafe_allow_html=True)

def dashboard():
    st.sidebar.title("Menú")
    opcion = st.sidebar.radio("Ir a", ["Inicio", "Mapa", "Gráficos", "Cerrar sesión"])

    if opcion == "Inicio":
        st.title("Sistema de Monitoreo Ambiental")
        st.markdown("Bienvenido a Polaris Web, visualiza y analiza datos ambientales en tiempo real.")
    elif opcion == "Mapa":
        st.subheader("Estaciones en Mapa")
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
    elif opcion == "Gráficos":
        st.subheader("Temperatura y Precipitación")
        df = pd.read_csv("estaciones.csv")
        st.line_chart(df[["temperatura", "precipitacion"]])
    elif opcion == "Cerrar sesión":
        st.session_state.logged_in = False
        st.experimental_rerun()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    dashboard()
else:
    login()
