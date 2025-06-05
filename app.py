import streamlit as st
import pandas as pd
import pydeck as pdk

# Simulación de usuarios
USERS = {"admin": "1234"}

st.set_page_config(page_title="Polaris Web", layout="centered")

# CSS para diseño visual moderno
st.markdown("""
    <style>
    .login-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 90vh;
        background-image: url('fondo.jpg');
        background-size: cover;
        background-position: center;
    }
    .login-box {
        background-color: rgba(255, 255, 255, 0.92);
        padding: 3rem 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        text-align: center;
        width: 100%;
        max-width: 400px;
    }
    .login-box h1 {
        color: #1E90FF;
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

def login():
    st.markdown('<div class="login-container"><div class="login-box">', unsafe_allow_html=True)
    st.markdown('<h1>Polaris Web</h1>', unsafe_allow_html=True)
    user = st.text_input("Usuario")
    pwd = st.text_input("Contraseña", type="password")
    if st.button("Iniciar sesión"):
        if USERS.get(user) == pwd:
            st.session_state.logged_in = True
            st.success("Sesión iniciada correctamente.")
            st.experimental_rerun()
        else:
            st.error("Usuario o contraseña incorrectos.")
    st.markdown('</div></div>', unsafe_allow_html=True)

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
