st.markdown(f"""
<style>
/* Fondo con imagen */
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/jpg;base64,{img_base64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    height: 100vh;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
}}

/* Formulario glassmorphism */
.login-form {{
    background: rgba(255, 255, 255, 0.15);
    border-radius: 20px;
    padding: 3rem 2.5rem;
    max-width: 400px;
    width: 90vw;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.18);
    color: white;
    text-align: center;
}} 

.login-form h1 {{
    font-weight: 700;
    font-size: 2.5rem;
    margin-bottom: 2rem;
}}

/* Labels */
div.stTextInput > label {{
    font-weight: 600;
    font-size: 1rem;
    margin-bottom: 0.5rem;
    display: block;
    color: white;
}}

/* Inputs */
div.stTextInput > div > input {{
    width: 100% !important;
    padding: 0.75rem 1rem !important;
    margin-bottom: 1.5rem !important;
    border-radius: 10px !important;
    border: none !important;
    font-size: 1rem !important;
    outline: none !important;
    box-shadow: none !important;
    transition: box-shadow 0.3s ease !important;
    background-color: rgba(255, 255, 255, 0.25) !important;
    color: white !important;
}}

/* Input placeholder and text color */
div.stTextInput > div > input::placeholder {{
    color: rgba(255, 255, 255, 0.7) !important;
}}

/* Input focus */
div.stTextInput > div > input:focus {{
    box-shadow: 0 0 8px 2px #1E90FF !important;
    background-color: rgba(255, 255, 255, 0.35) !important;
}}

/* Botón */
div.stButton > button {{
    width: 100% !important;
    padding: 0.85rem 1rem !important;
    background-color: #1E90FF !important;
    border: none !important;
    border-radius: 12px !important;
    color: white !important;
    font-weight: 700 !important;
    font-size: 1.3rem !important;
    cursor: pointer !important;
    transition: background-color 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(30, 144, 255, 0.5);
}}

div.stButton > button:hover {{
    background-color: #1c7ed6 !important;
    box-shadow: 0 6px 20px rgba(30, 144, 255, 0.7);
}}
</style>
""", unsafe_allow_html=True)
