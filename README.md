## Explicacion del modelo github

📁 Challenge_ASOCIO25/
Es la carpeta raíz del proyecto. Todo lo que desarrolles debe estar aquí dentro.

📁 data/
Contiene los archivos de entrada, por ejemplo los .json

📁 src/
Contiene todo el código fuente del proyecto.

📁 src/data/

- funciones de lectura, validación y transformación de datos, por ejemplo:

'''

def cargar_datos_json(nombre_archivo):
    # lee el archivo y devuelve estructuras en Python
📁 src/optimizer/model/
Aquí va la lógica del modelo de optimización, en este caso usando Gurobi.

model.py: es donde construirás el modelo matemático (variables, restricciones y función objetivo).

Podrías tener también un solver.py que ejecute la solución y devuelva resultados.

📁 src/visualization/
Si quieres agregar herramientas visuales (mostrar un mapa de escritorios y asignaciones) funciones con matplotlib, seaborn, o plotly.

📄 src/main.py
Es el script principal que se ejecutará

Cargar los datos.

Construir y resolver el modelo.

Imprimir/exportar los resultados.

if __name__ == "__main__":
    # Ejecuta todo el flujo


📄 .gitignore
Lista de archivos/carpetas que no quieres subir a GitHub, por ejemplo:

- __pycache__/
- *.log
- .env
- *.pyc

requirements.txt:

gurobipy
pandas
numpy

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