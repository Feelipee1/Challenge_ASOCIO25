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
from pyomo.solvers.plugins.solvers.mosek_direct import MOSEKDirect

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    # Configuración inicial usando la librería os
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_instancia = os.path.join(base_dir, "data", "instance3.json")
    # Cargar y procesar datos
    with open(ruta_instancia, "r", encoding="utf-8") as f:
        datos = json.load(f)
    param = preparar_datos_desde_json(datos)
    
    # Construir y resolver el modelo
    modelo = construir_modelo_pyomo(param)
    mosek_path = os.path.join(base_dir, "src", "optimizer", "solvers", "mosek", "mosek.exe")
    gurobi_path = os.path.join(base_dir, "src", "optimizer", "solvers", "gurobi", "gurobi.exe")
    cplex_path = os.path.join(base_dir, "src", "optimizer", "solvers", "cplex", "cplex.exe")

    # Seleccionar el solver
    use_solver = 2 # 1 para Gurobi, 0 para MOSEK.

    if use_solver == 1:
        solver = SolverFactory("gurobi", executable=gurobi_path)
    elif use_solver == 2:
        solver = SolverFactory("cplex", executable=cplex_path)
    else:
        solver = SolverFactory("mosek_direct", executable=mosek_path)

    results = solver.solve(modelo, tee=True)

    print("🔎 Estado del solver:")
    print(f"  Status: {results.solver.status}")
    print(f"  Termination condition: {results.solver.termination_condition}")
    
    # Presentar resultados
    presentar_resultados(modelo, param)

if __name__ == "__main__":
    main()

