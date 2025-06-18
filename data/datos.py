"""
Este archivo es para definir las rutas de los datos que se utilizarán en el proyecto.
Con los archivos json
"""

import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Abrir un solo archivo JSON (por ejemplo, instance1.json)
with open("instance10.json", "r") as archivo:
    datos = json.load(archivo)

# Cargar los datos del archivo JSON

Employees = datos["Employees"] #Empleados
print("Empleados:", Employees)



Desks = datos["Desks"] #Escritorios

Days = datos["Days"] #Días

Groups = datos["Groups"] #Grupos de empleados

Zones = datos["Zones"] #Zonas

# Escritorios por zona
Desks_Z = datos["Desks_Z"]

zone_desks = {}
for zone, desks in Desks_Z.items():
    zone_desks[zone] = desks

# Ejemplo de acceso:
Z0_desks = zone_desks.get("Z0", [])
Z1_desks = zone_desks.get("Z1", [])

# Escritorios ue cada empleado prefiere

Desks_E = datos["Desks_E"]
desks_employees = {}
for employee, desks in Desks_E.items():
    desks_employees[employee] = desks

# Ejemplo de acceso:
# print("Escritorios preferidos del empleado E1:", desks_employees.get("E1", []))

# Enumeracion de grupos de empleados
Employees_G = datos["Employees_G"]
employees_groups = {}
for employee, group in Employees_G.items():
    employees_groups[employee] = group

# Ejemplo de acceso:
# print("Grupo 0:", employees_groups.get("G0"))

# Dias disponibles de cada empleado
Days_E = datos["Days_E"]
days_employees = {}
for employee, days in Days_E.items():
    days_employees[employee] = days

# Ejemplo de acceso:
# print("Días disponibles del empleado E1:", days_employees.get("E1", []))

## Analizar todo mediante un DataFrame

# Invertir Employees_G: de grupo -> [empleados] a empleado -> grupo
employees_groups = {}

for grupo, empleados in Employees_G.items():
    for empleado in empleados:
        employees_groups[empleado] = grupo

# Construir DataFrame con toda la información por empleado
empleados_data = []
for empleado in Employees:
    empleados_data.append({
        "Empleado": empleado,
        "Grupo": employees_groups.get(empleado, "No asignado"),
        "EscritoriosPreferidos": desks_employees.get(empleado, []),
        "DiasDisponibles": days_employees.get(empleado, [])
    })

df_empleados = pd.DataFrame(empleados_data)

# Mandar a archivo xlsx

df_empleados.to_excel("empleados_info.xlsx", index=False)

# Graficas

# Asegurarse de que DiasDisponibles esté en forma de lista
df_empleados["DiasDisponibles"] = df_empleados["DiasDisponibles"].apply(lambda x: x if isinstance(x, list) else [])

# Agregar una columna con el número de días disponibles
df_empleados["CantidadDias"] = df_empleados["DiasDisponibles"].apply(len)

# Días de la semana
dias_semana = ["L", "Ma", "Mi", "J", "V"]

# Expandir columnas binarias por día
for dia in dias_semana:
    df_empleados[dia] = df_empleados["DiasDisponibles"].apply(lambda x: dia in x)

# Grupos únicos
grupos_unicos = df_empleados["Grupo"].unique()

# Configuración general de estilo
sns.set(style="whitegrid")

# Crear un heatmap por grupo
for grupo in sorted(grupos_unicos):
    df_grupo = df_empleados[df_empleados["Grupo"] == grupo]
    df_matriz = df_grupo.set_index("Empleado")[dias_semana]

    plt.figure(figsize=(8, 4))
    sns.heatmap(df_matriz, annot=True, cmap="Greens", cbar=False, linewidths=0.5, linecolor='gray')

    plt.title(f"Días disponibles por empleado - Grupo {grupo}")
    plt.xlabel("Día de la semana")
    plt.ylabel("Empleado")
    plt.tight_layout()
    plt.show()















