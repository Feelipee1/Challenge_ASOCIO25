"""
Codigo para ejecutar todo el proyecto de optimizacion
"""

import json
import os
import sys
from src.data.load_data import preparar_datos_desde_json
from src.optimizer.model.model import construir_modelo_pyomo
from pyomo.environ import *
from src.visualization.visualization import presentar_resultados
from src.optimizer.Inicial_solution.Inicial_solution import construir_modelo_pyomo_relajado
from pyomo.environ import value

# from src.optimizer.Inicial_solution.Inicial_solution import InicialSolution

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def resolver_relajado(param, use_solver=2):

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    modelo_relajado = construir_modelo_pyomo_relajado(param)

    mosek_path = os.path.join(base_dir, "src", "optimizer", "solvers", "mosek", "mosek.exe")
    gurobi_path = os.path.join(base_dir, "src", "optimizer", "solvers", "gurobi", "gurobi.exe")
    cplex_path = os.path.join(base_dir, "src", "optimizer", "solvers", "cplex", "cplex.exe")

    # Seleccionar el solver

    if use_solver == 1:
        solver = SolverFactory("gurobi", executable=gurobi_path)
    elif use_solver == 2:
        solver = SolverFactory("cplex", executable=cplex_path)
    else:
        solver = SolverFactory("mosek_direct", executable=mosek_path)

    results = solver.solve(modelo_relajado)

    return modelo_relajado

def inicializar_modelo_con_redondeo(modelo_relajado, modelo_binario, umbral=0.5):
    """
    Inicializa el modelo_binario con los valores redondeados del modelo_relajado.

    Args:
        modelo_relajado (ConcreteModel): Modelo con variables relajadas resuelto.
        modelo_binario (ConcreteModel): Modelo con variables binarias.
        umbral (float): Umbral de redondeo (por defecto 0.5).
    """
    no_inicializadas = 0

    # x
    for e in modelo_relajado.E:
        for d in modelo_relajado.D:
            try:
                val = value(modelo_relajado.x[e, d], exception=False)
                if val is not None:
                    modelo_binario.x[e, d].value = 1 if val >= umbral else 0
            except:
                no_inicializadas += 1

    # y
    for e in modelo_relajado.E:
        for d in modelo_relajado.D:
            for k in modelo_relajado.K:
                try:
                    val = value(modelo_relajado.y[e, d, k], exception=False)
                    if val is not None:
                        modelo_binario.y[e, d, k].value = 1 if val >= umbral else 0
                except:
                    no_inicializadas += 1

    # z
    for e in modelo_relajado.E:
        for k in modelo_relajado.K:
            try:
                val = value(modelo_relajado.z[e, k], exception=False)
                if val is not None:
                    modelo_binario.z[e, k].value = 1 if val >= umbral else 0
            except:
                no_inicializadas += 1

    # reunion
    for g in modelo_relajado.G:
        for d in modelo_relajado.D:
            try:
                val = value(modelo_relajado.reunion[g, d], exception=False)
                if val is not None:
                    modelo_binario.reunion[g, d].value = 1 if val >= umbral else 0
            except:
                no_inicializadas += 1

    # u
    for g in modelo_relajado.G:
        for z in modelo_relajado.Z:
            for d in modelo_relajado.D:
                try:
                    val = value(modelo_relajado.u[g, z, d], exception=False)
                    if val is not None:
                        modelo_binario.u[g, z, d].value = 1 if val >= umbral else 0
                except:
                    no_inicializadas += 1

    # slack
    for e in modelo_relajado.E:
        try:
            val = value(modelo_relajado.slack[e], exception=False)
            if val is not None:
                modelo_binario.slack[e].value = round(val)  # redondeo a entero
        except:
            no_inicializadas += 1

    print(f"✅ Inicialización completada. 🔢 Variables omitidas por falta de valor o error: {no_inicializadas}")

def main():
    # Configuración inicial usando la librería os
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_instancia = os.path.join(base_dir, "data", "instance5.json")
    # Cargar y procesar datos
    with open(ruta_instancia, "r", encoding="utf-8") as f:
        datos = json.load(f)
    param = preparar_datos_desde_json(datos)
    
    # Construir y resolver el modelo
    # modelo = construir_modelo_pyomo(param)

    mosek_path = os.path.join(base_dir, "src", "optimizer", "solvers", "mosek", "mosek.exe")
    gurobi_path = os.path.join(base_dir, "src", "optimizer", "solvers", "gurobi", "gurobi.exe")
    cplex_path = os.path.join(base_dir, "src", "optimizer", "solvers", "cplex", "cplex.exe")

    # Seleccionar el solver
    use_solver = 2 # 1 para Gurobi, 0 para MOSEK
   
    
    if use_solver == 1:
        solver = SolverFactory("gurobi", executable=gurobi_path)
    elif use_solver == 2:
        solver = SolverFactory("cplex", executable=cplex_path)
        solver.options["mipgap"] = 0.05  # Detenerse cuando el gap sea del 10%
    else:
        solver = SolverFactory("mosek_direct", executable=mosek_path)


    # Resolver el modelo relajado

    modelo_relajado = resolver_relajado(param, 2)

    modelo = construir_modelo_pyomo(param)

    # Inicializar el modelo con los valores redondeados del modelo relajado

    inicializar_modelo_con_redondeo(modelo_relajado, modelo, umbral=0.7)    
    
    results = solver.solve(modelo, tee=True)

    # Presentar resultados
    presentar_resultados(modelo, param)

    
if __name__ == "__main__":
    main()

