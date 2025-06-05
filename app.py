import streamlit as st
import pandas as pd
import pydeck as pdk
import base64
import re
import plotly.express as px
import datetime

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
/* Base container for the app view - Se mantiene como está, no se toca */
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/jpg;base64,{img_base64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    height: 100vh;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: white;
}}

/* Logo container styles - Se mantiene como está, no se toca */
.logo-container {{
    text-align: center;
    margin-top: 0.5rem;
    margin-bottom: 1rem;
}}

.logo-container img {{
    max-width: 250px;
    height: auto;
    display: block;
    margin: 0 auto;
}}

/* General H1 styles - Se mantiene como está, no se toca */
h1 {{
    color: white;
    text-align: center;
    margin-top: 0.5rem;
    margin-bottom: 1rem;
}}

/* Button styles - Se mantiene como está, no se toca */
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

/* Text input label styles - Se mantiene como está, no se toca */
div.stTextInput > label {{
    font-weight: 600;
    font-size: 1rem;
    margin-bottom: 0.5rem;
    display: block;
    color: white;
}}

/* Text input field styles - Se mantiene como está, no se toca */
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

/* --- ESTILOS DEL MENÚ LATERAL (SIDEBAR) --- */

/* Overall sidebar background and spacing */
[data-testid="stSidebar"] {{
    background-color: #1A2437; /* Fondo oscuro */
    color: white;
    padding-top: 0px;
    padding-left: 0px;
    padding-right: 0px;
    height: 100vh; /* Ocupa toda la altura de la ventana */
    display: flex;
    flex-direction: column;
}}

/* Contenedor del contenido del sidebar - CRÍTICO para el scroll y espacio */
[data-testid="stSidebarContent"] {{
    flex: 1; /* Permite que este elemento crezca y ocupe el espacio disponible */
    overflow-y: auto; /* Habilita el scroll vertical si el contenido excede el espacio */
    padding-top: 10px; /* Ajuste para el título, un poco menos */
    padding-bottom: 10px; /* Espacio al final del menú, un poco menos */
    padding-left: 0px;
    padding-right: 0px;
}}

/* Título en el sidebar */
[data-testid="stSidebarContent"] h1 {{
    color: white;
    text-align: left;
    margin-bottom: 0.5rem; /* Margen inferior aún más reducido */
    font-size: 1.5rem; /* Título un poco más pequeño */
    padding: 0 15px; /* Padding horizontal ligeramente reducido */
}}

/* Contenedor del grupo de radio buttons */
[data-testid="stSidebarContent"] .stRadio div[role="radiogroup"] {{
    width: 100%;
    padding: 0;
}}

/* Cada opción del menú (el área clicable) */
[data-testid="stSidebarContent"] .stRadio label {{
    font-size: 0.9rem; /* TAMAÑO DE TEXTO AÚN MÁS PEQUEÑO para maximizar espacio */
    font-weight: 500;
    color: rgba(255, 255, 255, 0.7) !important; /* Blanco ligeramente desvanecido */
    padding: 3px 15px !important; /* REDUCIDO AL MÍNIMO para que quepan todos los elementos */
    margin-bottom: 0px !important;
    border-radius: 0px !important;
    transition: background-color 0.2s ease, color 0.2s ease;
    display: flex !important;
    align-items: center !important;
    width: 100% !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1); /* Línea sutil */
}}

/* Eliminar la línea del último elemento del menú */
[data-testid="stSidebarContent"] .stRadio label:last-child {{
    border-bottom: none !important;
}}

/* Estado hover (cuando el ratón está encima) */
[data-testid="stSidebarContent"] .stRadio label:hover {{
    background-color: #2D3E5E !important; /* Fondo más claro en hover */
    color: white !important; /* Texto blanco puro en hover */
    cursor: pointer !important;
}}

/* Estado seleccionado (activo) */
[data-testid="stSidebarContent"] .stRadio label[data-baseweb="radio"][aria-checked="true"] {{
    background-color: #0E1629 !important; /* Fondo más oscuro para el elemento seleccionado */
    color: white !important; /* Texto blanco puro para el elemento seleccionado */
    font-weight: 600 !important; /* Ligeramente más negrita */
}}

/* Ocultar el círculo nativo del radio button */
[data-testid="stSidebarContent"] .stRadio label > div:first-child {{
    display: none !important;
}}

/* Alineación de íconos/emojis con el texto */
[data-testid="stSidebarContent"] .stRadio label > div[data-testid="stMarkdownContainer"] {{
    display: flex;
    align-items: center;
    gap: 7px; /* Espacio entre el ícono y el texto, un poco más reducido */
}}

/* --- ESTILOS PARA CONTROLES DEL MAPA GIS (NO SE TOCAN) --- */

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
            <img src="data:image:png;base64,{logo_base64}" alt="ADR Logo">
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
        st.title("🏠 Tablero de Control")
        st.write("Bienvenido al tablero principal de PolarisWEB. Aquí puedes ver un resumen del estado de tu red de monitoreo.")

        st.markdown("---")
        st.header("Métricas Clave")
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric(label="Estaciones Activas", value="15 / 20", delta="↑ 2 en 24h")
        with col_m2:
            st.metric(label="Alarmas Activas", value="3", delta="↑ 1 nueva")
        with col_m3:
            st.metric(label="Última Actualización", value=datetime.datetime.now().strftime("%H:%M:%S"), delta="Hace 1 minuto")

        st.markdown("---")
        st.header("Precipitación Total Últimas 24h")
        # Datos de ejemplo para el gráfico
        data_precip = pd.DataFrame({
            "Hora": pd.to_datetime(pd.date_range(end=datetime.datetime.now(), periods=24, freq='H')),
            "Precipitación (mm)": [i * 0.5 + (i % 5) for i in range(24)]
        })
        fig_precip = px.area(data_precip, x="Hora", y="Precipitación (mm)", title="Acumulado de Precipitación Horaria",
                             labels={"Precipitación (mm)": "Precipitación (mm)"})
        st.plotly_chart(fig_precip, use_container_width=True)


    elif st.session_state.menu_selection == "GIS":
        st.title("🌐 Información Geográfica")
        st.write("Esta sección provee herramientas avanzadas de análisis geográfico y gestión de capas GIS.")
        st.info("Aquí se podrían cargar y superponer diferentes capas GIS (hidrográficas, geológicas, límites administrativos, etc.) para análisis complejos.")
        st.subheader("Opciones Avanzadas GIS")
        st.checkbox("Mostrar capas hidrográficas")
        st.checkbox("Mostrar zonas de riesgo")
        st.selectbox("Seleccionar tipo de mapa base", ["Satélite", "Calles", "Topográfico"])


    elif st.session_state.menu_selection == "Mapa GIS":
        st.subheader("🗺️ Mapa GIS de Estaciones")

        # --- CONTROLES DE FILTRO/BÚSQUEDA DEL MAPA GIS ---
        col1, col2, col3, col4 = st.columns([2.5, 2.5, 2.5, 0.8])

        with col1:
            st.caption("Buscar estación")
            try:
                df_stations = pd.read_csv("estaciones.csv")
                station_names = ["Todas las estaciones"] + list(df_stations["nombre"].unique())
            except FileNotFoundError:
                st.error("Error: 'estaciones.csv' no encontrado. Asegúrate de que la imagen esté en el mismo directorio que el script.")
                station_names = ["Todas las estaciones"] # Fallback
            except KeyError:
                st.error("Error: Columna 'nombre' no encontrada en 'estaciones.csv'.")
                station_names = ["Todas las estaciones"] # Fallback

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
                df['estado'] = 'indefinido' # Default para evitar errores si la columna no existe

            if filter_option == "Activas":
                filtered_df = df[df['estado'] == 'activa']
            elif filter_option == "Inactivas":
                filtered_df = df[df['estado'] == 'inactiva']
            else:
                filtered_df = df

            if search_station != "Todas las estaciones":
                filtered_df = filtered_df[filtered_df['nombre'] == search_station]

            # Esto se puede quitar si no se quiere mostrar la tabla de datos del mapa
            # st.write("Datos que se están enviando al mapa (con la columna 'estado' del CSV):")
            # st.dataframe(filtered_df)

            def get_color(row):
                if display_option == "Estado de las estaciones":
                    return [0, 150, 0, 160] if row['estado'] == 'activa' else [100, 100, 100, 160] # Verde vs Gris
                elif display_option == "Temperatura":
                    # Ejemplo: Rojo para caliente, azul para frío
                    temp = row.get('temperatura', 0) # Asegúrate de tener esta columna en CSV
                    if temp > 25: return [255, 0, 0, 160] # Rojo
                    elif temp < 10: return [0, 0, 255, 160] # Azul
                    else: return [0, 200, 0, 160] # Verde
                elif display_option == "Precipitación":
                    # Ejemplo: Azul claro para poca, azul oscuro para mucha
                    precip = row.get('precipitacion', 0) # Asegúrate de tener esta columna en CSV
                    if precip > 10: return [0, 0, 150, 160] # Azul oscuro
                    elif precip > 0: return [0, 150, 255, 160] # Azul claro
                    else: return [150, 150, 150, 160] # Gris si no hay precipitación
                return [200, 200, 0, 160] # Default si no se encuentra opción

            st.pydeck_chart(pdk.Deck(
                map_style='mapbox://styles/mapbox/light-v9', # Puedes probar otros estilos: dark-v10, satellite-streets-v11
                initial_view_state=pdk.ViewState(
                    latitude=filtered_df["lat"].mean() if not filtered_df.empty else 40.4168, # Default Madrid si no hay datos
                    longitude=filtered_df["lon"].mean() if not filtered_df.empty else -3.7038, # Default Madrid si no hay datos
                    zoom=5,
                    pitch=50,
                ),
                layers=[
                    pdk.Layer(
                        'ScatterplotLayer',
                        data=filtered_df,
                        get_position='[lon, lat]',
                        get_color=get_color,
                        get_radius=2500, # Tamaño de los puntos
                        pickable=True, # Hace los puntos clickeables
                        auto_highlight=True,
                    ),
                ],
            ))

            st.write("Haz clic en los puntos del mapa para más detalles (funcionalidad de tooltip se implementaría con más complejidad en PyDeck).")

        except FileNotFoundError:
            st.error("Error: 'estaciones.csv' no encontrado. Asegúrate de que el archivo existe en el mismo directorio que el script.")
            st.warning("Para el 'Mapa GIS', crea un archivo `estaciones.csv` con columnas: `nombre, lat, lon, estado, temperatura, precipitacion`.")
            st.dataframe(pd.DataFrame({'nombre': ['Estación Demo 1'], 'lat': [40.4168], 'lon': [-3.7038], 'estado': ['activa'], 'temperatura': [20], 'precipitacion': [5]}))

        except KeyError as e:
            st.error(f"Error en el CSV: Columna '{e}' no encontrada. Asegúrate de que 'estaciones.csv' tiene las columnas 'nombre', 'lat', 'lon', 'temperatura', 'precipitacion' Y 'estado'.")
            st.warning("Para el 'Mapa GIS', crea un archivo `estaciones.csv` con columnas: `nombre, lat, lon, estado, temperatura, precipitacion`.")
            st.dataframe(pd.DataFrame({'nombre': ['Estación Demo 1'], 'lat': [40.4168], 'lon': [-3.7038], 'estado': ['activa'], 'temperatura': [20], 'precipitacion': [5]}))


    elif st.session_state.menu_selection == "Visor":
        st.title("📊 Visor de Datos")
        st.write("Accede a herramientas avanzadas para la visualización de series de tiempo de tus estaciones.")

        st.subheader("Selección de Datos")
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            try:
                df_stations_viewer = pd.read_csv("estaciones.csv")
                station_options = list(df_stations_viewer["nombre"].unique())
            except FileNotFoundError:
                station_options = ["Estación Demo"]
                st.warning("Para el 'Visor', crea un archivo `estaciones.csv` con una columna `nombre`.")

            selected_station = st.selectbox("Selecciona Estación", station_options)
        with col_v2:
            # Asumiendo que tenemos variables comunes para mostrar
            variable_options = ["Temperatura", "Precipitación", "Humedad", "Nivel de Agua"]
            selected_variable = st.selectbox("Selecciona Variable", variable_options)

        st.subheader(f"Gráfico de {selected_variable} para {selected_station}")

        # Datos de ejemplo para el visor
        time_data = pd.DataFrame({
            "Fecha/Hora": pd.to_datetime(pd.date_range(end=datetime.datetime.now(), periods=100, freq='H')),
            selected_variable: [i + (i % 10) * 0.5 for i in range(100)]
        })
        fig_viewer = px.line(time_data, x="Fecha/Hora", y=selected_variable,
                             title=f"Serie de Tiempo de {selected_variable}")
        st.plotly_chart(fig_viewer, use_container_width=True)


    elif st.session_state.menu_selection == "Fast Viewer":
        st.title("⚡ Fast Viewer")
        st.write("Visualización rápida de datos en tiempo real (modo simplificado).")
        st.info("Esta sección podría mostrar los datos más recientes de las estaciones críticas sin configuraciones adicionales.")
        st.text_area("Datos en tiempo real (simulado)", "Estación A: Temp 22.5°C, Precip 0.0mm\nEstación B: Nivel 1.2m, Hum 78%\n...", height=200)


    elif st.session_state.menu_selection == "Estaciones":
        st.title("📡 Gestión de Estaciones")
        st.write("Administra y consulta información detallada de todas tus estaciones de monitoreo.")

        st.subheader("Listado de Estaciones")
        try:
            df_all_stations = pd.read_csv("estaciones.csv")
            # Añadir una columna de "Última Conexión" si no existe
            if 'ultima_conexion' not in df_all_stations.columns:
                df_all_stations['ultima_conexion'] = [
                    (datetime.datetime.now() - datetime.timedelta(minutes=i*10)).strftime("%Y-%m-%d %H:%M:%S")
                    for i in range(len(df_all_stations))
                ]
            st.dataframe(df_all_stations, use_container_width=True)
        except FileNotFoundError:
            st.error("Error: 'estaciones.csv' no encontrado. Asegúrate de que el archivo existe en el mismo directorio que el script.")
            st.warning("Crea un archivo `estaciones.csv` con columnas: `nombre, lat, lon, estado, temperatura, precipitacion`.")
            st.dataframe(pd.DataFrame({'nombre': ['Estación A', 'Estación B'], 'lat': [41.3, 42.0], 'lon': [2.1, 1.5], 'estado': ['activa', 'inactiva'], 'temperatura': [20, 15], 'precipitacion': [5, 0], 'ultima_conexion': [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), (datetime.datetime.now() - datetime.timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S")]}))
        except KeyError as e:
            st.error(f"Error en el CSV: Columna '{e}' no encontrada. Asegúrate de que 'estaciones.csv' tiene las columnas requeridas.")


    elif st.session_state.menu_selection == "Monitoring":
        st.title("📈 Monitoreo en Tiempo Real")
        st.write("Aquí puedes supervisar los parámetros clave de las estaciones en vivo.")
        st.info("Implementar un panel de monitoreo con actualizaciones automáticas (requeriría backend o mecanismos de refresh).")


    elif st.session_state.menu_selection == "Informe personalizado":
        st.title("📄 Informes Personalizados")
        st.write("Genera informes a medida con los datos seleccionados y en el formato deseado.")
        st.info("Secciones para selección de fechas, estaciones, variables, formatos de exportación (PDF, CSV).")


    elif st.session_state.menu_selection == "Informe rosa de los vientos":
        st.title("💨 Informe Rosa de los Vientos")
        st.write("Visualiza patrones de dirección y velocidad del viento para estaciones seleccionadas.")
        st.info("Gráficos de rosa de los vientos para análisis meteorológicos.")


    elif st.session_state.menu_selection == "Consecutive Rains":
        st.title("🌧️ Análisis de Lluvias Consecutivas")
        st.write("Herramientas para analizar eventos de lluvia prolongados y sus impactos.")
        st.info("Cálculo de acumulados, intensidad y duración de eventos de lluvia.")


    elif st.session_state.menu_selection == "Vistas":
        st.title("👁️ Vistas Predefinidas")
        st.write("Carga y guarda configuraciones de visualización de datos y paneles.")
        st.info("Permite a los usuarios guardar y acceder rápidamente a sus configuraciones de gráficos y tablas.")


    elif st.session_state.menu_selection == "Sinóptico":
        st.title("🗺️ Diseñador de Sinópticos")
        st.write("Crea o edita diagramas sinópticos interactivos de tus sistemas.")
        st.info("Herramienta para diseñar representaciones visuales de la red con datos en vivo.")


    elif st.session_state.menu_selection == "Sinópticos":
        st.title("🗺️ Sinópticos Existentes")
        st.write("Lista y accede a tus diagramas sinópticos configurados.")
        st.info("Panel de control para ver y lanzar los sinópticos creados.")


    elif st.session_state.menu_selection == "Custom Synoptics":
        st.title("⚙️ Sinópticos Personalizados")
        st.write("Gestiona tus sinópticos adaptados y específicos para tus necesidades.")
        st.info("Funcionalidad para sinópticos con configuraciones avanzadas o específicas de usuario.")


    elif st.session_state.menu_selection == "Supervisor":
        st.title("🧑‍💻 Panel de Supervisor")
        st.write("Herramientas para la supervisión y gestión de usuarios y permisos del sistema.")
        st.info("Control de acceso, roles de usuario y auditoría.")


    elif st.session_state.menu_selection == "Estadísticas de red":
        st.title("📊 Estadísticas de la Red")
        st.write("Consulta el rendimiento y estado general de tu red de monitoreo.")
        st.info("Métricas de uptime, latencia, volumen de datos, etc.")


    elif st.session_state.menu_selection == "Registros":
        st.title("📜 Historial de Registros")
        st.write("Accede a los logs y registros de actividad detallados del sistema.")
        st.info("Filtrado y búsqueda de logs para diagnóstico de problemas.")


    elif st.session_state.menu_selection == "Módulos":
        st.title("📦 Administración de Módulos")
        st.write("Activa y desactiva módulos de la aplicación para personalizar la experiencia.")
        st.info("Interfaz para gestionar extensiones y funcionalidades adicionales.")


    elif st.session_state.menu_selection == "Túnel":
        st.title("🔗 Configuración de Túnel")
        st.write("Gestiona conexiones y túneles de comunicación seguros a tus dispositivos.")
        st.info("Herramientas para configurar conexiones VPN o túneles SSH/TCP.")


    elif st.session_state.menu_selection == "Validador":
        st.title("✅ Herramienta de Validación")
        st.write("Valida la calidad y consistencia de tus datos de monitoreo.")
        st.info("Reglas de validación, detección de outliers y corrección de datos.")


    elif st.session_state.menu_selection == "Cerrar sesión":
        st.session_state.logged_in = False
        st.rerun()

if st.session_state.log
