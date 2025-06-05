import streamlit as st
import pandas as pd
import pydeck as pdk
import base64
import re

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
    overflow-y: auto; /* Allow scrolling for content */
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

/* General H1 and H2 styles for content pages */
h1, h2, h3 {{
    color: white;
    text-align: center;
    margin-top: 2rem;
    margin-bottom: 1rem;
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

/* --- GENERAL FORM STYLES FOR CONTENT PAGES (Estaciones, Informe, Supervisor) --- */
.stForm {{
    background-color: rgba(255, 255, 255, 0.1); /* Slightly visible background for forms */
    padding: 20px;
    border-radius: 10px;
    margin-top: 2rem;
    margin-bottom: 2rem;
}}
.stForm > div > div > label {{ /* Adjust label color inside forms */
    color: white !important;
}}
.stForm h3 {{ /* Adjust title color inside forms */
    color: white !important;
    text-align: left;
    margin-top: 0;
    margin-bottom: 1.5rem;
}}

/* --- Selectbox styles (re-applied for consistency) --- */
div.stSelectbox > label {{
    font-weight: 600;
    font-size: 1rem;
    margin-bottom: 0.5rem;
    display: block;
    color: white;
}}
.stSelectbox [data-testid="stSelectboxProcessedOptions"] {{
    background-color: rgba(255, 255, 255, 0.15) !important;
    border-radius: 8px !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    color: white !important;
    padding: 0.5rem 1rem !important;
    font-size: 1rem !important;
}}
.stSelectbox ul {{
    background-color: #2D3E5E !important;
    color: white !important;
    border-radius: 8px;
}}
.stSelectbox li:hover {{
    background-color: #1A2437 !important;
    color: white !important;
}}
.stSelectbox li[aria-selected="true"] {{
    background-color: #1E90FF !important;
    color: white !important;
}}

/* --- GIS Map Controls --- */
.stButton[data-testid="baseButton-secondary"] > button {{
    background-color: #1E90FF !important;
    color: white !important;
    font-weight: 700;
    font-size: 1.2rem;
    padding: 0.75rem 1rem !important;
    border-radius: 10px !important;
    border: none !important;
    width: auto !important;
    min-width: 50px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 38px;
    margin-top: 1.5rem;
}}
.stButton[data-testid="baseButton-secondary"] > button:hover {{
    background-color: #1c7ed6 !important;
}}

/* Adjust margins for column layout in GIS Map */
.st-emotion-cache-1jm692t, .st-emotion-cache-1jm692t > div {{
    margin-bottom: 0 !important;
    padding-bottom: 0 !important;
}}
.st-emotion-cache-1c7y2vl {{ /* This targets the columns internal padding */
    padding-bottom: 0px !important;
}}

/* Specific adjustments for the PyDeck map container itself */
.stDeckGlJsonChart {{
    border-radius: 10px;
    overflow: hidden;
    margin-top: 1rem;
}}

/* --- NEW: GIS Map Legend Box --- */
.gis-legend-box {{
    background-color: rgba(255, 255, 255, 0.9); /* Semi-transparent white */
    border-radius: 8px;
    padding: 15px;
    position: absolute; /* Position over the map */
    bottom: 20px; /* Adjust as needed */
    right: 20px; /* Adjust as needed */
    z-index: 1000; /* Ensure it's above the map */
    color: #333; /* Dark text for readability on light background */
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    max-width: 250px; /* Limit width */
}}
.gis-legend-box h4 {{
    color: #333;
    margin-top: 0;
    margin-bottom: 10px;
    font-size: 1.1rem;
}}
.legend-item {{
    display: flex;
    align-items: center;
    margin-bottom: 5px;
    font-size: 0.9rem;
}}
.legend-color-box {{
    width: 15px;
    height: 15px;
    border-radius: 50%; /* Circular for points */
    margin-right: 8px;
    flex-shrink: 0;
}}
.legend-count {{
    margin-left: auto;
    font-weight: bold;
}}

/* --- NEW: Text Input with Search Icon (Nuevo informe personalizado) --- */
.search-input-container {{
    position: relative;
    margin-bottom: 1.5rem;
}}
.search-input-container input {{
    padding-right: 35px !important; /* Space for icon */
}}
.search-input-icon {{
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    color: rgba(255, 255, 255, 0.7);
    pointer-events: none; /* Don't block input clicks */
}}
.search-input-container label {{ /* Adjust label for these search inputs */
    color: white !important;
    font-weight: 600;
    font-size: 1rem;
    margin-bottom: 0.5rem;
    display: block;
}}

/* --- NEW: Buttons for "Nuevo informe personalizado" LISTAR section --- */
.list-buttons-container {{
    display: flex;
    justify-content: flex-end; /* Align to the right */
    gap: 10px; /* Space between buttons */
    margin-top: 1rem;
    margin-bottom: 1rem;
}}
.list-buttons-container button {{
    width: auto !important; /* Allow buttons to size to content */
    padding: 0.5rem 1rem !important;
    font-size: 0.9rem !important;
    border-radius: 5px !important;
}}
/* Specific styles for "Añadir Todos..." and "Añadir Todos los val" */
.list-buttons-container button.st-emotion-cache-nahz7x {{ /* Default Streamlit button style */
    background-color: #6C757D !important; /* Gray */
}}
.list-buttons-container button.st-emotion-cache-nahz7x:hover {{
    background-color: #5a6268 !important;
}}
.list-buttons-container button.st-emotion-cache-nahz7x[data-testid="baseButton-secondary"]:nth-of-type(2) {{ /* Target the second button for green */
    background-color: #28A745 !important; /* Green */
}}
.list-buttons-container button.st-emotion-cache-nahz7x[data-testid="baseButton-secondary"]:nth-of-type(2):hover {{
    background-color: #218838 !important;
}}
/* Style for "Restablecer filtros" button */
.reset-filter-button-container {{
    display: flex;
    justify-content: flex-end;
    margin-top: 1rem;
    margin-bottom: 1rem;
}}
.reset-filter-button-container button {{
    background-color: #6C757D !important; /* Gray */
    color: white !important;
    width: auto !important;
    padding: 0.5rem 1rem !important;
    font-size: 0.9rem !important;
    border-radius: 5px !important;
}}
.reset-filter-button-container button:hover {{
    background-color: #5a6268 !important;
}}

/* --- NEW: Supervisor Tunnel specific styles --- */
.supervisor-stats-container {{
    display: flex;
    justify-content: space-around;
    padding: 15px;
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    margin-bottom: 2rem;
}}
.stat-item {{
    text-align: center;
    font-size: 1.1rem;
    font-weight: bold;
    color: white;
}}
.stat-item .count {{
    font-size: 1.5rem;
    margin-right: 5px;
}}
.stat-connected {{ color: #28a745; }} /* Green */
.stat-listening {{ color: #ffc107; }} /* Yellow */
.stat-disconnected {{ color: #dc3545; }} /* Red */

/* Export button for Supervisor Tunnel */
.supervisor-export-button-container {{
    display: flex;
    justify-content: flex-end;
    margin-bottom: 1rem;
}}
.supervisor-export-button-container button {{
    background-color: #1E90FF !important;
    color: white !important;
    width: auto !important;
    padding: 0.5rem 1rem !important;
    font-size: 0.9rem !important;
    border-radius: 5px !important;
    display: flex;
    align-items: center;
    gap: 8px;
}}
.supervisor-export-button-container button:hover {{
    background-color: #1c7ed6 !important;
}}

/* Dataframe styles - making them dark/transparent */
[data-testid="stDataFrame"] {{
    background-color: rgba(0, 0, 0, 0.5) !important;
    border-radius: 10px;
    overflow: hidden; /* For rounded corners */
}}
[data-testid="stDataFrame"] table {{
    background-color: transparent !important;
    color: white !important;
}}
[data-testid="stDataFrame"] thead th {{
    background-color: rgba(45, 62, 94, 0.8) !important; /* Darker header */
    color: white !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.3) !important;
}}
[data-testid="stDataFrame"] tbody tr {{
    background-color: rgba(25, 34, 53, 0.6) !important; /* Darker row background */
}}
[data-testid="stDataFrame"] tbody tr:nth-child(even) {{
    background-color: rgba(35, 48, 74, 0.6) !important; /* Slightly different for even rows */
}}
[data-testid="stDataFrame"] tbody tr:hover {{
    background-color: rgba(60, 77, 107, 0.8) !important; /* Hover effect */
}}
[data-testid="stDataFrame"] td, [data-testid="stDataFrame"] th {{
    border-color: rgba(255, 255, 255, 0.1) !important; /* Lighter borders for cells */
    color: white !important;
}}
/* Pagination control for dataframe */
[data-testid="stBlock"] .stSelectbox [data-testid="stSelectboxProcessedOptions"] {{
    background-color: rgba(0,0,0,0.5) !important; /* Darker for this specific selectbox */
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
    if st.session_state.menu_selection == "Tablero":
        st.title("Tablero de Control")
        st.write("Bienvenido al tablero principal. Aquí podrás ver un resumen de los datos.")
    elif st.session_state.menu_selection == "GIS":
        st.title("Información Geográfica")
        st.write("Explora datos GIS relevantes para tus proyectos.")

    elif st.session_state.menu_selection == "Mapa GIS":
        st.subheader("Mapa GIS")

        # --- CONTROLES DE FILTRO/BÚSQUEDA DEL MAPA GIS ---
        col1, col2, col3, col4 = st.columns([2.5, 2.5, 2.5, 0.8]) # Adjusted proportions

        with col1:
            st.caption("Buscar estación")
            # Dynamic station names from CSV
            try:
                all_station_names = ["Todas las estaciones"] + list(pd.read_csv("estaciones.csv")["nombre"].unique())
            except FileNotFoundError:
                all_station_names = ["Todas las estaciones", "Estación A", "Estación B", "Estación C"]
                st.warning("`estaciones.csv` no encontrado. Usando datos de ejemplo para 'Buscar estación'.")

            search_station = st.selectbox(
                "Search Station",
                all_station_names,
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
            st.button("☰", key="map_filter_button")

        # --- PyDeck Map Section ---
        try:
            df = pd.read_csv("estaciones.csv")
            
            if 'estado' not in df.columns:
                st.error("La columna 'estado' no se encontró en 'estaciones.csv'. Por favor, asegúrate de que el archivo contiene esta columna.")
                df['estado'] = 'indefinido' # Fallback to prevent errors

            if filter_option == "Activas":
                filtered_df = df[df['estado'] == 'activa']
            elif filter_option == "Inactivas":
                filtered_df = df[df['estado'] == 'inactiva']
            else:
                filtered_df = df

            if search_stat
