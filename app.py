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
    color: white;
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

    # Prepare options with emojis for display
    display_options = []
    for opt in menu_options:
        if opt == "Tablero":
            display_options.append("🏠 Tablero") # Add home emoji
        elif opt == "GIS":
            display_options.append("🌐 GIS") # Example globe emoji
        elif opt == "Mapa GIS":
            display_options.append("🗺️ Mapa GIS") # Example map emoji
        elif opt == "Visor":
            display_options.append("📊 Visor") # Example bar chart emoji
        elif opt == "Supervisor":
            display_options.append("🧑‍💻 Supervisor") # Example person emoji
        elif opt == "Validador":
            display_options.append("✅ Validador") # Example checkmark emoji
        elif opt == "Registros":
            display_options.append("📜 Registros") # Example scroll emoji
        elif opt == "Módulos":
            display_options.append("📦 Módulos") # Example box emoji
        elif opt == "Túnel":
            display_options.append("🔗 Túnel") # Example link emoji
        elif opt == "Cerrar sesión":
            display_options.append("🚪 Cerrar sesión") # Example door emoji
        else:
            display_options.append(opt)


    # Determine the index for the selected option in display_options
    current_selected_display_option = st.session_state.menu_selection
    if st.session_state.menu_selection == "Tablero":
        current_selected_display_option = "🏠 Tablero"
    elif st.session_state.menu_selection == "GIS":
        current_selected_display_option = "🌐 GIS"
    elif st.session_state.menu_selection == "Mapa GIS":
        current_selected_display_option = "🗺️ Mapa GIS"
    elif st.session_state.menu_selection == "Visor":
        current_selected_display_option = "📊 Visor"
    elif st.session_state.menu_selection == "Supervisor":
        current_selected_display_option = "🧑‍💻 Supervisor"
    elif st.session_state.menu_selection == "Validador":
        current_selected_display_option = "✅ Validador"
    elif st.session_state.menu_selection == "Registros":
        current_selected_display_option = "📜 Registros"
    elif st.session_state.menu_selection == "Módulos":
        current_selected_display_option = "📦 Módulos"
    elif st.session_state.menu_selection == "Túnel":
        current_selected_display_option = "🔗 Túnel"
    elif st.session_state.menu_selection == "Cerrar sesión":
        current_selected_display_option = "🚪 Cerrar sesión"


    selected_index = display_options.index(current_selected_display_option)


    selected_option_display = st.sidebar.radio(
        "Navegación",
        options=display_options,
        index=selected_index,
        key="main_menu_radio",
        label_visibility="collapsed"
    )

    # Convert back to the original option name (removing emoji)
    # This regex removes leading emojis and spaces.
    import re
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
        st.subheader("Mapa GIS Interactivo")
        st.write("Visualiza tus estaciones y datos en un mapa detallado.")
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
    elif st.session_state.menu_selection == "Visor":
        st.title("Visor de Datos")
        st.write("Accede a herramientas avanzadas para la visualización de series de tiempo.")
    elif st.session_state.menu_selection == "Fast Viewer":
        st.title("Visor Rápido")
        st.write("Visualización rápida de datos en tiempo real.")
    elif st.session_state.menu_selection == "Estaciones":
        st.title("Gestión de Estaciones")
        st.write("Administra y consulta información de tus estaciones de monitoreo.")
    elif st.session_state.menu_selection == "Monitoring":
        st.title("Monitoreo en Tiempo Real")
        st.write("Sigue los parámetros clave en tiempo real.")
    elif st.session_state.menu_selection == "Informe personalizado":
        st.title("Informes Personalizados")
        st.write("Genera informes a medida según tus necesidades.")
    elif st.session_state.menu_selection == "Informe rosa de los vientos":
        st.title("Informe Rosa de los Vientos")
        st.write("Visualiza patrones de dirección y velocidad del viento.")
    elif st.session_state.menu_selection == "Consecutive Rains":
        st.title("Análisis de Lluvias Consecutivas")
        st.write("Herramientas para analizar eventos de lluvia prolongados.")
    elif st.session_state.menu_selection == "Vistas":
        st.title("Vistas Predefinidas")
        st.write("Carga y guarda configuraciones de visualización de datos.")
    elif st.session_state.menu_selection == "Sinóptico":
        st.title("Diseñador de Sinópticos")
        st.write("Crea o edita diagramas sinópticos de tus sistemas.")
    elif st.session_state.menu_selection == "Sinópticos":
        st.title("Sinópticos Existentes")
        st.write("Lista de tus diagramas sinópticos.")
    elif st.session_state.menu_selection == "Custom Synoptics":
        st.title("Sinópticos Personalizados")
        st.write("Gestiona tus sinópticos adaptados.")
    elif st.session_state.menu_selection == "Supervisor":
        st.title("Panel de Supervisor")
        st.write("Herramientas para la supervisión y gestión de usuarios.")
    elif st.session_state.menu_selection == "Estadísticas de red":
        st.title("Estadísticas de la Red")
        st.write("Consulta el rendimiento y estado de tu red de monitoreo.")
    elif st.session_state.menu_selection == "Registros":
        st.title("Historial de Registros")
        st.write("Accede a los logs y registros de actividad del sistema.")
    elif st.session_state.menu_selection == "Módulos":
        st.title("Administración de Módulos")
        st.write("Activa y desactiva módulos de la aplicación.")
    elif st.session_state.menu_selection == "Túnel":
        st.title("Configuración de Túnel")
        st.write("Gestiona conexiones y túneles de comunicación.")
    elif st.session_state.menu_selection == "Validador":
        st.title("Herramienta de Validación")
        st.write("Valida la calidad y consistencia de tus datos.")
    elif st.session_state.menu_selection == "Cerrar sesión":
        st.session_state.logged_in = False
        st.rerun()

if st.session_state.logged_in:
    dashboard()
else:
    login()
