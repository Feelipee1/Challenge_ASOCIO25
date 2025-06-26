"""
Vamos a crear una heurística inicial que nos permita
resolver el problema de asignación de escritorios y zonas de trabajo de manera rápida y eficiente.
"""

def construir_heuristica(param):
    """
    Construye una solución inicial basada en:
    - Días preferidos (priorizando los primeros disponibles).
    - Mantener el mismo escritorio para cada empleado si es posible.
    Retorna diccionarios con claves (e,d) para x y (e,d,k) para y.
    """
    x_heur = {}
    y_heur = {}

    empleados = param["Employees"]
    dias = param["Days"]
    preferencias = param["Days_E"]
    desks_e = param["Desks_E"]

    escritorios_ocupados = {d: set() for d in dias}

    for e in empleados:
        dias_asignados = 0
        escritorio_asignado = None

        for d in preferencias[e]:
            if dias_asignados >= 2:
                break

            # Si ya tiene un escritorio asignado, intenta usarlo
            if escritorio_asignado:
                if escritorio_asignado not in escritorios_ocupados[d]:
                    x_heur[(e, d)] = 1
                    y_heur[(e, d, escritorio_asignado)] = 1
                    escritorios_ocupados[d].add(escritorio_asignado)
                    dias_asignados += 1
                    continue

            # Si no tiene escritorio aún o el que tenía no está disponible, busca uno libre
            for k in desks_e[e]:
                if k not in escritorios_ocupados[d]:
                    x_heur[(e, d)] = 1
                    y_heur[(e, d, k)] = 1
                    escritorios_ocupados[d].add(k)
                    escritorio_asignado = k
                    dias_asignados += 1
                    break

    return x_heur, y_heur

def verificar_heuristica(model, x_heur, y_heur):
    for (e, d), val in x_heur.items():
        if not (e in model.E and d in model.D):
            print(f"⚠️ x[{e},{d}] inválido")
            return False
    for (e, d, k), val in y_heur.items():
        if not (e in model.E and d in model.D and k in model.K):
            print(f"⚠️ y[{e},{d},{k}] inválido")
            return False
    return True

