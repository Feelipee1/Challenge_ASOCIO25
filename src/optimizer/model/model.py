"""
Este archivo define un modelo matemático de optimización usando Pyomo para asignar empleados a escritorios en una oficina,
considerando restricciones de asistencia mínima y máxima, preferencias de días, compatibilidad de escritorios, reuniones de grupo,
uso de zonas y evitando aislamiento de empleados. El objetivo es maximizar la satisfacción de preferencias y minimizar penalizaciones 
por incumplimiento de restricciones.
"""

from pyomo.environ import  *

def construir_modelo_pyomo(param):
    model = ConcreteModel()

    # Conjuntos
    model.E = Set(initialize=param["Employees"])  # Empleados
    model.D = Set(initialize=param["Days"])       # Días laborales
    model.K = Set(initialize=param["Desks"])      # Escritorios
    model.G = Set(initialize=param["Groups"])     # Grupos
    model.Z = Set(initialize=param["Zones"])      # Zonas

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
    model.x = Var(model.E, model.D, domain=Binary)                # Asistencia del empleado en el día
    model.y = Var(model.E, model.D, model.K, domain=Binary)       # Asignación de escritorio por día
    model.z = Var(model.E, model.K, domain=Binary)                # Si el empleado usó un escritorio alguna vez
    model.reunion = Var(model.G, model.D, domain=Binary)          # Día de reunión por grupo
    model.u = Var(model.G, model.Z, model.D, domain=Binary)       # Uso de zona por grupo y día

    # --- RESTRICCIONES ---

    # Variable de holgura
    model.slack = Var(model.E, domain=NonNegativeIntegers)

    # Definir constantes de días mínimos y máximos de asistencia
    MIN_DIAS = 2 # Cada empleado debe asistir al menos 2 días
    MAX_DIAS = 3 # Cada empleado puede asistir como máximo 3 días

    # Cada empleado debe asistir entre 2 y 3 días presenciales, permitiendo slack solo si no llega al mínimo
    def restric_dias_presenciales_min(model, e):
        return sum(model.x[e, d] for d in model.D) + model.slack[e] >= MIN_DIAS
    model.r1a = Constraint(model.E, rule=restric_dias_presenciales_min)
    
    def restric_dias_presenciales_max(model, e):
        return sum(model.x[e, d] for d in model.D) <= MAX_DIAS
    model.r1b = Constraint(model.E, rule=restric_dias_presenciales_max)

    # Si asiste un día, debe tener un único escritorio compatible
    def restric_escritorio_unico(model, e, d):
        return sum(model.y[e, d, k] for k in Desks_E[e]) == model.x[e, d]
    model.r2 = Constraint(model.E, model.D, rule=restric_escritorio_unico)
    
    # Preferencia blanda: se busca que cada empleado use un único escritorio todos los días presenciales.
    def escritorio_unico_duro(model, e):
        return sum(model.z[e, k] for k in Desks_E[e]) <= 1
    # Restricción dura: cada empleado usa máximo un escritorio
    model.r11 = Constraint(model.E, rule=escritorio_unico_duro)
    
    # Un escritorio no puede asignarse a más de una persona el mismo día
    def restric_escritorio_no_compartido(model, d, k):
        return sum(model.y[e, d, k] for e in empleados_por_escritorio[k]) <= 1
    model.r3 = Constraint(model.D, model.K, rule=restric_escritorio_no_compartido)


    # Activar z[e,k] si el escritorio fue usado por ese empleado al menos una vez
    def activar_z(model, e, k):
        if k in Desks_E[e]:
            return sum(model.y[e, d, k] for d in model.D) <= len(model.D) * model.z[e, k]
        else:
            return Constraint.Skip
    model.r4 = Constraint(model.E, model.K, rule=activar_z)

    # Cada grupo debe tener exactamente un día de reunión
    def reunion_un_dia(model, g):
        return sum(model.reunion[g, d] for d in model.D) == 1
    model.r5 = Constraint(model.G, rule=reunion_un_dia)

    # Todos los miembros del grupo deben asistir el día de la reunión
    def asistencia_reunion(model, e, d):
        g = Empleado_Grupo[e]
        return model.x[e, d] >= model.reunion[g, d]
    model.r6 = Constraint(model.E, model.D, rule=asistencia_reunion)

    # Activar zona si hay empleados del grupo trabajando allí en ese día
    def activar_u(model, g, z, d):
        empleados = [e for e in model.E if Empleado_Grupo[e] == g]
        escritorios = [k for k in model.K if Escritorio_Zona[k] == z]
        return sum(model.y[e, d, k] for e in empleados for k in escritorios if k in Desks_E[e]) <= 1000 * model.u[g, z, d]
    model.r7 = Constraint(model.G, model.Z, model.D, rule=activar_u)

    # Cada grupo puede usar máximo 2 zonas por día
    def max_dos_zonas(model, g, d):
        return sum(model.u[g, z, d] for z in model.Z) <= 2
    model.r8 = Constraint(model.G, model.D, rule=max_dos_zonas)
    

    def evitar_aislamiento_directo(model, g, z, d):
        empleados = [e for e in model.E if Empleado_Grupo[e] == g]
        escritorios = [k for k in model.K if Escritorio_Zona[k] == z]
        return sum(model.y[e, d, k] for e in empleados for k in escritorios if k in Desks_E[e]) >= 2 * model.u[g, z, d]
    model.r10_directa = Constraint(model.G, model.Z, model.D, rule=evitar_aislamiento_directo)


    # --- FUNCIÓN OBJETIVO ---

    dias_preferidos = [(e, d) for e in model.E for d in Preferencias_E[e]]
    dias_no_preferidos = [(e, d) for e in model.E for d in model.D if d not in Preferencias_E[e]]

    # Pesos
    P1, P3, P4 = 10, 5, 100

    # Penalización de slack en la función objetivo
    P5 = 100

    model.obj = Objective(
        expr=(
            + P4 * sum(model.x[e, d] for (e, d) in dias_preferidos)
            - P1 * sum(model.x[e, d] for (e, d) in dias_no_preferidos)
            - P3 * sum(model.u[g, z, d] for g in model.G for z in model.Z for d in model.D)
            - P5 * sum(model.slack[e] for e in model.E)

        ),
        sense=maximize
    )

    return model