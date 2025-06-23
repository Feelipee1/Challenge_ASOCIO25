"""
En este archivo se cargan los datos necesarios para el modelo matemático.
"""

import os
import json

def preparar_datos_desde_json(instancia_json: dict):
    # Extraer listas y diccionarios del JSON
    Employees = instancia_json["Employees"]
    Desks = instancia_json["Desks"]
    Days = instancia_json["Days"]
    Groups = instancia_json["Groups"]
    Zones = instancia_json["Zones"]
    Desks_Z = instancia_json["Desks_Z"]       # Escritorios por zona
    Desks_E = instancia_json["Desks_E"]       # Escritorios compatibles por empleado
    Employees_G = instancia_json["Employees_G"]  # Empleados por grupo
    Days_E = instancia_json["Days_E"]         # Días disponibles por empleado

    # Relacionar cada escritorio con su zona
    Escritorio_Zona = {}
    for z, lista in Desks_Z.items():
        for d in lista:
            Escritorio_Zona[d] = z

    # Relacionar cada empleado con su grupo
    Empleado_Grupo = {}
    for g, lista in Employees_G.items():
        for e in lista:
            Empleado_Grupo[e] = g

    # Retornar diccionario con todos los parámetros del modelo
    return {
        "Employees": Employees,
        "Desks": Desks,
        "Days": Days,
        "Groups": Groups,
        "Zones": Zones,
        "Desks_E": Desks_E,
        "Desks_Z": Desks_Z,
        "Escritorio_Zona": Escritorio_Zona,
        "Days_E": Days_E,
        "Employees_G": Employees_G,
        "Empleado_Grupo": Empleado_Grupo
    }


