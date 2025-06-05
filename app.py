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

# Asegúrate de que 'fondo.jpg' exista en el mismo directorio o proporciona la ruta completa.
try:
    img_base64 = get_base64_of_bin_file("fondo.jpg")
except FileNotFoundError:
    st.error("Error: 'fondo.jpg' no encontrado. Asegúrate de que la imagen esté en el mismo directorio que el script.")
    img_base64 = "" # Para evitar errores si la imagen no se encuentra

# --- Nuevo código para el logo ---
try:
    logo_base64 = get_base64_of_bin_file("adrlogo.png")
except FileNotFoundError:
    st.error("Error: 'adrlogo.png' no encontrado. Asegúrate de que el logo esté en el mismo directorio que el script.")
    logo_base64 = "" # Para evitar errores si la imagen no se encuentra

# --- Fin del nuevo código para el logo ---

st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/jpg;base64,{img_base64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    height: 100vh;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: white;
}}

/* Estilos para el logo */
.logo-container {{
    text-align: center;
    margin-top: 4rem;
    margin-bottom: 2rem;
}}

.logo-container img {{
    max-width: 250px; /* Ajusta esto al tamaño deseado para tu logo */
    height: auto;
    display: block;
    margin: 0 auto;
}}

h1 {{
    color: white;
    text-align: center;
    margin-top: 4rem;
    margin-bottom: 2rem;
}}

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

div.stTextInput > label {{
    font-weight: 600;
    font-size: 1rem;
    margin-bottom: 0.5rem;
    display: block;
    color: white;
}}

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

/* --- Estilos para el menú lateral (REVISADO Y MEJORADO) --- */
[data-testid="stSidebar"] {{
    background-color: #1A2437; /* Color de fondo oscuro similar al ejemplo */
    color: white;
    padding-top: 20px;
    padding-left: 0px; /* Ajustado para que las opciones empiecen más a la izquierda */
    padding-right: 0px;
}}

[data-testid="stSidebar"] .stRadio {{
    width: 100%; /* Asegura que el contenedor del radio ocupe todo el ancho */
}}

/* Estilo general para cada opción del menú */
[data-testid="stSidebar"] .stRadio > label {{
    font-size: 1rem;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.7); /* Blanco más suave para las opciones no seleccionadas */
    padding: 12px 20px; /* Más padding para un mejor espaciado */
    margin-bottom: 0px; /* Elimina el margen inferior entre elementos */
    border-radius: 0px; /* Bordes rectos para un look más moderno */
    transition: background-color 0.2s ease, color 0.2s ease;
    display: flex;
    align-items: center;
    width: 100%; /* Ocupa todo el ancho disponible */
}}

/* Estado hover para las opciones */
[data-testid="stSidebar"] .stRadio > label:hover {{
    background-color: #2D3E5E; /* Color de fondo al pasar el ratón, ligeramente más claro */
    color: white; /* Texto blanco puro al hacer hover */
    cursor: pointer; /* Indicar que es clickeable */
}}

/* Ocultar el círculo de radio nativo de Streamlit */
[data-testid="stSidebar"] .stRadio > label > div:first-child {{
    display: none !important; /* Elimina completamente el círculo */
}}

/* Estilo para la opción seleccionada */
[data-testid="stSidebar"] .stRadio > label[data-baseweb="radio"][aria-checked="true"] {{
    background-color: #0E1629; /* Fondo más oscuro para la opción seleccionada */
    color: white; /* Texto blanco puro para la opción seleccionada */
    font-weight: 600; /* Ligeramente más negrita para resaltar */
}}

/* Estilo para el título del menú en la sidebar */
[data-testid="stSidebar"] h1 {{
    color: white;
    text-align: left;
    margin-bottom: 1.5rem; /* Más espacio debajo del título */
    font-size: 1.8rem;
    padding: 0 20px; /* Padding izquierdo/derecho para el título */
}}

/* Asegurar que el contenedor del radio no agregue margen */
.stRadio div[role="radiogroup"] {{
    padding: 0;
}}

/* Para los iconos si los hubiera, margen a la derecha del icono */
.stRadio > label > div[data-testid="stMarkdownContainer"] {{
    display: flex;
    align-items: center;
    gap: 10px; /* Espacio entre icono y texto */
}}
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    if logo_base64: # Solo muestra el logo si se cargó correctamente
        st.markdown(f"""
        <div class="logo-container">
            <img src="data:image/png;base64,{logo_base64}" alt="ADR Logo">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.title("Polaris Web") # Fallback si el logo no se carga

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

    # Si quieres añadir un icono a "Tablero", puedes hacerlo así:
    # Opción 1: Usando la lista de opciones con emojis o caracteres unicode
    # Esto es limitado pero fácil:
    display_options = [
        "🏠 Tablero" if opt == "Tablero" else opt for opt in menu_options
    ]

    # Opción 2 (más avanzada, si usas st-pages o similares):
    # Podrías pasar una lista de diccionarios con 'label' y 'icon'

    selected_option_display = st.sidebar.radio(
        "Navegación",
        options=display_options,
        index=display_options.index(
            "🏠 " + st.session_state.menu_selection if st.session_state.menu_selection == "Tablero" else st.session_state.menu_selection
        ), # Ajusta el índice para que coincida con la opción de display
        key="main_menu_radio",
        label_visibility="collapsed" # Oculta la etiqueta "Navegación"
    )

    # Convertir de vuelta a la opción original para el manejo de contenido
    # Quita el emoji '🏠 ' si está presente
    actual_selected_option = selected_option_display.replace("🏠 ", "")

    if actual_selected_option != st.session_state.menu_selection:
        st.session_state.menu_selection = actual_selected_option
        st.rerun()

    # --- Contenido principal basado en la selección del menú ---
    # Usa actual_selected_option para el control de flujo
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
