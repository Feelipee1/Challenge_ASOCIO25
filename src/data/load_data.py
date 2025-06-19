"""
En este archivo se cargan los datos necesarios para el modelo matemático.
"""

import os
import json

def cargar_instancia_json(numero_instancia, ruta_base='data'):
    """
    Carga un archivo JSON específico (por ejemplo, instance3.json) desde la carpeta de datos.

    Parámetros:
        numero_instancia (int): número de la instancia que deseas cargar.
        ruta_base (str): carpeta donde están los archivos JSON (por defecto 'data').

    Retorna:
        dict: datos contenidos en el archivo JSON seleccionado.
    """
    nombre_archivo = f'instance{numero_instancia}.json'
    ruta_completa = os.path.join(ruta_base, nombre_archivo)

    if not os.path.exists(ruta_completa):
        raise FileNotFoundError(f"No se encontró el archivo '{nombre_archivo}' en la ruta '{ruta_base}'.")

    with open(ruta_completa, 'r', encoding='utf-8') as archivo:
        datos = json.load(archivo)

    return datos


