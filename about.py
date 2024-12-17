import streamlit as st

def app():
    st.title("About")

    st.header("¿En qué consiste esta aplicación?")
    st.write("""
    Esta aplicación está diseñada para ayudarte a gestionar tu dieta y tu cuenta personal de manera eficiente. 
    A continuación, se describen las principales funcionalidades de la aplicación:

    - **Account**: Aquí puedes gestionar tu información personal, incluyendo tu nombre, email, edad y subir una foto de perfil.
    - **Diet Generator**: Una herramienta para generar planes de dieta personalizados según tus necesidades y objetivos.
    - **About**: Esta sección donde puedes encontrar información sobre la aplicación y cómo utilizarla.

    ### Características Adicionales
    - **Personalización de Dietas**: Puedes definir tus necesidades de macronutrientes manualmente o calcularlas automáticamente según tus datos personales.
    - **Selección de Alimentos Preferidos**: Puedes seleccionar tus fuentes preferidas de proteínas, hidratos y grasas para cada comida.
    - **Distribución de Macronutrientes**: La aplicación distribuye las calorías y macronutrientes entre las comidas del día según tus preferencias.
    - **Guardado de Configuraciones**: Tus configuraciones y datos personales se guardan automáticamente para que no tengas que ingresarlos cada vez.

    ### ¿Cómo Utilizar la Aplicación?
    1. **Account**: Comienza ingresando tu información personal en la sección Account. Aquí puedes guardar tu nombre, email, edad, peso, altura, género, nivel de actividad y objetivo.
    2. **Diet Generator**: Dirígete a la sección Diet Generator para generar un plan de dieta personalizado. Puedes definir tus necesidades de macronutrientes manualmente o dejar que la aplicación los calcule automáticamente según tus datos personales.
    3. **Selecciona Alimentos Preferidos**: En Diet Generator, selecciona tus fuentes preferidas de proteínas, hidratos y grasas para cada comida.
    4. **Genera tu Dieta**: La aplicación generará un plan de dieta personalizado con la distribución de calorías y macronutrientes por comida.

    ### Contacto
    Si tienes alguna sugerencia o necesitas ayuda, no dudes en contactarnos a través del siguiente correo electrónico:
    - **Correo de Sugerencias**: mauriciomontillagarcia@gmail.com
    Esperamos que esta aplicación te sea de gran ayuda para alcanzar tus objetivos de salud y bienestar.
    """)

# Llamar a la función app para ejecutar la aplicación
if __name__ == "__main__":
    app()