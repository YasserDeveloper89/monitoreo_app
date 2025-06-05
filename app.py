import streamlit as st
import pandas as pd
import pydeck as pdk
import base64
import re

USERS = {"admin": "1234567890"}

st.set_page_config(page_title="Polaris Web", layout="centered")

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
    color: white; /* Default text color, will be overridden by overlay */
    position: relative; /* Needed for the overlay */
    /* Posiblemente reducir el padding superior por defecto de Streamlit */
    padding-top: 0rem; /* Añadido/Ajustado: Intenta reducir el padding superior del contenedor principal */
}}

/* Overlay for background image to ensure text legibility */
[data-testid="stAppViewContainer"]::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent black overlay (50% opacity) */
    z-index: -1; /* Place it behind content but in front of background image */
}}


/* Logo container styles */
.logo-container {{
    text-align: center;
    /* REDUCIMOS MÁS EL MARGEN SUPERIOR PARA SUBIR EL LOGO Y EL FORMULARIO */
    margin-top: 0.5rem; /* Antes 2rem, intentemos 0.5rem o incluso 0 */
    margin-bottom: 1rem; /* Antes 1.5rem, lo hacemos un poco más compacto */
}}

.logo-container img {{
    max-width: 250px;
    height: auto;
    display: block;
    margin: 0 auto;
}}

/* General H1 styles (para cuando no hay logo) */
h1 {{
    color: white;
    text-align: center;
    /* Ajustamos también aquí si no hay logo */
    margin-top: 0.5rem; /* Antes 2rem */
    margin-bottom: 1rem; /* Antes 1.5rem */
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
    margin-bottom: 0.25rem; /* Reducido para compactar las etiquetas */
    display: block;
    color: white; /* Ensure labels are white and clearly visible */
}}

/* Text input field styles */
div.stTextInput > div > input {{
    width: 100% !important;
    padding: 0.75rem 1rem !important;
    margin-bottom: 1rem !important; /* Reducido para compactar los campos */
    border-radius: 10px !important;
    border: none !important;
    font-size: 1rem !important;
    outline: none !important;
    background-color: rgba(255, 255, 255, 0.25) !important; /* Semi-transparent white background for input fields */
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

/* NEW: Flexbox container for login elements to vertically center or align */
.main-login-container {{
    display: flex;
    flex-direction: column;
    justify-content: center; /* Centra verticalmente el contenido */
    align-items: center; /* Centra horizontalmente el contenido (para los elementos flex) */
    min-height: 100vh; /* Asegura que el contenedor ocupe toda la altura de la vista */
    padding: 1rem; /* Añade un poco de padding para no pegar el contenido a los bordes */
    box-sizing: border-box; /* Incluye el padding en el cálculo del ancho/alto */
}}

/* RE-ADJUST Streamlit's main content wrapper to center */
[data-testid="stVerticalBlock"] {{
    max-width: 400px; /* Limita el ancho del formulario para que no se extienda demasiado */
    width: 90%; /* Ancho responsivo */
    margin: auto; /* Centra el bloque verticalmente */
    padding: 20px; /* Añade padding interno para que el contenido no pegue a los bordes */
    background-color: rgba(0, 0, 0, 0.3); /* Un fondo sutil para el formulario en sí, si se quiere */
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}}

</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    # Añadimos un div contenedor para todo el contenido de login
    # Esto es más bien para propósitos de CSS que Streamlit pueda inyectar directamente
    # Streamlit ya envuelve el contenido en un stVerticalBlock por defecto,
    # así que vamos a apuntar a ese test-id si es posible.
    # No es necesario envolver aquí con markdown si los CSS apuntan a los elementos de Streamlit directamente.

    if logo_base64:
        st.markdown(f"""
        <div class="logo-container">
            <img src="data:image/png;base64,{logo_base64}" alt="ADR Logo">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.title("Polaris Web")

    # Los elementos de st.text_input y st.button serán contenidos por un stVerticalBlock

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
    if st.session_state.menu_selection == "Tablero":
        st.title("Tablero de Control")
        st.write("Bienvenido al tablero principal. Aquí podrás ver un resumen de los datos.")
    elif st.session_state.menu_selection == "GIS":
        st.title("Información Geográfica")
        st.write("Explora datos GIS relevantes para tus proyectos.")
    elif st.session_state.menu_selection == "Mapa GIS":
        st.subheader("Mapa GIS")

        # --- CONTROLES DE FILTRO/BÚSQUEDA DEL MAPA GIS ---
        col1, col2, col3, col4 = st.columns([2.5, 2.5, 2.5, 0.8])

        with col1:
            st.caption("Buscar estación")
            # Simular estaciones.csv si no existe
            try:
                df_all_stations = pd.read_csv("estaciones.csv")
            except FileNotFoundError:
                st.warning("Archivo 'estaciones.csv' no encontrado. Se generarán datos de ejemplo.")
                data = {
                    'nombre': ['Estación A', 'Estación B', 'Estación C', 'Estación D', 'Estación E'],
                    'lat': [41.3851, 41.4000, 41.3700, 41.3950, 41.3650],
                    'lon': [2.1734, 2.1800, 2.1600, 2.1900, 2.1500],
                    'temperatura': [25, 28, 22, 26, 21],
                    'precipitacion': [10, 5, 12, 8, 3],
                    'estado': ['activa', 'inactiva', 'activa', 'activa', 'inactiva']
                }
                df_all_stations = pd.DataFrame(data)
                # Opcional: Guardar el CSV para futuras ejecuciones
                # df_all_stations.to_csv("estaciones.csv", index=False)


            station_names = ["Todas las estaciones"] + list(df_all_stations["nombre"].unique())
            search_station = st.selectbox(
                "Search Station",
                station_names,
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
                ("Estado de las estaciones", "Temperatura", "Precipitación"),
                label_visibility="collapsed"
            )

        with col4:
            st.markdown("<p style='margin-bottom:0.5rem; color: transparent;'>.</p>", unsafe_allow_html=True)
            st.button("☰", key="filter_button")

        # --- LÓGICA DE FILTRADO PARA EL MAPA ---
        try:
            df = df_all_stations.copy() # Usar una copia para no modificar el DataFrame original

            # Pequeña verificación para asegurarnos de que la columna 'estado' existe en el DataFrame
            if 'estado' not in df.columns:
                st.error("La columna 'estado' no se encontró en 'estaciones.csv'. Por favor, asegúrate de que el archivo contiene esta columna. Se asignará un estado 'indefinido' por defecto.")
                df['estado'] = 'indefinido'

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

            # --- Mantenemos la tabla para depuración, puedes quitarla si quieres ---
            st.write("Datos que se están enviando al mapa (con la columna 'estado' del CSV):")
            st.dataframe(filtered_df)
            # ----------------------------------------------------------------------

            # Define los colores basados en el estado
            def get_color(row):
                if display_option == "Estado de las estaciones":
                    return [0, 150, 0, 160] if row['estado'] == 'activa' else [100, 100, 100, 160] # Verde vs Gris
                elif display_option == "Temperatura":
                    # Ejemplo: Gradiente de color para temperatura (azul a rojo)
                    temp = row['temperatura']
                    if temp < 15: return [0, 0, 255, 160] # Azul frío
                    elif temp < 25: return [0, 200, 0, 160] # Verde templado
                    else: return [255, 0, 0, 160] # Rojo cálido
                elif display_option == "Precipitación":
                    # Ejemplo: Gradiente de color para precipitación (amarillo a azul oscuro)
                    precip = row['precipitacion']
                    if precip < 5: return [255, 255, 0, 160] # Poca lluvia, amarillo
                    elif precip < 10: return [0, 191, 255, 160] # Lluvia moderada, azul cielo
                    else: return [0, 0, 128, 160] # Mucha lluvia, azul oscuro
                return [255, 255, 255, 160] # Blanco por defecto si no coincide

            # Calcula el centro del mapa dinámicamente o usa un valor por defecto si filtered_df está vacío
            initial_latitude = filtered_df["lat"].mean() if not filtered_df.empty else 41.3851 # Centro de Barcelona
            initial_longitude = filtered_df["lon"].mean() if not filtered_df.empty else 2.1734 # Centro de Barcelona
            initial_zoom = 5 if not filtered_df.empty else 10 # Zoom más cercano si hay datos

            st.pydeck_chart(pdk.Deck(
                map_style='mapbox://styles/mapbox/
