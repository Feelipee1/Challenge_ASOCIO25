"""
Codigo principal del optimizador de puestos de trabajo (ASOCIO 2025)
Este script permite al usuario seleccionar una instancia de datos, 
establecer un tiempo límite para la solución y ejecutar un modelo de optimización para asignar empleados a escritorios, 
considerando restricciones de días, zonas y reuniones.
"""

import json
import os
import sys
from src.data.load_data import preparar_datos_desde_json
from src.optimizer.model.model import construir_modelo_pyomo
from pyomo.environ import *
from src.visualization.visualization import presentar_resultados
from pyomo.environ import value
from src.visualization.display import exportar_resultados_excel

def main():
    print("🎯 BIENVENIDO AL OPTIMIZADOR DE PUESTOS DE TRABAJO (ASOCIO 2025) 🎯\n")

    # Mostrar opciones al usuario
    print("📂 Selección de instancia disponible (instance1.json a instance10.json)")
    while True:
        try:
            instancia_num = int(input("🔢 Ingresa el número de la instancia que deseas cargar (1-10): "))
            if instancia_num < 1 or instancia_num > 10:
                raise ValueError
            break
        except ValueError:
            print("⚠️ Por favor, ingresa un número válido entre 1 y 10.\n")

    print("\n⏱️ Establecer tiempo límite de ejecución")
    while True:
        try:
            tiempo_limite = int(input("⏰ Ingresa el tiempo máximo de solución en segundos (por ejemplo, 900): "))
            if tiempo_limite <= 0:
                raise ValueError
            break
        except ValueError:
            print("⚠️ Ingresa un número entero positivo.\n")

    # Mostrar mensaje sobre el solver
    print("\n⚙️ Se usará por defecto el solver: CPLEX")
    print("📌 Si deseas usar otro solver como Gurobi o MOSEK, modifica el código fuente en esta función.")

    # Cargar la instancia seleccionada
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    nombre_archivo = f"instance{instancia_num}.json"
    ruta_instancia = os.path.join(base_dir, "data", nombre_archivo)

    if not os.path.exists(ruta_instancia):
        print(f"❌ No se encontró el archivo: {ruta_instancia}")
        return

    with open(ruta_instancia, "r", encoding="utf-8") as f:
        datos = json.load(f)
    param = preparar_datos_desde_json(datos)

    # Crear solver
    cplex_path = os.path.join(base_dir, "src", "optimizer", "solvers", "cplex", "cplex.exe")
    solver = SolverFactory("cplex", executable=cplex_path)
    solver.options["mipgap"] = 0.05
    solver.options["timelimit"] = tiempo_limite
    solver.options["solutiontype"] = 2
    solver.options["workmem"] = 2048

    # Construir modelo y resolver
    print("\n🚧 Construyendo el modelo...")
    modelo = construir_modelo_pyomo(param)

    print("\n🚀 Ejecutando el solver...")
    results = solver.solve(modelo, tee=True)

    # Presentar y exportar resultados
    presentar_resultados(modelo, param)

    nombre_salida = f"output/instance{instancia_num}_{tiempo_limite}s_resultado.xlsx"
    exportar_resultados_excel(modelo, param, ruta_salida=nombre_salida)

    print(f"\n📦 Resultados guardados en: {nombre_salida}")
    print("✅ Optimización finalizada. ¡Gracias por usar el sistema!\n")

if __name__ == "__main__":
    main()