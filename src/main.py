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
    ruta_instancia = r"D:\Challenge_ASOCIO25\data\instance1.json"
    # Cargar y procesar datos
    with open(ruta_instancia, "r", encoding="utf-8") as f:
        datos = json.load(f)
    param = preparar_datos_desde_json(datos)
    
    # Construir y resolver el modelo
    modelo = construir_modelo_pyomo(param)
    mosek_path = r"D:\Challenge_ASOCIO25\src\optimizer\solvers\mosek\mosek.exe"
    solver = SolverFactory("mosek", executable=mosek_path)
    results = solver.solve(modelo, tee=True)
    
    # Presentar resultados
    presentar_resultados(modelo, param)

if __name__ == "__main__":
    main()

