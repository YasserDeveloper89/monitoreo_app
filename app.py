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

# CSS global para la app
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    body, html {{
        margin: 0; padding: 0; height: 100%;
        font-family: 'Roboto', sans-serif;
    }}

    .login-page {{
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        background-image: url("data:image/jpg;base64,{img_base64}");
        background-size: cover;
        background-position: center;
    }}

    /* Este es el contenedor que envolverá todo el login */
    .login-box {{
        background-color: rgba(0, 0, 0, 0.7);
        padding: 3rem 2.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5);
        width: 400px;
        color: white;
        text-align: center;
    }}

    .login-box h1 {{
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 1.5rem;
        color: #1E90FF;
        letter-spacing: 1.2px;
    }}

    /* Inputs */
    div.stTextInput > label {{
        display: none;  /* ocultar etiquetas nativas para personalizar */
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

    /* Mensajes de éxito o error */
    .stSuccess, .stError {{
        margin-top: 1rem;
        font-weight: 600;
        font-size: 1rem;
    }}
    </style>
""", unsafe_allow_html=True)

def login():
    # Crear un contenedor con la clase login-page para fondo + centrado
    with st.container():
        st.markdown('<div class="login-page">', unsafe_allow_html=True)

        # Dentro, otro div para el cuadro oscuro
        st.markdown('<div class="login-box">', unsafe_allow_html=True)

        st.markdown('<h1>Polaris Web</h1>', unsafe_allow_html=True)

        user = st.text_input("Usuario", key="user_input")
        pwd = st.text_input("Contraseña", type="password", key="pwd_input")
        login_btn = st.button("Iniciar sesión", key="login_btn")

        if login_btn:
            if USERS.get(user) == pwd:
                st.session_state.logged_in = True
                st.success("Sesión iniciada correctamente.")
            else:
                st.error("Usuario o contraseña incorrectos.")

        st.markdown('</div>', unsafe_allow_html=True)  # cerrar login-box
        st.markdown('</div>', unsafe_allow_html=True)  # cerrar login-page

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
