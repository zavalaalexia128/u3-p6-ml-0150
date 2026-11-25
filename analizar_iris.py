# ==========================================
# CASO 2: IDENTIFICACIÓN DE PROBLEMAS (SIMULADOS)
# DATASET: IRIS
# ==========================================
#Zavala Medina | NC= 0150
import pandas as pd
import numpy as np
import os

os.makedirs("resultados", exist_ok=True)
print("🌸 Iniciando análisis de Flores Iris...\n")

# 1. Cargar el archivo original
df_original = pd.read_csv("datos/iris.csv")

# 2. Crear una copia para "ensuciar" y probar
df_prueba = df_original.copy()

# ==========================================
# FASE A: SIMULACIÓN DE ERRORES (¡No tocar en producción real!)
# ==========================================
# Error 1: Dato nulo
df_prueba.loc[0, "sepal_length"] = np.nan

# Error 2: Registro duplicado (copiamos la fila 1 y la pegamos al final)
df_prueba = pd.concat([df_prueba, df_prueba.iloc[[1]]], ignore_index=True)

# Error 3: Tipo de dato incorrecto (metemos texto en columna numérica)
df_prueba["sepal_width"] = df_prueba["sepal_width"].astype(object)
df_prueba.loc[2, "sepal_width"] = "desconocido"

# Error 4: Valor atípico extremo
df_prueba.loc[5, "sepal_length"] = 1000.0 

# ==========================================
# FASE B: DETECCIÓN Y LIMPIEZA
# ==========================================
print("===== 1. DIMENSIONES TRAS 'ENSUCIAR' =====")
print(f"Filas: {df_prueba.shape[0]} (Debería ser 151 por el duplicado)\n")

print("===== 2. DETECCIÓN DE NULOS =====")
print(df_prueba.isnull().sum(), "\n")

print("===== 3. DETECCIÓN DE DUPLICADOS =====")
print(f"Duplicados encontrados: {df_prueba.duplicated().sum()}\n")

print("===== 4. REVISIÓN DE TIPOS DE DATOS =====")
print(df_prueba.dtypes, "\n")

# Truco para encontrar texto en columnas numéricas:
print("===== 5. FORZANDO CONVERSIÓN NUMÉRICA (Detecta errores) =====")
# 'coerce' convierte lo que no sea número en NaN
sepal_width_limpio = pd.to_numeric(df_prueba["sepal_width"], errors="coerce")
errores_tipo = sepal_width_limpio.isnull() & df_prueba["sepal_width"].notnull()
print(f"Filas con texto en lugar de número: {errores_tipo.sum()}\n")

print("===== 6. DETECCIÓN DE ATÍPICOS (Reglas de negocio) =====")
print("Valores de sepal_length mayores a 10 cm (imposible en Iris):")
print(df_prueba[df_prueba["sepal_length"] > 10], "\n")

# ==========================================
# FASE C: CORRECCIÓN
# ==========================================
df_corregido = df_prueba.copy()

# 1. Eliminar duplicados
df_corregido = df_corregido.drop_duplicates()

# 2. Corregir tipo de dato (el "desconocido" se volverá NaN)
df_corregido["sepal_width"] = pd.to_numeric(df_corregido["sepal_width"], errors="coerce")
df_corregido["sepal_length"] = pd.to_numeric(df_corregido["sepal_length"], errors="coerce")

# 3. Rellenar los NaN resultantes (tanto el simulado como el convertido) con la mediana
df_corregido["sepal_width"] = df_corregido["sepal_width"].fillna(df_corregido["sepal_width"].median())
df_corregido["sepal_length"] = df_corregido["sepal_length"].fillna(df_corregido["sepal_length"].median())

# 4. Guardar resultado
df_corregido.to_csv("resultados/iris_revisado.csv", index=False)
print("✅ Dataset corregido guardado en 'resultados/iris_revisado.csv'")
print("\n🎉 ¡Análisis del Caso 2 completado con éxito!")
print("Zavala Medina NC= 0150")