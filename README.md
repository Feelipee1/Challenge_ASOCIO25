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

3. Instalar solvers:
- CBC: Descargar de [COIN-OR](https://projects.coin-or.org/Cbc)
- Gurobi: Descargar desde [Gurobi](https://www.gurobi.com/)
- Mosek: Descargar desde [Mosek](https://www.mosek.com/)

## Uso

1. Colocar archivos de datos en la carpeta `data/`
2. Ejecutar:
```bash
python src/main.py
```

## Estructura del Proyecto

- `data/`: Archivos de entrada y recursos
- `src/`: Código fuente
  - `data/`: Módulos de datos
  - `optimizer/`: Lógica de optimización
  - `visualization/`: Visualizaciones
- `venv/`: Entorno virtual
- `requirements.txt`: Dependencias
- `README.md`: Documentación

## Utilizar Gurobi

✅ Ventajas de usar Gurobi
Rendimiento sobresaliente:
Gurobi es uno de los solvers más rápidos y potentes del mercado para programación lineal y entera (MILP), ideal para problemas de asignación y optimización combinatoria como este.

Capacidad de manejar restricciones complejas:
Puedes modelar fácilmente condiciones como:

compatibilidad entre escritorios y empleados,

días preferidos de asistencia,

mantener cercanía de equipos por zonas,

minimizar cambios de escritorio entre días.

Interfaz con Python (gurobipy):
Su API en Python es muy intuitiva, poderosa y bien documentada, lo que te permite:

crear modelos rápidamente,

modificar dinámicamente datos de entrada,

obtener estadísticas de solución.

Licencia académica gratuita:
Gurobi ofrece licencias gratuitas para estudiantes y uso académico (solo necesitas registrarte con correo .edu o institucional).

📌 Consideraciones
Si optas por usar Gurobi, asegúrate de que tu solución sea modular y parametrizable, para que se pueda adaptar fácilmente a las 10 instancias del reto.

Como te piden entregar el proyecto en un repositorio, es útil agregar un README.md que explique cómo instalar Gurobi y ejecutar tu script.

Por si acaso algún jurado no puede usar Gurobi, puedes preparar una versión alternativa con un solver libre (como CBC o HiGHS en PuLP), aunque esto es opcional.