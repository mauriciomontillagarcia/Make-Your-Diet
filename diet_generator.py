import streamlit as st
import pandas as pd
import numpy as np
import os
from funciones import distribuir_macronutrientes, generar_combinaciones
from streamlit_option_menu import option_menu

@st.cache_data
def cargar_datos_alimentos():
    file_path = os.path.join('data', 'alimentos.csv')
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        st.error("El archivo 'alimentos.csv' no se encuentra en la carpeta 'data'.")
        return pd.DataFrame()

@st.cache_data
def cargar_datos_usuario():
    file_path = os.path.join('data', 'usuario.csv')
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return pd.DataFrame(columns=["Nombre", "Apellido", "Email", "Edad", "Peso", "Altura", "Género", "Nivel de Actividad", "Objetivo"])

def calcular_tmb(peso, altura, edad, genero):
    if genero == "Masculino":
        return 88.36 + (13.4 * peso) + (4.8 * altura) - (5.7 * edad)
    else:
        return 447.6 + (9.2 * peso) + (3.1 * altura) - (4.3 * edad)

def ajustar_calorias(tmb, nivel_actividad):
    actividad_factor = {
        "Sedentario": 1.2,
        "Ligera actividad": 1.375,
        "Moderada actividad": 1.55,
        "Alta actividad": 1.725,
        "Muy alta actividad": 1.9
    }
    return tmb * actividad_factor[nivel_actividad]

def calcular_macronutrientes(calorias, peso, objetivo):
    if objetivo == "Perder peso":
        calorias -= 500
    elif objetivo == "Ganar peso":
        calorias += 500
    
    proteinas = peso * 1
    grasas = peso * 0.8
    hidratos = (calorias - (proteinas * 4 + grasas * 9)) / 4
    return calorias, proteinas, hidratos, grasas

def app():
    df_alimentos = cargar_datos_alimentos()
    df_usuario = cargar_datos_usuario()

    if df_alimentos.empty:
        st.stop()  # Detener la ejecución si no se pudo cargar el archivo CSV

    if not df_usuario.empty:
        nombre = df_usuario["Nombre"].values[0]
        apellido = df_usuario["Apellido"].values[0]
        email = df_usuario["Email"].values[0]
        edad = df_usuario["Edad"].values[0]
        peso = df_usuario["Peso"].values[0]
        altura = df_usuario["Altura"].values[0]
        genero = df_usuario["Género"].values[0]
        nivel_actividad = df_usuario["Nivel de Actividad"].values[0]
        objetivo = df_usuario["Objetivo"].values[0]
    else:
        nombre = ""
        apellido = ""
        email = ""
        edad = 0
        peso = 0.0
        altura = 0.0
        genero = ""
        nivel_actividad = ""
        objetivo = ""

    metodo_necesidades = st.radio("HOLA", 
                                  ("Definir por mí mismo", "Calcular automáticamente"))

    if metodo_necesidades == "Definir por mí mismo":
        calorias = st.number_input("Calorías (kcal)", min_value=1000, value=2250)
        porcentaje_proteinas = st.slider("Porcentaje de proteínas (%)", min_value=0, max_value=100, value=40)
        porcentaje_hidratos = st.slider("Porcentaje de hidratos (%)", min_value=0, max_value=100, value=40)
        porcentaje_grasas = st.slider("Porcentaje de grasas (%)", min_value=0, max_value=100, value=20)
        
        proteinas = (calorias * (porcentaje_proteinas / 100)) / 4
        hidratos = (calorias * (porcentaje_hidratos / 100)) / 4
        grasas = (calorias * (porcentaje_grasas / 100)) / 9
        
        st.write(f"Proteínas: {proteinas:.2f} g")
        st.write(f"Hidratos: {hidratos:.2f} g")
        st.write(f"Grasas: {grasas:.2f} g")
    else:
        tmb = calcular_tmb(peso, altura, edad, genero)
        calorias = ajustar_calorias(tmb, nivel_actividad)
        calorias, proteinas, hidratos, grasas = calcular_macronutrientes(calorias, peso, objetivo)
        
        st.write(f"Calorías: {calorias:.2f} kcal")
        st.write(f"Proteínas: {proteinas:.2f} g")
        st.write(f"Hidratos: {hidratos:.2f} g")
        st.write(f"Grasas: {grasas:.2f} g")

    num_comidas = st.slider("¿Cuántas comidas deseas realizar al día?", 1, 7, 4)
    nombres_comidas = [st.text_input(f"Nombre de la comida {i+1}", value=f"Comida {i+1}") for i in range(num_comidas)]

    distribucion_personalizada = st.radio("¿Quieres personalizar la distribución porcentual de macronutrientes?", 
                                          ("Sí", "No"))

    if distribucion_personalizada == "Sí":
        porcentajes = []
        for i, nombre in enumerate(nombres_comidas):
            porcentaje = st.slider(f"Porcentaje de calorías para {nombre}", 0, 100, [30, 30, 25, 15][i] if i < 4 else 100 // num_comidas)
            porcentajes.append(porcentaje)
    else:
        porcentajes = [30, 30, 25, 15][:num_comidas] + [100 // num_comidas] * (num_comidas - 4)

    distribucion_final = distribuir_macronutrientes(calorias, proteinas, hidratos, grasas, num_comidas, porcentajes)
    st.subheader("Distribución de calorías y macronutrientes por comida")
    st.dataframe(distribucion_final)

    # 4. Elegir alimentos preferidos
    st.subheader("Selecciona tus fuentes preferidas de proteínas, hidratos y grasas")
    favoritos = {
        "Comida 1": {
            "proteinas": ["Claras", "Huevos", "Jamón serrano", "Lomo embuchado", "Pechuga pavo en lonchas", "Proteína isolada"],
            "hidratos": ["Copos avena", "Cornflakes", "Harina de avena", "Tortita de arroz", "Tortita de maíz", "Pan"],
            "grasas": ["Chocolate negro", "Frutos secos", "Guacamole"]
        },
        "Comida 2": {
            "proteinas": ["Atún al natural en lata", "Atún en aceite en lata", "Carne de cerdo", "Carne picada de pollo-pavo", "Pechuga de pollo", "Sepia", "Ternera"],
            "hidratos": ["Arroz", "Garbanzos", "Lentejas", "Pasta"],
            "grasas": ["Aceite"]
        },
        "Comida 3": {
            "proteinas": ["Atún al natural en lata", "Atún en aceite en lata", "Claras", "Hamburguesa de pollo-pavo", "Huevos", "Lomo embuchado", "Pechuga de pollo", "Sardinas", "Sepia", "Ternera"],
            "hidratos": ["Arroz", "Pan", "Patata", "Tortilla trigo", "Tortita de arroz", "Tortita de maíz"],
            "grasas": ["Aceite"]
        },
        "Comida 4": {
            "proteinas": ["Queso fresco batido", "Proteína isolada"],
            "hidratos": ["Cornflakes"],
            "grasas": ["Chocolate negro", "Frutos secos"]
        }
    }
    
    for nombre in nombres_comidas:
        if nombre not in favoritos:
            favoritos[nombre] = {"proteinas": [], "hidratos": [], "grasas": []}
        st.markdown(f"### {nombre}")
        tipo_proteina = st.multiselect(f"Proteínas para {nombre}", df_alimentos[df_alimentos["Tipo"] == "Proteínas"]["Alimento"].tolist(), default=favoritos[nombre]["proteinas"])
        tipo_hidratos = st.multiselect(f"Hidratos para {nombre}", df_alimentos[df_alimentos["Tipo"] == "Hidratos"]["Alimento"].tolist(), default=favoritos[nombre]["hidratos"])
        tipo_grasas = st.multiselect(f"Grasas para {nombre}", df_alimentos[df_alimentos["Tipo"] == "Grasas"]["Alimento"].tolist(), default=favoritos[nombre]["grasas"])
        favoritos[nombre] = {"proteinas": tipo_proteina, "hidratos": tipo_hidratos, "grasas": tipo_grasas}

    # Mostrar distribución y combinaciones en una sola tabla final
    combinaciones_df = generar_combinaciones(df_alimentos, distribucion_final, favoritos)

    # Crear una tabla final con las combinaciones por comida
    tabla_final = pd.DataFrame(index=[f"Opción {i+1}" for i in range(3)], columns=nombres_comidas)

    for nombre in nombres_comidas:
        opciones_comida = combinaciones_df[combinaciones_df["Comida"] == nombre]["Alimentos"].values
        if len(opciones_comida) < 3:
            opciones_comida = list(opciones_comida) + [""] * (3 - len(opciones_comida))  # Rellenar con valores vacíos si hay menos de 3 opciones
        tabla_final[nombre] = opciones_comida

    st.subheader("Dieta generada")
    st.dataframe(tabla_final)