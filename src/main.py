"""
Codigo para ejecutar todo el proyecto de optimizacion
"""
import json
from src.data.load_data import preparar_datos_desde_json
from src.optimizer.model import construir_modelo_pyomo
from pyomo.environ import *
from src.visualization.visualization import presentar_resultados
import os


def main():
    # Configuración inicial usando la librería os
    ruta_instancia = os.path.join("data", "instance1.json")
    
    # Cargar y procesar datos
    with open(ruta_instancia, "r", encoding="utf-8") as f:
        datos = json.load(f)
    param = preparar_datos_desde_json(datos)
    
    # Construir y resolver el modelo
    modelo = construir_modelo_pyomo(param)
    mosek_dir = os.path.join("src", "optimizer", "solvers", "mosek")
    mosek_path = os.path.abspath(os.path.join(mosek_dir, "mosek.exe"))
    os.environ["PATH"] = mosek_dir + os.pathsep + os.environ.get("PATH", "")
    solver = SolverFactory("mosek", executable=mosek_path)
    results = solver.solve(modelo, tee=True)
    
    # Presentar resultados
    presentar_resultados(modelo, param)

if __name__ == "__main__":
    main()

