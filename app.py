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

img_base64 = get_base64_of_bin_file("fondo.jpg")

st.markdown(f"""
<style>
/* Fondo y centrado total */
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/jpg;base64,{img_base64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    height: 100vh;
    font-family: 'Roboto', sans-serif;
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
}}

/* Caja negra centrada con transparencia */
.login-box {{
    background-color: rgba(0, 0, 0, 0.75);
    padding: 3rem 2.5rem;
    border-radius: 15px;
    box-shadow: 0 0 25px rgba(0,0,0,0.6);
    max-width: 400px;
    width: 90vw;
    text-align: center;
}}

/* Título dentro de la caja */
.login-box h1 {{
    color: white;
    font-weight: 700;
    margin-bottom: 2.5rem;
    font-size: 2.4rem;
}}

/* Labels */
div.stTextInput > label {{
    font-weight: 600;
    font-size: 1rem;
    margin-bottom: 0.5rem;
    display: block;
    color: white;
}}

/* Inputs */
div.stTextInput > div > input {{
    width: 100% !important;
    padding: 0.75rem 1rem !important;
    margin-bottom: 1.5rem !important;
    border-radius: 8px !important;
    border: none !important;
    font-size: 1rem !important;
    outline: none !important;
    box-shadow: none !important;
    transition: box-shadow 0.3s ease !important;
}}

/* Input focus */
div.stTextInput > div > input:focus {{
    box-shadow: 0 0 8px 2px #1E90FF !important;
}}

/* Botón con texto visible */
div.stButton > button {{
    width: 100% !important;
    padding: 0.8rem 1rem !important;
    background-color: #1E90FF !important;
    border: none !important;
    border-radius: 8px !important;
    color: white !important;  /* Aseguramos color blanco */
    font-weight: 700 !important;
    font-size: 1.2rem !important;
    cursor: pointer !important;
    transition: background-color 0.3s ease !important;
}}

div.stButton > button:hover {{
    background-color: #1c7ed6 !important;
}}
</style>
""", unsafe_allow_html=True)


def login():
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown("<h1>Polaris Web</h1>", unsafe_allow_html=True)

    with st.form(key="login_form"):
        usuario = st.text_input("Nombre de usuario")
        contrasena = st.text_input("Contraseña", type="password")
        submit_btn = st.form_submit_button("Login")

        if submit_btn:
            if USERS.get(usuario) == contrasena:
                st.session_state.logged_in = True
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


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    dashboard()
else:
    login()
