import streamlit as st

# Asegúrate de que set_page_config sea el primer comando de Streamlit
st.set_page_config(page_title="Make Your Diet", layout="wide")

from streamlit_option_menu import option_menu
import about, account, diet_generator
import os
from PIL import Image

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({"title": title, "function": function})

    @st.cache_data
    def get_logo_background_color(_self, logo_path):  # Cambia 'self' por '_self'
        if os.path.exists(logo_path):
            try:
                with Image.open(logo_path) as img:
                    rgb_img = img.convert('RGBA')
                    datas = rgb_img.getdata()

                    new_data = []
                    for item in datas:
                        # Cambiar todos los píxeles blancos (y tonos de blanco) a transparentes
                        if item[0] > 200 and item[1] > 200 and item[2] > 200:
                            new_data.append((255, 255, 255, 0))
                        else:
                            new_data.append(item)

                    rgb_img.putdata(new_data)
                    return rgb_img
            except ImportError:
                st.warning("Necesitas instalar la biblioteca Pillow para extraer el color del logo.")
        else:
            st.warning(f"Logo no encontrado en {logo_path}")
        return None

    def run(self):
        logo_path = "images/make_your_diet_web.png"
        logo_image = self.get_logo_background_color(logo_path)

        # Mover el menú a una barra lateral izquierda sin fondo y letras negras
        with st.sidebar:
            if logo_image:
                st.image(logo_image, width=300)  # Aumentar el tamaño del logo

            app = option_menu(
                menu_title="",
                options=["Account", "Diet Generator", "About"],  
                icons=['person', 'table', 'question'],
                menu_icon='menu',
                default_index=0,
                orientation="vertical",
                styles={
                    "container": {"padding": "5!important", "background-color": "transparent"},  # Sin fondo
                    "icon": {"color": "black", "font-size": "23px"},
                    "nav-link": {
                        "color": "#000000",  # Letras en negro
                        "font-size": "20px",
                        "text-align": "left",
                        "margin": "0px",
                        "--hover-color": "#D3D3D3",
                        "--hover-background-color": "#F0F0F0",
                        "--hover-border-radius": "10px",
                        "--hover-box-shadow": "0 4px 8px rgba(0, 0, 0, 0.1)"
                    },
                    "nav-link-selected": {
                        "background-color": "#02ab21",
                        "border-radius": "10px",
                        "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.1)"
                    }
                }
            )

        # Establecer el fondo de la aplicación en blanco
        st.markdown(
            """
            <style>
            .main {
                background-color: white;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        if app == "Account":
            account.app()
        elif app == "Diet Generator":
            diet_generator.app()
        elif app == "About":
            about.app()

# Crear una instancia de MultiApp y agregar las aplicaciones
app = MultiApp()
app.add_app("Account", account.app)
app.add_app("Diet Generator", diet_generator.app)
app.add_app("About", about.app)

# Ejecutar la aplicación
app.run()