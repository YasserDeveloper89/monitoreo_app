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

/* --- Estilos para el menú lateral --- */
[data-testid="stSidebar"] {{
    background-color: #1A2437; /* Color de fondo oscuro similar al ejemplo */
    color: white;
    padding-top: 20px;
    padding-left: 10px;
}}

[data-testid="stSidebar"] .stRadio > label {{
    font-size: 1rem;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.85); /* Un blanco ligeramente menos puro */
    padding: 10px 15px;
    margin-bottom: 5px;
    border-radius: 5px;
    transition: background-color 0.2s ease, color 0.2s ease;
    display: flex;
    align-items: center; /* Para alinear con iconos si los hubiera */
}}

[data-testid="stSidebar"] .stRadio > label:hover {{
    background-color: #2D3E5E; /* Color de fondo al pasar el ratón */
    color: white;
}}

/* Estilo para la opción seleccionada */
[data-testid="stSidebar"] .stRadio > label[data-baseweb="radio"] > div:first-child {{
    background-color: transparent !important; /* Quita el círculo de radio nativo */
    border: none !important;
}}

[data-testid="stSidebar"] .stRadio > label[data-baseweb="radio"] > div:first-child > div {{
    background-color: transparent !important; /* Quita el círculo de radio nativo interno */
}}

[data-testid="stSidebar"] .stRadio > label[data-baseweb="radio"][aria-checked="true"] {{
    background-color: #0E1629; /* Color de fondo para la opción seleccionada */
    color: white;
    font-weight: 600;
}}

/* Estilo para el título del menú en la sidebar */
[data-testid="stSidebar"] h1 {{
    color: white;
    text-align: left;
    margin-bottom: 1rem;
    font-size: 1.8rem;
    padding-left: 10px;
}}

/* Para hacer los elementos de lista del radio más como enlaces */
.stRadio div[role="radiogroup"] > label {{
    margin-left: 0; /* Asegura que no haya indentación */
}}

/* Quitar el marcador de círculo del radio button */
.stRadio > label > div:first-child {{
    display: none !important;
}}

</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Inicializa 'menu_selection' si no existe
if "menu_selection" not in st.session_state:
    st.session_state.menu_selection = "Inicio" # Opción por defecto al iniciar sesión

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
            st.success("Sesión iniciada correctamente.")
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos.")

def dashboard():
    # Define las opciones del menú con los títulos que ves en el ejemplo
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
        "Cerrar sesión" # Añadimos Cerrar sesión aquí para que esté en el menú
    ]

    st.sidebar.title("Menú Principal") # Título para la barra lateral

    # Usar st.radio para el menú en la barra lateral
    # Guardamos la selección en st.session_state para que persista
    selected_option = st.sidebar.radio(
        "Navegación", # Etiqueta del radio, puede ser vacía "" si no quieres texto
        options=menu_options,
        index=menu_options.index(st.session_state.menu_selection), # Mantiene la opción seleccionada
        key="main_menu_radio" # Clave única para el widget
    )

    # Actualiza la sesión de estado si la opción cambia
    if selected_option != st.session_state.menu_selection:
        st.session_state.menu_selection = selected_option
        st.rerun() # Para que se recargue y muestre el contenido de la nueva sección

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
        # Reutilizamos el código del mapa que ya tenías
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
        st.session_state.menu_selection = "Inicio" # Resetea la selección del menú al cerrar sesión
        st.rerun()

if st.session_state.logged_in:
    dashboard()
else:
    login()
                                        
