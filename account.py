import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

@st.cache
def cargar_datos_peso():
    file_path = os.path.join('data', 'peso.csv')
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return pd.DataFrame(columns=["Fecha", "Peso"])

def guardar_datos_usuario(nombre, apellido, email, edad, peso, altura, genero, nivel_actividad, objetivo):
    df_usuario = pd.DataFrame({
        "Nombre": [nombre],
        "Apellido": [apellido],
        "Email": [email],
        "Edad": [edad],
        "Peso": [peso],
        "Altura": [altura],
        "Género": [genero],
        "Nivel de Actividad": [nivel_actividad],
        "Objetivo": [objetivo]
    })
    df_usuario.to_csv('data/usuario.csv', index=False)

def guardar_datos_peso(fecha, peso):
    df_peso = cargar_datos_peso()
    df_peso = df_peso.append({"Fecha": fecha, "Peso": peso}, ignore_index=True)
    df_peso.to_csv('data/peso.csv', index=False)

def app():
    st.title("Account")

    # Datos del usuario
    st.header("Información del Usuario")
    
    col1, col2 = st.columns(2)
    
    with col1:
        nombre = st.text_input("Nombre")
        email = st.text_input("Email")
        peso = st.number_input("Peso (kg)", min_value=0.0)
        nivel_actividad = st.selectbox("Nivel de actividad física", ["Sedentario", "Ligera actividad", "Moderada actividad", "Alta actividad", "Muy alta actividad"])
        genero = st.radio("Género", ("Masculino", "Femenino"))

    with col2:
        apellido = st.text_input("Apellido")
        edad = st.number_input("Edad", min_value=0, max_value=100, step=1)
        altura = st.number_input("Altura (cm)", min_value=0.0)
        objetivo = st.selectbox("Objetivo", ["Perder peso", "Mantenerse", "Ganar peso"])

    # Guardar los datos del usuario
    if st.button("Guardar"):
        guardar_datos_usuario(nombre, apellido, email, edad, peso, altura, genero, nivel_actividad, objetivo)
        guardar_datos_peso(pd.Timestamp.now().date(), peso)
        st.success("Datos guardados correctamente")

    # Mostrar gráfico de evolución del peso
    st.header("Evolución del Peso")
    df_peso = cargar_datos_peso()
    if not df_peso.empty:
        fig, ax = plt.subplots()
        ax.plot(df_peso["Fecha"], df_peso["Peso"], marker='o')
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Peso (kg)")
        ax.set_title("Evolución del Peso")
        st.pyplot(fig)

# Llamar a la función app para ejecutar la aplicación
if __name__ == "__main__":
    app()