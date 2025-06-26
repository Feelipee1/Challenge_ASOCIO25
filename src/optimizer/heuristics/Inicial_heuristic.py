"""
Vamos a crear una heurística inicial que nos permita
resolver el problema de asignación de escritorios y zonas de trabajo de manera rápida y eficiente.
"""

def construir_heuristica(param):
    """
    Construye una solución inicial factible basada en días preferidos y compatibilidad con escritorios.
    Retorna un diccionario con claves (e,d) para x, y (e,d,k) para y.
    """
    x_heur = {}
    y_heur = {}

    empleados = param["Employees"]
    dias = param["Days"]
    escritorios = param["Desks"]
    desks_e = param["Desks_E"]
    preferencias = param["Days_E"]

    escritorios_ocupados = {d: set() for d in dias}

    for e in empleados:
        dias_asignados = 0
        for d in preferencias[e]:
            if dias_asignados >= 2:
                break
            escritorio_disponible = next((k for k in desks_e[e] if k not in escritorios_ocupados[d]), None)
            if escritorio_disponible:
                x_heur[(e, d)] = 1
                y_heur[(e, d, escritorio_disponible)] = 1
                escritorios_ocupados[d].add(escritorio_disponible)
                dias_asignados += 1

    return x_heur, y_heur
