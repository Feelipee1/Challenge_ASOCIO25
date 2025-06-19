"""
Codigo para ejecutar todo el proyecto de optimizacion
"""

from src.data.load_data import cargar_instancia_json

if __name__ == "__main__":
    # Por ejemplo, cargar la instancia 3
    numero = 3
    datos = cargar_instancia_json(numero)

    print(f"Empleados en la instancia {numero}: {datos['Employees']}")

