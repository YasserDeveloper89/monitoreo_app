import streamlit as st
import pandas as pd
import pydeck as pdk
import base64
import re
from datetime import datetime, timedelta
import random # Necesario para generar datos de ejemplo

USERS = {"admin": "1234"}

st.set_page_config(page_title="ADR Web", layout="centered")

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

try:
    img_base64 = get_base64_of_bin_file("fondo.jpg")
except FileNotFoundError:
    st.error("Error: 'fondo.jpg' no encontrado. Asegúrate de que la imagen esté en el mismo directorio que el script.")
    img_base64 = ""

try:
    logo_base64 = get_base64_of_bin_file("adrlogo.png")
except FileNotFoundError:
    st.error("Error: 'adrlogo.png' no encontrado. Asegúrate de que el logo esté en el mismo directorio que el script.")
    logo_base64 = ""

st.markdown(f"""
<style>
/* Base container for the app view */
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/jpg;base64,{img_base64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    height: 100vh;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: white !important; /* ¡CAMBIADO AQUI! */
}}

/* Logo container styles */
.logo-container {{
    text-align: center;
    margin-top: 4rem;
    margin-bottom: 2rem;
}}

.logo-container img {{
    max-width: 250px;
    height: auto;
    display: block;
    margin: 0 auto;
}}

/* General H1 styles */
h1 {{
    color: white;
    text-align: center;
    margin-top: 4rem;
    margin-bottom: 2rem;
}}

/* Button styles */
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

/* Text input label styles */
div.stTextInput > label {{
    font-weight: 600;
    font-size: 1rem;
    margin-bottom: 0.5rem;
    display: block;
    color: white;
}}

/* Text input field styles */
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

/* --- REVISED AND MORE AGGRESSIVE STYLES FOR THE SIDEBAR MENU --- */

/* Overall sidebar background and spacing */
[data-testid="stSidebar"] {{
    background-color: #1A2437; /* Dark background */
    color: white;
    padding-top: 20px;
    padding-left: 0px;
    padding-right: 0px;
}}

/* Title in the sidebar */
[data-testid="stSidebar"] h1 {{
    color: white;
    text-align: left;
    margin-bottom: 1.5rem;
    font-size: 1.8rem;
    padding: 0 20px;
}}

/* Ensure the radio group container fills the width */
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {{
    width: 100%;
    padding: 0;
}}

/* Each radio option label (the clickable area) */
[data-testid="stSidebar"] .stRadio label {{
    font-size: 1rem;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.7) !important; /* Slightly faded white for unselected */
    padding: 12px 20px !important; /* Increased padding for better click area */
    margin-bottom: 0px !important; /* Remove space between items */
    border-radius: 0px !important; /* Sharp corners like the example */
    transition: background-color 0.2s ease, color 0.2s ease;
    display: flex !important; /* Use flexbox for icon/text alignment */
    align-items: center !important;
    width: 100% !important; /* Ensure it takes full width */
}}

/* Hover state for menu options */
[data-testid="stSidebar"] .stRadio label:hover {{
    background-color: #2D3E5E !important; /* Lighter background on hover */
    color: white !important; /* Pure white text on hover */
    cursor: pointer !important;
}}

/* Selected (active) state for menu options */
[data-testid="stSidebar"] .stRadio label[data-baseweb="radio"][aria-checked="true"] {{
    background-color: #0E1629 !important; /* Darker background for selected item */
    color: white !important; /* Pure white text for selected item */
    font-weight: 600 !important; /* Slightly bolder */
}}

/* This is the key to remove the native radio bullet point/circle */
/* Target the div that contains the actual radio input element */
[data-testid="stSidebar"] .stRadio label > div:first-child {{
    display: none !important;
}}

/* If using markdown in label (for emojis/icons), ensure it's aligned */
[data-testid="stSidebar"] .stRadio label > div[data-testid="stMarkdownContainer"] {{
    display: flex;
    align-items: center;
    gap: 10px; /* Space between icon and text */
}}

/* --- NEW / UPDATED STYLES FOR GIS MAP CONTROLS --- */

/* Style for selectbox labels */
div.stSelectbox > label {{
    font-weight: 600;
    font-size: 1rem;
    margin-bottom: 0.5rem;
    display: block;
    color: white; /* White label text */
}}

/* Style for selectbox dropdown input area */
.stSelectbox [data-testid="stSelectboxProcessedOptions"] {{
    background-color: rgba(255, 255, 255, 0.15) !important; /* Semi-transparent dark background */
    border-radius: 8px !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    color: white !important;
    padding: 0.5rem 1rem !important;
    font-size: 1rem !important;
}}

/* Style for selectbox options in dropdown */
.stSelectbox ul {{
    background-color: #2D3E5E !important; /* Darker background for dropdown options */
    color: white !important;
    border-radius: 8px;
}}

.stSelectbox li:hover {{
    background-color: #1A2437 !important; /* Slightly darker on hover */
    color: white !important;
}}

.stSelectbox li[aria-selected="true"] {{
    background-color: #1E90FF !important; /* Blue for selected option */
    color: white !important;
}}

/* Style for the button with the filter icon */
.stButton[data-testid="baseButton-secondary"] > button {{
    background-color: #1E90FF !important; /* Blue background */
    color: white !important;
    font-weight: 700;
    font-size: 1.2rem;
    padding: 0.75rem 1rem !important; /* Adjusted padding */
    border-radius: 10px !important;
    border: none !important;
    width: auto !important; /* Auto width for the icon button */
    min-width: 50px; /* Minimum width for the button */
    cursor: pointer;
    transition: background-color 0.3s ease;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 38px; /* Match height of selectbox for alignment */
    margin-top: 1.5rem; /* Align with selectboxes above */
}}

.stButton[data-testid="baseButton-secondary"] > button:hover {{
    background-color: #1c7ed6 !important;
}}

/* Adjust margins for column layout in GIS Map - Streamlit sometimes adds extra space */
.st-emotion-cache-1jm692t, .st-emotion-cache-1jm692t > div {{
    margin-bottom: 0 !important;
    padding-bottom: 0 !important;
}}
.st-emotion-cache-1c7y2vl {{ /* This targets the columns internal padding */
    padding-bottom: 0px !important;
}}

/* Specific adjustments for the PyDeck map container itself */
.stDeckGlJsonChart {{
    border-radius: 10px; /* Rounded corners for the map */
    overflow: hidden; /* Ensures corners are respected */
    margin-top: 1rem; /* Space between controls and map */
}}

</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    if logo_base64:
        st.markdown(f"""
        <div class="logo-container">
            <img src="data:image/png;base64,{logo_base64}" alt="ADR Logo">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.title("Polaris Web")

    usuario = st.text_input("Nombre de usuario", placeholder="Introduce tu usuario")
    contrasena = st.text_input("Contraseña", type="password", placeholder="Introduce tu contraseña")
    if st.button("Login"):
        if USERS.get(usuario) == contrasena:
            st.session_state.logged_in = True
            st.session_state.menu_selection = "Tablero"
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos.")

def dashboard():
    menu_options = [
        "Tablero",
        "GIS",
        "Mapa GIS",
        "Visor",
        "Fast Viewer",
        "Estaciones",
        "Monitoring",
        "Informe personalizado",
        "Informe rosa de los vientos",
        "Consecutive Rains",
        "Vistas",
        "Sinóptico",
        "Sinópticos",
        "Custom Synoptics",
        "Supervisor",
        "Estadísticas de red",
        "Registros",
        "Módulos",
        "Túnel",
        "Validador",
        "Cerrar sesión"
    ]

    if "menu_selection" not in st.session_state or st.session_state.menu_selection not in menu_options:
        st.session_state.menu_selection = menu_options[0]

    st.sidebar.title("Menú Principal")

    display_options = []
    for opt in menu_options:
        if opt == "Tablero": display_options.append("🏠 Tablero")
        elif opt == "GIS": display_options.append("🌐 GIS")
        elif opt == "Mapa GIS": display_options.append("🗺️ Mapa GIS")
        elif opt == "Visor": display_options.append("📊 Visor")
        elif opt == "Fast Viewer": display_options.append("⚡ Fast Viewer")
        elif opt == "Estaciones": display_options.append("📡 Estaciones")
        elif opt == "Monitoring": display_options.append("📈 Monitoring")
        elif opt == "Informe personalizado": display_options.append("📄 Informe personalizado")
        elif opt == "Informe rosa de los vientos": display_options.append("💨 Informe rosa de los vientos")
        elif opt == "Consecutive Rains": display_options.append("🌧️ Consecutive Rains")
        elif opt == "Vistas": display_options.append("👁️ Vistas")
        elif opt == "Sinóptico": display_options.append("🗺️ Sinóptico")
        elif opt == "Sinópticos": display_options.append("🗺️ Sinópticos")
        elif opt == "Custom Synoptics": display_options.append("⚙️ Custom Synoptics")
        elif opt == "Supervisor": display_options.append("🧑‍💻 Supervisor")
        elif opt == "Estadísticas de red": display_options.append("📊 Estadísticas de red")
        elif opt == "Registros": display_options.append("📜 Registros")
        elif opt == "Módulos": display_options.append("📦 Módulos")
        elif opt == "Túnel": display_options.append("🔗 Túnel")
        elif opt == "Validador": display_options.append("✅ Validador")
        elif opt == "Cerrar sesión": display_options.append("🚪 Cerrar sesión")
        else: display_options.append(opt)

    current_selected_display_option = st.session_state.menu_selection
    for opt in display_options:
        if re.sub(r'^\S+\s+', '', opt) == st.session_state.menu_selection:
            current_selected_display_option = opt
            break

    selected_index = display_options.index(current_selected_display_option)

    selected_option_display = st.sidebar.radio(
        "Navegación",
        options=display_options,
        index=selected_index,
        key="main_menu_radio",
        label_visibility="collapsed"
    )

    actual_selected_option = re.sub(r'^\S+\s+', '', selected_option_display)

    if actual_selected_option != st.session_state.menu_selection:
        st.session_state.menu_selection = actual_selected_option
        st.rerun()

    # --- Contenido principal basado en la selección del menú ---
    elif st.session_state.menu_selection == "Tablero":
        st.title("Tablero de Control")
        st.write("Bienvenido al tablero principal. Aquí podrás ver un resumen de los datos más importantes.")

        st.subheader("Estado General del Sistema")
        col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
        with col_kpi1:
            st.metric("Estaciones Operativas", "45/50", "90%")
        with col_kpi2:
            st.metric("Última Actualización", "Hace 5 minutos")
        with col_kpi3:
            st.metric("Datos Recibidos (24h)", "12,345")

        st.subheader("Precipitación Últimas 24 Horas")
        # Generar datos de ejemplo para el gráfico
        horas = [f"{i:02d}:00" for i in range(24)]
        precipitacion_ejemplo = [random.randint(0, 15) for _ in range(24)]
        df_precipitacion = pd.DataFrame({
            'Hora': horas,
            'Precipitación (mm)': precipitacion_ejemplo
        })
        st.line_chart(df_precipitacion.set_index('Hora'))

        st.subheader("Alertas Recientes")
        st.info("No hay alertas críticas en este momento.")
        st.warning("Estación Río Claro (ID: 105) con baja conectividad desde las 10:30 AM.")

    elif st.session_state.menu_selection == "GIS":
        st.title("Información Geográfica del Sistema")
        st.write("Explora y analiza datos geoespaciales relevantes para tus estaciones.")

        st.subheader("Gestión de Capas Geográficas")
        st.checkbox("Mostrar límites administrativos", value=True)
        st.checkbox("Mostrar zonas de exclusión")
        st.checkbox("Mostrar topografía")

        st.subheader("Herramientas de Análisis GIS")
        st.button("Calcular Distancias entre Estaciones")
        st.button("Análisis de Cobertura de Señal")
        st.button("Exportar Datos GeoJSON")

        st.info("Para visualizar las estaciones en un mapa interactivo, dirígete a la sección 'Mapa GIS'.")

    elif st.session_state.menu_selection == "Mapa GIS":
        st.subheader("Mapa GIS Interactivo")

        # --- CONTROLES DE FILTRO/BÚSQUEDA DEL MAPA GIS ---
        col1, col2, col3, col4 = st.columns([2.5, 2.5, 2.5, 0.8])

        with col1:
            st.caption("Buscar estación")
            # Asegúrate de que estaciones.csv existe y tiene una columna 'nombre'
            try:
                all_station_names = pd.read_csv("estaciones.csv")["nombre"].unique()
                station_names_for_select = ["Todas las estaciones"] + list(all_station_names)
            except FileNotFoundError:
                st.error("Error: 'estaciones.csv' no encontrado. Asegúrate de que el archivo existe.")
                station_names_for_select = ["Todas las estaciones"] # Fallback
            search_station = st.selectbox(
                "Search Station",
                station_names_for_select,
                label_visibility="collapsed"
            )

        with col2:
            st.caption("Filtrar")
            filter_option = st.selectbox(
                "Filter Options",
                ("Todas", "Activas", "Inactivas"),
                label_visibility="collapsed"
            )

        with col3:
            st.caption("Mostrar")
            display_option = st.selectbox(
                "Display Options",
                ("Estado de las estaciones", "Temperatura", "Precipitación", "Humedad"), # Añadido Humedad
                label_visibility="collapsed"
            )

        with col4:
            st.markdown("<p style='margin-bottom:0.5rem; color: transparent;'>.</p>", unsafe_allow_html=True)
            st.button("☰", key="filter_button_map_gis") # Cambiado el key para evitar duplicados si ya existe un "filter_button"

        # --- LÓGICA DE FILTRADO PARA EL MAPA ---
        try:
            df = pd.read_csv("estaciones.csv")
            
            # Asegúrate de que las columnas necesarias existan en el DataFrame
            required_cols = ['nombre', 'lat', 'lon', 'estado', 'temperatura', 'precipitacion', 'humedad']
            for col in required_cols:
                if col not in df.columns:
                    # Rellena con valores por defecto o muestra un error más específico
                    if col == 'estado':
                        df[col] = 'indefinido'
                    else:
                        df[col] = 0.0 # Valores numéricos por defecto
                    st.warning(f"La columna '{col}' no se encontró en 'estaciones.csv'. Usando valores por defecto.")

            # Filtrar por estado si la opción no es 'Todas'
            if filter_option == "Activas":
                filtered_df = df[df['estado'] == 'activa']
            elif filter_option == "Inactivas":
                filtered_df = df[df['estado'] == 'inactiva']
            else:
                filtered_df = df

            # Lógica de búsqueda de estación (simple por nombre)
            if search_station != "Todas las estaciones":
                filtered_df = filtered_df[filtered_df['nombre'] == search_station]

            # Define los colores basados en la opción de visualización
            def get_color_for_map(row):
                if display_option == "Estado de las estaciones":
                    return [0, 150, 0, 160] if row['estado'] == 'activa' else [255, 0, 0, 160] # Verde vs Rojo
                elif display_option == "Temperatura":
                    # Ejemplo de escala de color para temperatura (ajustar rangos y colores)
                    temp = row['temperatura']
                    if temp < 10: return [0, 0, 255, 160] # Azul (frío)
                    elif temp < 25: return [0, 255, 0, 160] # Verde (templado)
                    else: return [255, 0, 0, 160] # Rojo (caliente)
                elif display_option == "Precipitación":
                    # Ejemplo de escala de color para precipitación
                    prec = row['precipitacion']
                    if prec == 0: return [100, 100, 100, 160] # Gris (sin lluvia)
                    elif prec < 5: return [0, 100, 255, 160] # Azul claro (lluvia ligera)
                    else: return [0, 0, 255, 160] # Azul oscuro (lluvia fuerte)
                elif display_option == "Humedad":
                    # Ejemplo de escala de color para humedad
                    hum = row['humedad']
                    if hum < 40: return [255, 165, 0, 160] # Naranja (baja humedad)
                    elif hum < 70: return [0, 255, 255, 160] # Cian (humedad media)
                    else: return [0, 128, 0, 160] # Verde oscuro (alta humedad)
                return [0, 150, 0, 160] # Color por defecto si no coincide ninguna opción

            # Tooltip para mostrar información detallada al pasar el ratón
            tooltip = {
                "html": "<b>Estación:</b> {nombre}<br/>"
                        "<b>Estado:</b> {estado}<br/>"
                        "<b>Temperatura:</b> {temperatura:.1f}°C<br/>"
                        "<b>Precipitación:</b> {precipitacion:.1f}mm<br/>"
                        "<b>Humedad:</b> {humedad:.1f}%<br/>"
                        "<b>Lat:</b> {lat:.4f}<br/>"
                        "<b>Lon:</b> {lon:.4f}",
                "style": {"backgroundColor": "darkblue", "color": "white", "font-family": "Segoe UI"}
            }

            st.pydeck_chart(pdk.Deck(
                map_style='mapbox://styles/mapbox/light-v9',
                initial_view_state=pdk.ViewState(
                    latitude=filtered_df["lat"].mean() if not filtered_df.empty else 0,
                    longitude=filtered_df["lon"].mean() if not filtered_df.empty else 0,
                    zoom=5,
                    pitch=50,
                ),
                layers=[
                    pdk.Layer(
                        'ScatterplotLayer',
                        data=filtered_df,
                        get_position='[lon, lat]',
                        get_color=get_color_for_map, # Usar la función mejorada
                        get_radius=2500,
                        pickable=True, # Habilita la interacción para el tooltip
                    ),
                ],
                tooltip=tooltip # Aplicar el tooltip
            ))

        except FileNotFoundError:
            st.error("Error: 'estaciones.csv' no encontrado. Asegúrate de que el archivo existe en el directo correcto")
