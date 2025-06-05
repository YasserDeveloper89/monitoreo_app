import streamlit as st
import pandas as pd
import pydeck as pdk
import base64
import re

# --- Configuración de usuarios y la página ---
USERS = {"admin": "1234"}
st.set_page_config(page_title="Polaris Web", layout="centered")

# --- Funciones de utilidad para cargar imágenes ---
def get_base64_of_bin_file(bin_file):
    """
    Convierte un archivo binario (ej. imagen) a una cadena base64.
    Retorna la cadena base64 o una cadena vacía si el archivo no se encuentra.
    """
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        # st.error(f"Error: '{bin_file}' no encontrado. Asegúrate de que la imagen esté en el mismo directorio que el script.")
        # Quitamos st.error aquí para evitar que se muestre antes de que Streamlit esté completamente inicializado
        # y cause problemas de renderizado al inicio. La falta de la imagen se manejará visualmente.
        print(f"Advertencia: '{bin_file}' no encontrado. Asegúrate de que la imagen esté en el mismo directorio que el script.")
        return "" # Retorna una cadena vacía para que el CSS no falle

# Cargar imágenes de fondo y logo
# Es crucial que estos archivos existan en el mismo directorio que el script app.py
img_base64 = get_base64_of_bin_file("fondo.jpg")
logo_base64 = get_base64_of_bin_file("adrlogo.png")

# --- Estilos CSS inyectados en Streamlit ---
# Se utiliza un f-string para insertar las imágenes base64 directamente en el CSS
# Los estilos deben ser correctos para evitar problemas de renderizado.
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

/* Style for Supervisor cards */
.supervisor-card {{
    background-color: rgba(255, 255, 255, 0.1);
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    cursor: pointer;
    transition: transform 0.2s ease, background-color 0.2s ease;
    min-height: 180px; /* Para mantener altura consistente */
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}}

.supervisor-card:hover {{
    transform: translateY(-5px);
    background-color: rgba(255, 255, 255, 0.15);
}}

.supervisor-card h3 {{
    color: white;
    margin-bottom: 5px;
    font-size: 1.4rem;
}}

.supervisor-card p {{
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.9rem;
    margin-bottom: 0;
}}

</style>
""", unsafe_allow_html=True)

# --- Lógica de autenticación ---
# Inicializa el estado de la sesión para 'logged_in' si no existe.
# Esta es una de las primeras cosas que debe ocurrir.
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    """Muestra la interfaz de inicio de sesión."""
    # Muestra el logo si está disponible, de lo contrario, muestra un título.
    if logo_base64:
        st.markdown(f"""
        <div class="logo-container">
            <img src="data:image/png;base64,{logo_base64}" alt="ADR Logo">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.title("Polaris Web")

    # Campos de entrada para usuario y contraseña
    usuario = st.text_input("Nombre de usuario", placeholder="Introduce tu usuario")
    contrasena = st.text_input("Contraseña", type="password", placeholder="Introduce tu contraseña")

    # Botón de Login
    if st.button("Login"):
        if USERS.get(usuario) == contrasena:
            st.session_state.logged_in = True
            st.session_state.menu_selection = "Tablero" # Establece una selección inicial para el dashboard
            st.rerun() # Reinicia la aplicación para mostrar el dashboard
        else:
            st.error("Usuario o contraseña incorrectos.")

# --- Función principal del Dashboard ---
def dashboard():
    """Muestra el dashboard de la aplicación con navegación lateral y contenido dinámico."""
    # Define las opciones del menú lateral
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

    # Asegura que 'menu_selection' esté siempre inicializado y sea una opción válida
    if "menu_selection" not in st.session_state or st.session_state.menu_selection not in menu_options:
        st.session_state.menu_selection = menu_options[0] # Por defecto, selecciona "Tablero"

    st.sidebar.title("Menú Principal")

    # Prepara las opciones del menú para mostrar con emojis, mapeando la opción real a la de visualización
    display_options_map = {}
    for opt in menu_options:
        if opt == "Tablero": display_options_map[opt] = "🏠 Tablero"
        elif opt == "GIS": display_options_map[opt] = "🌐 GIS"
        elif opt == "Mapa GIS": display_options_map[opt] = "🗺️ Mapa GIS"
        elif opt == "Visor": display_options_map[opt] = "📊 Visor"
        elif opt == "Fast Viewer": display_options_map[opt] = "⚡ Fast Viewer"
        elif opt == "Estaciones": display_options_map[opt] = "📡 Estaciones"
        elif opt == "Monitoring": display_options_map[opt] = "📈 Monitoring"
        elif opt == "Informe personalizado": display_options_map[opt] = "📄 Informe personalizado"
        elif opt == "Informe rosa de los vientos": display_options_map[opt] = "💨 Informe rosa de los vientos"
        elif opt == "Consecutive Rains": display_options_map[opt] = "🌧️ Consecutive Rains"
        elif opt == "Vistas": display_options_map[opt] = "👁️ Vistas"
        elif opt == "Sinóptico": display_options_map[opt] = "🗺️ Sinóptico"
        elif opt == "Sinópticos": display_options_map[opt] = "🗺️ Sinópticos"
        elif opt == "Custom Synoptics": display_options_map[opt] = "⚙️ Custom Synoptics"
        elif opt == "Supervisor": display_options_map[opt] = "🧑‍💻 Supervisor"
        elif opt == "Estadísticas de red": display_options_map[opt] = "📊 Estadísticas de red"
        elif opt == "Registros": display_options_map[opt] = "📜 Registros"
        elif opt == "Módulos": display_options_map[opt] = "📦 Módulos"
        elif opt == "Túnel": display_options_map[opt] = "🔗 Túnel"
        elif opt == "Validador": display_options_map[opt] = "✅ Validador"
        elif opt == "Cerrar sesión": display_options_map[opt] = "🚪 Cerrar sesión"
        else: display_options_map[opt] = opt # Opción de fallback si no hay emoji

    # Obtiene la lista de opciones de visualización para el radio button
    options_for_radio = list(display_options_map.values())

    # Determina la opción actual a mostrar como seleccionada en el radio button
    current_display_option = display_options_map.get(st.session_state.menu_selection, menu_options[0])
    selected_index = options_for_radio.index(current_display_option)


    # Crea el radio button en la barra lateral
    selected_option_display = st.sidebar.radio(
        "Navegación",
        options=options_for_radio,
        index=selected_index,
        key="main_menu_radio",
        label_visibility="collapsed"
    )

    # Invierte el mapeo para obtener la opción real a partir de la opción de visualización
    # Esto es más seguro que usar regex, ya que el regex podría fallar con emojis complejos.
    actual_selected_option = next((key for key, value in display_options_map.items() if value == selected_option_display), None)

    # Si la opción seleccionada ha cambiado, actualiza el estado de la sesión y reinicia la aplicación
    if actual_selected_option and actual_selected_option != st.session_state.menu_selection:
        st.session_state.menu_selection = actual_selected_option
        st.rerun()

    # --- Contenido principal basado en la selección del menú ---
    # Cada 'elif' DEBE TERMINAR CON ':' y tener una indentación correcta.
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
            station_names = ["Todas las estaciones"]
            try:
                # Asegúrate de que 'estaciones.csv' exista y tenga una columna 'nombre'
                df_stations_load = pd.read_csv("estaciones.csv")
                station_names.extend(list(df_stations_load["nombre"].unique()))
            except FileNotFoundError:
                st.warning("El archivo 'estaciones.csv' no fue encontrado para cargar nombres de estación.")
            except KeyError:
                st.warning("La columna 'nombre' no se encontró en 'estaciones.csv'.")

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
            df = pd.read_csv("estaciones.csv")

            if 'estado' not in df.columns:
                st.error("La columna 'estado' no se encontró en 'estaciones.csv'. Por favor, asegúrate de que el archivo contiene esta columna.")
                df['estado'] = 'indefinido' # Asigna un valor por defecto si no existe

            # Filtrar por estado si la opción no es 'Todas'
            if filter_option == "Activas":
                filtered_df = df[df['estado'].str.lower() == 'activa']
            elif filter_option == "Inactivas":
                filtered_df = df[df['estado'].str.lower() == 'inactiva']
            else:
                filtered_df = df

            # Lógica de búsqueda de estación (simple por nombre)
            if search_station != "Todas las estaciones":
                filtered_df = filtered_df[filtered_df['nombre'] == search_station]

            # Define los colores basados en el estado
            def get_color(row):
                return [0, 150, 0, 160] if row['estado'].lower() == 'activa' else [100, 100, 100, 160] # Verde vs Gris

            if not filtered_df.empty:
                st.pydeck_chart(pdk.Deck(
                    map_style='mapbox://styles/mapbox/light-v9',
                    initial_view_state=pdk.ViewState(
                        latitude=filtered_df["lat"].mean(),
                        longitude=filtered_df["lon"].mean(),
                        zoom=5,
                        pitch=50,
                    ),
                    layers=[
                        pdk.Layer(
                            'ScatterplotLayer',
                            data=filtered_df,
                            get_position='[lon, lat]',
                            get_color=get_color,
                            get_radius=2500,
                        ),
                    ],
                ))
            else:
                st.warning("No hay estaciones para mostrar con los filtros aplicados.")

        except FileNotFoundError:
            st.error("Error: 'estaciones.csv' no encontrado. Asegúrate de que el archivo existe en el mismo directorio que el script.")
        except KeyError as e:
            st.error(f"Error en el CSV: Columna '{e}' no encontrada. Asegúrate de que 'estaciones.csv' tiene las columnas 'nombre', 'lat', 'lon' y 'estado'.")
        except Exception as e:
            st.error(f"Ocurrió un error inesperado al cargar el mapa: {e}")

    elif st.session_state.menu_selection == "Visor":
        st.title("Visor de Datos")
        st.write("Accede a herramientas avanzadas para la visualización de series de tiempo.")
    elif st.session_state.menu_selection == "Fast Viewer":
        st.title("Visor Rápido")
        st.write("Visualización rápida de datos en tiempo real.")

    elif st.session_state.menu_selection == "Estaciones":
        st.title("Gestión de Estaciones")
        st.write("Administra y consulta información de tus estaciones de monitoreo.")

        # Controles de filtros basados en la imagen "Estaciones"
        st.subheader("Filtros de Estaciones")
        col_est1, col_est2, col_est3 = st.columns(3)
        with col_est1:
            station_names_filter = ["Todas las estaci
