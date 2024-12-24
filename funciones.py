import streamlit as st 
import pandas as pd
import numpy as np

# 1. Definir función para distribuir macronutrientes
def distribuir_macronutrientes(calorias, proteinas, hidratos, grasas, num_comidas, porcentajes=None):
    """
    Distribuye las calorías y macronutrientes entre las comidas del día.

    :param calorias: Total de calorías.
    :param proteinas: Total de proteínas.
    :param hidratos: Total de hidratos.
    :param grasas: Total de grasas.
    :param num_comidas: Número de comidas al día.
    :param porcentajes: Lista de porcentajes para cada comida.
    :return: DataFrame con la distribución de macronutrientes por comida.
    """
    if porcentajes:
        if len(porcentajes) != num_comidas:
            raise ValueError("El número de porcentajes proporcionado no coincide con el número de comidas.")
        if sum(porcentajes) != 100:
            raise ValueError("La suma de los porcentajes debe ser 100.")
        proporciones = np.array(porcentajes) / 100
    else:
        proporciones = np.full(num_comidas, 1 / num_comidas)

    distribucion = pd.DataFrame({
        "Comida": [f"Comida {i+1}" for i in range(num_comidas)],
        "Calorías": calorias * proporciones,
        "Proteínas": proteinas * proporciones,
        "Hidratos": hidratos * proporciones,
        "Grasas": grasas * proporciones
    })

    return distribucion

# 2. Función auxiliar para seleccionar alimentos
def seleccionar_alimentos(alimentos_comida, remaining_cal, remaining_protein, remaining_carbs, remaining_fat):
    alimentos_seleccionados = []
    total_proteinas = 0
    total_hidratos = 0
    total_grasas = 0
    tipos_seleccionados = set()

    while remaining_cal > 0 and not alimentos_comida.empty:
        alimento_seleccionado = alimentos_comida.sample(1)
        alimento_nombre = alimento_seleccionado["Alimento"].values[0]
        alimento_tipo = alimento_seleccionado["Tipo"].values[0]
        alimento_cal = alimento_seleccionado["Kcal"].values[0]
        alimento_protein = alimento_seleccionado["Proteína"].values[0]
        alimento_carbs = alimento_seleccionado["Hidratos"].values[0]
        alimento_fat = alimento_seleccionado["Grasas"].values[0]
        alimento_mezcla = alimento_seleccionado["Mezcla"].values[0]

        # Calcular una cantidad realista basada en las calorías restantes
        gramos_a_usar = min(100, remaining_cal / alimento_cal * 100)
        
        # Redondear gramos a múltiplos de 5
        gramos_a_usar = round(gramos_a_usar / 5) * 5
        
        kcal_usadas = (gramos_a_usar / 100) * alimento_cal
        proteinas_usadas = (gramos_a_usar / 100) * alimento_protein
        hidratos_usados = (gramos_a_usar / 100) * alimento_carbs
        grasas_usadas = (gramos_a_usar / 100) * alimento_fat

        # Verificar restricciones de cantidad mínima y máxima
        if (alimento_tipo == "Grasas" and (grasas_usadas < 5 or grasas_usadas > 25)) or \
           (alimento_tipo == "Proteínas" and proteinas_usadas < 75) or \
           (alimento_tipo == "Hidratos" and hidratos_usados < 30):
            continue

        alimentos_seleccionados.append(f"{alimento_nombre} ({gramos_a_usar:.0f}g)")
        remaining_cal -= kcal_usadas
        remaining_protein -= proteinas_usadas
        remaining_carbs -= hidratos_usados
        remaining_fat -= grasas_usadas

        # Añadir el tipo de alimento a los tipos seleccionados
        tipos_seleccionados.add(alimento_tipo)

        # Actualizar los totales de macronutrientes seleccionados
        if alimento_tipo == "Proteínas":
            total_proteinas += proteinas_usadas
        elif alimento_tipo == "Hidratos":
            total_hidratos += hidratos_usados
        elif alimento_tipo == "Grasas":
            total_grasas += grasas_usadas

        alimentos_comida = alimentos_comida[alimentos_comida["Alimento"] != alimento_nombre]

    # Verificar que se cumplan las cantidades mínimas para cada tipo de macronutriente en la combinación final
    if total_proteinas < 75 or total_hidratos < 30 or total_grasas < 5 or total_grasas > 25:
        return []

    return alimentos_seleccionados

# 3. Definir función para generar combinaciones de alimentos
def generar_combinaciones(alimentos, distribucion, favoritos):
    """
    Genera combinaciones de alimentos para cada comida basada en las necesidades de macronutrientes.

    :param alimentos: DataFrame con la información de los alimentos.
    :param distribucion: DataFrame con la distribución de macronutrientes por comida.
    :param favoritos: Diccionario con los alimentos favoritos por comida.
    :return: DataFrame con las combinaciones de alimentos por comida.
    """
    combinaciones = []

    for index, row in distribucion.iterrows():
        comida = row["Comida"]
        calorias = row["Calorías"]
        proteinas = row["Proteínas"]
        hidratos = row["Hidratos"]
        grasas = row["Grasas"]

        favoritos_comida = favoritos.get(comida, {"proteinas": [], "hidratos": [], "grasas": []})
        alimentos_comida = alimentos[alimentos["Alimento"].isin(favoritos_comida["proteinas"] + favoritos_comida["hidratos"] + favoritos_comida["grasas"])]

        if alimentos_comida.empty:
            st.warning(f"No se encontraron alimentos favoritos para {comida}. Usando todos los alimentos disponibles.")
            alimentos_comida = alimentos

        for i in range(3):  # Generar solo 3 opciones distintas
            combinacion = {"Comida": comida, "Opción": f"Opción {i+1}"}
            alimentos_seleccionados = seleccionar_alimentos(alimentos_comida, calorias, proteinas, hidratos, grasas)
            combinacion["Alimentos"] = ", ".join(alimentos_seleccionados)
            combinaciones.append(combinacion)

    return pd.DataFrame(combinaciones)
