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
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    body, html {{
        margin: 0; padding: 0; height: 100%;
        font-family: 'Roboto', sans-serif;
    }}

    .login-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh;
        background-image: url("data:image/jpg;base64,{img_base64}");
        background-size: cover;
        background-position: center;
    }}

    .login-box {{
        background-color: rgba(0, 0, 0, 0.7); /* Fondo oscuro semitransparente */
        padding: 3rem 2.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5);
        text-align: center;
        width: 100%;
        max-width: 400px;
        color: #ffffff;
    }}

    .login-box h1 {{
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 1.5rem;
        color: #1E90FF; /* Azul brillante */
        letter-spacing: 1.2px;
    }}

    /* Inputs personalizados */
    .login-box input[type="text"],
    .login-box input[type="password"] {{
        width: 100%;
        padding: 0.75rem 1rem;
        margin-bottom: 1.2rem;
        border: none;
        border-radius: 8px;
        font-size: 1rem;
        outline: none;
        transition: box-shadow 0.3s ease;
    }}

    .login-box input[type="text"]:focus,
    .login-box input[type="password"]:focus {{
        box-shadow: 0 0 8px 2px #1E90FF;
    }}

    /* Botón moderno */
    .login-box button {{
        width: 100%;
        padding: 0.75rem 1rem;
        background-color: #1E90FF;
        border: none;
        border-radius: 8px;
        color: white;
        font-weight: 700;
        font-size: 1.1rem;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }}

    .login-box button:hover {{
        background-color: #1c7ed6;
    }}

    /* Mensajes */
    .stSuccess, .stError {{
        margin-top: 1rem;
        font-weight: 600;
        font-size: 1rem;
    }}
    </style>
""", unsafe_allow_html=True)

def login():
    st.markdown('<div class="login-container"><div class="login-box">', unsafe_allow_html=True)
    st.markdown('<h1>Polaris Web</h1>', unsafe_allow_html=True)

    user = st.text_input("", placeholder="Usuario")
    pwd = st.text_input("", placeholder="Contraseña", type="password")
    login_btn = st.button("Iniciar sesión")

    if login_btn:
        if USERS.get(user) == pwd:
            st.session_state.logged_in = True
            st.success("Sesión iniciada correctamente.")
        else:
            st.error("Usuario o contraseña incorrectos.")
    st.markdown('</div></div>', unsafe_allow_html=True)

    if st.session_state.get("logged_in", False):
        st.experimental_rerun()

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
