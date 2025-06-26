"""

"""
import json
import os
import sys
from src.data.load_data import preparar_datos_desde_json
from src.optimizer.model.model import construir_modelo_pyomo
from pyomo.environ import *
from src.visualization.visualization import presentar_resultados
from pyomo.environ import value

# Función que construye el modelo de optimización en Pyomo
def construir_modelo_pyomo_relajado(param):
    model_relajado = ConcreteModel()

    # Conjuntos
    model_relajado.E = Set(initialize=param["Employees"])  # Empleados
    model_relajado.D = Set(initialize=param["Days"])       # Días laborales
    model_relajado.K = Set(initialize=param["Desks"])      # Escritorios
    model_relajado.G = Set(initialize=param["Groups"])     # Grupos
    model_relajado.Z = Set(initialize=param["Zones"])      # Zonas

    # Parámetros
    Desks_E = param["Desks_E"]
    Preferencias_E = param["Days_E"]  # Se interpreta como preferencias
    Empleado_Grupo = param["Empleado_Grupo"]
    Escritorio_Zona = param["Escritorio_Zona"]
    
    # Precalcular qué empleados son compatibles con cada escritorio
    empleados_por_escritorio = {
        k: [e for e in param["Employees"] if k in param["Desks_E"][e]]
        for k in param["Desks"]
    }

    # Variables
    model_relajado.x = Var(model_relajado.E, model_relajado.D, domain=UnitInterval)                
    model_relajado.y = Var(model_relajado.E, model_relajado.D, model_relajado.K, domain=UnitInterval)       
    model_relajado.z = Var(model_relajado.E, model_relajado.K, domain=UnitInterval)                
    model_relajado.reunion = Var(model_relajado.G, model_relajado.D, domain=UnitInterval)          
    model_relajado.u = Var(model_relajado.G, model_relajado.Z, model_relajado.D, domain=UnitInterval)

    # --- RESTRICCIONES ---

    # Variable de holgura
    model_relajado.slack = Var(model_relajado.E, domain=NonNegativeIntegers)

    # Definir constantes de días mínimos y máximos de asistencia
    MIN_DIAS = 2 # Cada empleado debe asistir al menos 2 días
    MAX_DIAS = 3 # Cada empleado puede asistir como máximo 3 días

    # Cada empleado debe asistir entre 2 y 3 días presenciales, permitiendo slack solo si no llega al mínimo
    def restric_dias_presenciales_min(model_relajado, e):
        return sum(model_relajado.x[e, d] for d in model_relajado.D) + model_relajado.slack[e] >= MIN_DIAS
    model_relajado.r1a = Constraint(model_relajado.E, rule=restric_dias_presenciales_min)
    
    def restric_dias_presenciales_max(model_relajado, e):
        return sum(model_relajado.x[e, d] for d in model_relajado.D) <= MAX_DIAS
    model_relajado.r1b = Constraint(model_relajado.E, rule=restric_dias_presenciales_max)

    # Si asiste un día, debe tener un único escritorio compatible
    def restric_escritorio_unico(model_relajado, e, d):
        return sum(model_relajado.y[e, d, k] for k in Desks_E[e]) == model_relajado.x[e, d]
    model_relajado.r2 = Constraint(model_relajado.E, model_relajado.D, rule=restric_escritorio_unico)
    
    # Preferencia blanda: se busca que cada empleado use un único escritorio todos los días presenciales.
    def escritorio_unico_duro(model_relajado, e):
        return sum(model_relajado.z[e, k] for k in Desks_E[e]) <= 1
    # Restricción dura: cada empleado usa máximo un escritorio
    model_relajado.r11 = Constraint(model_relajado.E, rule=escritorio_unico_duro)
    
    # Un escritorio no puede asignarse a más de una persona el mismo día
    def restric_escritorio_no_compartido(model_relajado, d, k):
        return sum(model_relajado.y[e, d, k] for e in empleados_por_escritorio[k]) <= 1
    model_relajado.r3 = Constraint(model_relajado.D, model_relajado.K, rule=restric_escritorio_no_compartido)


    # Activar z[e,k] si el escritorio fue usado por ese empleado al menos una vez
    def activar_z(model_relajado, e, k):
        if k in Desks_E[e]:
            return sum(model_relajado.y[e, d, k] for d in model_relajado.D) <= len(model_relajado.D) * model_relajado.z[e, k]
        else:
            return Constraint.Skip
    model_relajado.r4 = Constraint(model_relajado.E, model_relajado.K, rule=activar_z)

    # Cada grupo debe tener exactamente un día de reunión
    def reunion_un_dia(model_relajado, g):
        return sum(model_relajado.reunion[g, d] for d in model_relajado.D) == 1
    model_relajado.r5 = Constraint(model_relajado.G, rule=reunion_un_dia)

    # Todos los miembros del grupo deben asistir el día de la reunión
    def asistencia_reunion(model_relajado, e, d):
        g = Empleado_Grupo[e]
        return model_relajado.x[e, d] >= model_relajado.reunion[g, d]
    model_relajado.r6 = Constraint(model_relajado.E, model_relajado.D, rule=asistencia_reunion)

    # Activar zona si hay empleados del grupo trabajando allí en ese día
    def activar_u(model_relajado, g, z, d):
        empleados = [e for e in model_relajado.E if Empleado_Grupo[e] == g]
        escritorios = [k for k in model_relajado.K if Escritorio_Zona[k] == z]
        return sum(model_relajado.y[e, d, k] for e in empleados for k in escritorios if k in Desks_E[e]) <= 1000 * model_relajado.u[g, z, d]
    model_relajado.r7 = Constraint(model_relajado.G, model_relajado.Z, model_relajado.D, rule=activar_u)

    # Cada grupo puede usar máximo 2 zonas por día
    def max_dos_zonas(model_relajado, g, d):
        return sum(model_relajado.u[g, z, d] for z in model_relajado.Z) <= 2
    model_relajado.r8 = Constraint(model_relajado.G, model_relajado.D, rule=max_dos_zonas)
    

    def evitar_aislamiento_directo(model_relajado, g, z, d):
        empleados = [e for e in model_relajado.E if Empleado_Grupo[e] == g]
        escritorios = [k for k in model_relajado.K if Escritorio_Zona[k] == z]
        return sum(model_relajado.y[e, d, k] for e in empleados for k in escritorios if k in Desks_E[e]) >= 2 * model_relajado.u[g, z, d]
    model_relajado.r10_directa = Constraint(model_relajado.G, model_relajado.Z, model_relajado.D, rule=evitar_aislamiento_directo)


    # --- FUNCIÓN OBJETIVO ---

    dias_preferidos = [(e, d) for e in model_relajado.E for d in Preferencias_E[e]]
    dias_no_preferidos = [(e, d) for e in model_relajado.E for d in model_relajado.D if d not in Preferencias_E[e]]

    # Pesos
    P1, P3, P4 = 10, 5, 100

    # Penalización de slack en la función objetivo
    P5 = 100

    model_relajado.obj = Objective(
        expr=(
            + P4 * sum(model_relajado.x[e, d] for (e, d) in dias_preferidos)
            - P1 * sum(model_relajado.x[e, d] for (e, d) in dias_no_preferidos)
            - P3 * sum(model_relajado.u[g, z, d] for g in model_relajado.G for z in model_relajado.Z for d in model_relajado.D)
            - P5 * sum(model_relajado.slack[e] for e in model_relajado.E)

        ),
        sense=maximize
    )
    

    return model_relajado

