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
from src.optimizer.heuristics.Inicial_heuristic import construir_heuristica, verificar_heuristica
from src.optimizer.heuristics.Slack_heuristic import ajustar_slack
from src.optimizer.heuristics.Alternativa_heuristic import construir_heuristica_alternativa


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    # Configuración inicial usando la librería os
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_instancia = os.path.join(base_dir, "data", "instance1.json")
    # Cargar y procesar datos
    with open(ruta_instancia, "r", encoding="utf-8") as f:
        datos = json.load(f)
    param = preparar_datos_desde_json(datos)
    
    # Construir y resolver el modelo
    modelo = construir_modelo_pyomo(param)

    # x_heur, y_heur = construir_heuristica(param)

    # if verificar_heuristica(modelo, x_heur, y_heur):
    #     for (e, d), val in x_heur.items():
    #             modelo.x[e, d].value = val
    #     for (e, d, k), val in y_heur.items():
    #             modelo.y[e, d, k].value = val

    #     # Ajustar slack basándose en x_heur
    #     slack_heur = ajustar_slack(param, x_heur)
    #     for e, val in slack_heur.items():
    #             modelo.slack[e].value = val

    #     print("✅ Heurística válida cargada.")
    # else:
    #     print("❌ Heurística rechazada. No se asignará como punto inicial.")

    x_heur, y_heur = construir_heuristica_alternativa(param)

    if verificar_heuristica(modelo, x_heur, y_heur):
        for (e, d), val in x_heur.items():
            modelo.x[e, d].value = val
        for (e, d, k), val in y_heur.items():
            modelo.y[e, d, k].value = val
        print("✅ Heurística alternativa válida cargada.")
    else:
        print("❌ Heurística alternativa rechazada.")


    mosek_path = os.path.join(base_dir, "src", "optimizer", "solvers", "mosek", "mosek.exe")
    gurobi_path = os.path.join(base_dir, "src", "optimizer", "solvers", "gurobi", "gurobi.exe")
    cplex_path = os.path.join(base_dir, "src", "optimizer", "solvers", "cplex", "cplex.exe")

    # Seleccionar el solver
    use_solver = 1 # 2 para cplex, 1 para Gurobi, 0 para MOSEK.

    if use_solver == 1:
        solver = SolverFactory("gurobi", executable=gurobi_path)
    elif use_solver == 2:
        solver = SolverFactory("cplex", executable=cplex_path)
    else:
        solver = SolverFactory("mosek_direct", executable=mosek_path)

    results = solver.solve(modelo, tee=True, warmstart=True)

    print("🔎 Estado del solver:")
    print(f"  Status: {results.solver.status}")
    print(f"  Termination condition: {results.solver.termination_condition}")
    
    # Presentar resultados
    presentar_resultados(modelo, param)

if __name__ == "__main__":
    main()

