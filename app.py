# Polaris Web App Mejorada

import streamlit as st
import pandas as pd
import pydeck as pdk
import base64
import plotly.express as px
import datetime
import requests  # Para futuras APIs

USERS = {"admin": "1234"}

st.set_page_config(page_title="Polaris Web", layout="wide")

# Estilos visuales modernos
st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] {
            background-color: #0F172A;
            color: white;
        }
        [data-testid="stSidebar"] {
            background-color: #1E293B;
            color: white;
        }
        .stButton > button {
            background-color: #1E3A8A;
            color: white;
            border-radius: 10px;
        }
        .stButton > button:hover {
            background-color: #2563EB;
        }
    </style>
""", unsafe_allow_html=True)

# Login y sesiones
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Autenticación básica
def login():
    st.title("Polaris Web")
    user = st.text_input("Usuario")
    pwd = st.text_input("Contraseña", type="password")
    if st.button("Ingresar"):
        if USERS.get(user) == pwd:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Credenciales inválidas")

# Herramientas para el Tablero
def tablero():
    st.title("🏠 Tablero de Control")
    st.metric("Estaciones Activas", 18, "+2")
    st.metric("Precipitaciones 24h", "35 mm")

    # Precipitación por hora
    data = pd.DataFrame({
        "Hora": pd.date_range(end=datetime.datetime.now(), periods=24, freq='h'),
        "mm": [i % 5 + i * 0.2 for i in range(24)]
    })
    st.plotly_chart(px.area(data, x="Hora", y="mm", title="Lluvia Horaria"))

    # Top 5 estaciones con más lluvia
    top5 = pd.DataFrame({
        "Estación": [f"Estación {i}" for i in range(5)],
        "mm": [30, 28, 24, 22, 21]
    })
    st.bar_chart(top5.set_index("Estación"))

# GIS con superposición
@st.cache_data

def load_geojson():
    return requests.get("https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json").json()

def gis():
    st.title("🌐 GIS")
    geojson = load_geojson()
    st.map()  # Puedes usar st.pydeck_chart con pdk.Layer para capas avanzadas
    st.json(geojson, expanded=False)

# Mapa con filtros

def mapa():
    st.title("🗺️ Mapa GIS")
    df = pd.DataFrame({
        "lat": [40.4, 40.5],
        "lon": [-3.7, -3.6],
        "nombre": ["Estación A", "Estación B"],
        "estado": ["activa", "inactiva"]
    })
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v10',
        initial_view_state=pdk.ViewState(latitude=40.4, longitude=-3.7, zoom=6),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=df,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=2000,
            )
        ]
    ))

# Visor con selector y exportación

def visor():
    st.title("📊 Visor")
    fechas = st.date_input("Rango de fechas", [datetime.date.today() - datetime.timedelta(days=7), datetime.date.today()])
    estacion = st.selectbox("Estación", ["A", "B"])
    var = st.selectbox("Variable", ["Temp", "Precip"])  

    datos = pd.DataFrame({
        "Fecha": pd.date_range(start=fechas[0], end=fechas[1], freq='D'),
        var: [20 + i for i in range((fechas[1] - fechas[0]).days + 1)]
    })
    fig = px.line(datos, x="Fecha", y=var, title=f"{var} - Estación {estacion}")
    st.plotly_chart(fig)
    st.download_button("Descargar CSV", data=datos.to_csv().encode(), file_name="datos.csv")

# Menú lateral

def menu():
    secciones = ["Tablero", "GIS", "Mapa GIS", "Visor", "Cerrar sesión"]
    opcion = st.sidebar.radio("Navegación", secciones)
    if opcion == "Tablero":
        tablero()
    elif opcion == "GIS":
        gis()
    elif opcion == "Mapa GIS":
        mapa()
    elif opcion == "Visor":
        visor()
    elif opcion == "Cerrar sesión":
        st.session_state.logged_in = False
        st.rerun()

if st.session_state.logged_in:
    menu()
else:
    login()
