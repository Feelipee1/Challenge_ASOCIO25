# Optimización de Espacios de Trabajo

Sistema de optimización para la asignación de escritorios y zonas de trabajo.

## Instalación

1. Crear entorno virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

---

3. 🧰 Instalación de CPLEX (Recomendado)

Este proyecto usa **CPLEX** como solver principal, ya que no requiere licencia académica para uso local en problemas pequeños y es altamente eficiente.

### 🔽 Pasos para instalar CPLEX:

1. Crea una cuenta gratuita en IBM Research:
   👉 https://www.ibm.com/account/reg/us-en/signup?formid=urx-19776

2. Descarga IBM ILOG CPLEX Optimization Studio desde:
   👉 https://www.ibm.com/products/ilog-cplex-optimization-studio

3. Durante la instalación, selecciona una ruta accesible. Ejemplo típico en Windows:


## Uso

1. Colocar archivos de datos en la carpeta `data/`
2. Ejecutar:
```bash
python -m src.main
```

## Estructura del Proyecto

- `data/`: Archivos de entrada y recursos
- `src/`: Código fuente
  - `data/`: Módulos de datos
  - `optimizer/`: Lógica de optimización
    - `model/`: Modelo Matematico en Pyomo
    - `solvers/`: cplex.exe
  - `visualization/`: Visualizaciones
- `venv/`: Entorno virtual
- `requirements.txt`: Dependencias
- `README.md`: Documentación

## 📊 Salida de Resultados
Al finalizar la ejecución, el sistema genera automáticamente un archivo .xlsx con:

Hoja 1: Asignación de empleados por día y escritorio

Hoja 2: Reuniones de grupo asignadas

Hoja 3: Empleados que requirieron slack (por incumplimiento de días)

Además, los resultados se imprimen en consola con análisis por empleado, por día, por grupo y por zonas.

## 🧠 Notas Finales
El modelo puede tardar más tiempo en instancias grandes. Se recomienda comenzar con las instancias pequeñas para pruebas iniciales.

CPLEX es usado como solver predeterminado por su eficiencia y facilidad de integración.

El sistema está preparado para escalar a nuevas instancias sin requerir modificaciones al código fuente.

## Ejemplo 1 de respuesta para las Instances1.json

An optimal solution satisfying the relative gap tolerance of 1.00e-02(%) has been located.
The relative gap is 0.00e+00(%).
An optimal solution satisfying the absolute gap tolerance of 0.00e+00 has been located.
The absolute gap is 0.00e+00.

Objective of best integer solution : 3.210000000000e+03
Best objective bound               : 3.210000000000e+03
Initial feasible solution objective: Undefined
Construct solution objective       : Not employed
User objective cut value           : Not employed
Number of cuts generated           : 1335
  Number of Gomory cuts            : 185
  Number of CMIR cuts              : 114
  Number of clique cuts            : 447
  Number of knapsack_cover cuts    : 589
Number of branches                 : 68598
Number of relaxations solved       : 86389
Number of interior point iterations: 8
Number of simplex iterations       : 6414493
Time spend presolving the root     : 0.03
Time spend optimizing the root     : 0.02
Mixed integer optimizer terminated. Time: 106.42

Optimizer terminated. Time: 106.42  


Integer solution solution summary
  Problem status  : PRIMAL_FEASIBLE
  Solution status : INTEGER_OPTIMAL
  Primal.  obj: 3.2100000000e+03    nrm: 1e+03    Viol.  con: 4e-13    var: 7e-15    itg: 7e-15

📋 ASIGNACIÓN POR EMPLEADO:

👤 E0 (1 día(s) asignado(s))
   📆 Mi: 🪑 D7
   🪑 Escritorio único: D7

👤 E1 (2 día(s) asignado(s))
   📆 Ma: 🪑 D2
   📆 Mi: 🪑 D2
   🪑 Escritorio único: D2

👤 E2 (3 día(s) asignado(s))
   📆 L: 🪑 D0
   📆 Ma: 🪑 D0
   📆 Mi: 🪑 D0
   🪑 Escritorio único: D0

👤 E3 (2 día(s) asignado(s))
   📆 L: 🪑 D6
   📆 Mi: 🪑 D6
   🪑 Escritorio único: D6

👤 E4 (3 día(s) asignado(s))
   📆 L: 🪑 D1
   📆 Ma: 🪑 D1
   📆 Mi: 🪑 D1
   🪑 Escritorio único: D1

👤 E5 (1 día(s) asignado(s))
   📆 J: 🪑 D3
   🪑 Escritorio único: D3

👤 E6 (1 día(s) asignado(s))
   📆 J: 🪑 D1
   🪑 Escritorio único: D1

👤 E7 (2 día(s) asignado(s))
   📆 Ma: 🪑 D5
   📆 Mi: 🪑 D5
   🪑 Escritorio único: D5

👤 E8 (2 día(s) asignado(s))
   📆 J: 🪑 D0
   📆 V: 🪑 D0
   🪑 Escritorio único: D0

👤 E9 (2 día(s) asignado(s))
   📆 Ma: 🪑 D8
   📆 Mi: 🪑 D8
   🪑 Escritorio único: D8

👤 E10 (2 día(s) asignado(s))
   📆 L: 🪑 D4
   📆 Ma: 🪑 D4
   🪑 Escritorio único: D4

👤 E11 (2 día(s) asignado(s))
   📆 L: 🪑 D8
   📆 V: 🪑 D8
   🪑 Escritorio único: D8

👤 E12 (1 día(s) asignado(s))
   📆 J: 🪑 D2
   🪑 Escritorio único: D2

👤 E13 (1 día(s) asignado(s))
   📆 V: 🪑 D5
   🪑 Escritorio único: D5

👤 E14 (2 día(s) asignado(s))
   📆 L: 🪑 D3
   📆 Ma: 🪑 D3
   🪑 Escritorio único: D3

👤 E15 (2 día(s) asignado(s))
   📆 Mi: 🪑 D3
   📆 V: 🪑 D3
   🪑 Escritorio único: D3

👤 E16 (1 día(s) asignado(s))
   📆 Mi: 🪑 D4
   🪑 Escritorio único: D4

👤 E17 (1 día(s) asignado(s))
   📆 V: 🪑 D2
   🪑 Escritorio único: D2

👤 E18 (3 día(s) asignado(s))
   📆 J: 🪑 D7
   📆 Ma: 🪑 D7
   📆 V: 🪑 D7
   🪑 Escritorio único: D7

👤 E19 (2 día(s) asignado(s))
   📆 J: 🪑 D6
   📆 V: 🪑 D6
   🪑 Escritorio único: D6

📅 ASIGNACIONES POR DÍA:
📆 L: 6 empleados → ['E2', 'E3', 'E4', 'E10', 'E11', 'E14']
📆 Ma: 8 empleados → ['E1', 'E2', 'E4', 'E7', 'E9', 'E10', 'E14', 'E18']
📆 Mi: 9 empleados → ['E0', 'E1', 'E2', 'E3', 'E4', 'E7', 'E9', 'E15', 'E16']
📆 J: 6 empleados → ['E5', 'E6', 'E8', 'E12', 'E18', 'E19']
📆 V: 7 empleados → ['E8', 'E11', 'E13', 'E15', 'E17', 'E18', 'E19']

🧑‍🤝‍🧑 ASISTENCIA A REUNIONES DE GRUPO:
✅ Grupo G0 tuvo reunión completa el Mi
✅ Grupo G1 tuvo reunión completa el J
✅ Grupo G2 tuvo reunión completa el L
✅ Grupo G3 tuvo reunión completa el V

📍 ZONAS USADAS POR GRUPO:
Grupo G0 el L está en zonas: ['Z0', 'Z1']
Grupo G0 el Ma está en zonas: ['Z0']
Grupo G0 el Mi está en zonas: ['Z0', 'Z1']
Grupo G1 el Ma está en zonas: ['Z1']
Grupo G1 el Mi está en zonas: ['Z1']
Grupo G1 el J está en zonas: ['Z0', 'Z1']
Grupo G1 el V está en zonas: ['Z0']
Grupo G2 el L está en zonas: ['Z0', 'Z1']
Grupo G2 el Ma está en zonas: ['Z0']
Grupo G2 el J está en zonas: ['Z0']
Grupo G2 el V está en zonas: ['Z1']
Grupo G3 el Ma está en zonas: ['Z1']
Grupo G3 el Mi está en zonas: ['Z0']
Grupo G3 el J está en zonas: ['Z1']
Grupo G3 el V está en zonas: ['Z0', 'Z1']

📛 EMPLEADOS CON DÍAS NO PREFERIDOS:
⚠️ E0: días no preferidos asignados → ['L']
⚠️ E6: días no preferidos asignados → ['V']
⚠️ E7: días no preferidos asignados → ['J']
⚠️ E9: días no preferidos asignados → ['J']
⚠️ E10: días no preferidos asignados → ['J']
⚠️ E12: días no preferidos asignados → ['L']
⚠️ E13: días no preferidos asignados → ['L']
⚠️ E16: días no preferidos asignados → ['V']
⚠️ E19: días no preferidos asignados → ['Ma']

🧾 VALIDACIÓN DE DÍAS MÍNIMOS Y USO DE SLACK:
⚠️ E5: 1 días asignados + slack 1 → total: 2 (mínimo requerido: 2)
⚠️ E17: 1 días asignados + slack 1 → total: 2 (mínimo requerido: 2)

🚨 VALIDACIÓN DE AISLAMIENTO POR ZONA (por grupo y día):
✅ Grupo G0 el día L tiene buena distribución → zona Z1: ['E0', 'E3']; zona Z0: ['E2', 'E4']
✅ Grupo G0 el día Ma tiene buena distribución → zona Z0: ['E1', 'E2', 'E4']
✅ Grupo G0 el día Mi tiene buena distribución → zona Z1: ['E0', 'E3']; zona Z0: ['E1', 'E2', 'E4']
✅ Grupo G1 el día Ma tiene buena distribución → zona Z1: ['E7', 'E9']
✅ Grupo G1 el día Mi tiene buena distribución → zona Z1: ['E7', 'E9']
✅ Grupo G1 el día J tiene buena distribución → zona Z0: ['E5', 'E6', 'E8']; zona Z1: ['E7', 'E9']
✅ Grupo G1 el día V tiene buena distribución → zona Z0: ['E6', 'E8']
✅ Grupo G2 el día L tiene buena distribución → zona Z0: ['E10', 'E12', 'E14']; zona Z1: ['E11', 'E13']
✅ Grupo G2 el día Ma tiene buena distribución → zona Z0: ['E10', 'E14']
✅ Grupo G2 el día J tiene buena distribución → zona Z0: ['E10', 'E12']
✅ Grupo G2 el día V tiene buena distribución → zona Z1: ['E11', 'E13']
✅ Grupo G3 el día Ma tiene buena distribución → zona Z1: ['E18', 'E19']
✅ Grupo G3 el día Mi tiene buena distribución → zona Z0: ['E15', 'E16']
✅ Grupo G3 el día J tiene buena distribución → zona Z1: ['E18', 'E19']
✅ Grupo G3 el día V tiene buena distribución → zona Z0: ['E15', 'E16', 'E17']; zona Z1: ['E18', 'E19']

📊 RESUMEN GENERAL:
👥 Empleados totales: 20
📆 Días asignados: 45
⏳ Slack total: 2
✅ ¿Asignación dentro del rango permitido?: True