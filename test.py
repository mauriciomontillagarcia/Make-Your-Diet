import pandas as pd

# Cargar el archivo CSV 'alimentos.csv'
df_alimentos = pd.read_csv('data/alimentos.csv')

# Verificar si la columna 'Mezcla' existe en el DataFrame
if 'Mezcla' not in df_alimentos.columns:
    print("La columna 'Mezcla' no existe en el DataFrame.")
else:
    print("La columna 'Mezcla' existe en el DataFrame.")

# Mostrar las primeras filas del DataFrame para verificar
print(df_alimentos.head())