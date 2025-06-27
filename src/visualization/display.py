import pandas as pd
import os

def exportar_resultados_excel(modelo, param, ruta_salida="resultados.xlsx"):
    """
    Exporta las asignaciones de días, escritorios y reuniones a un archivo Excel.
    """
    # Crear carpeta de salida si no existe
    carpeta = os.path.dirname(ruta_salida)
    if carpeta and not os.path.exists(carpeta):
        os.makedirs(carpeta)

    asignaciones = []

    for e in modelo.E:
        for d in modelo.D:
            if d in param["Days_E"][e] and round(modelo.x[e, d].value) == 1:
                escritorio = "Sin asignar"
                for k in param["Desks_E"][e]:
                    if round(modelo.y[e, d, k].value) == 1:
                        escritorio = k
                        break
                zona = param["Escritorio_Zona"].get(escritorio, "Desconocida") if escritorio != "Sin asignar" else "N/A"
                asignaciones.append({
                    "Empleado": e,
                    "Día": d,
                    "Escritorio": escritorio,
                    "Zona": zona
                })

    df_asignaciones = pd.DataFrame(asignaciones)
    df_asignaciones.sort_values(by=["Empleado", "Día"], inplace=True)

    # Reuniones por grupo
    reuniones = []
    for g in modelo.G:
        for d in modelo.D:
            if round(modelo.reunion[g, d].value) == 1:
                reuniones.append({
                    "Grupo": g,
                    "Día de Reunión": d
                })

    df_reuniones = pd.DataFrame(reuniones)

    # Slack por empleado
    slack = []
    for e in modelo.E:
        slack.append({
            "Empleado": e,
            "Slack usado": round(modelo.slack[e].value)
        })

    df_slack = pd.DataFrame(slack)

    # Escribir en Excel
    with pd.ExcelWriter(ruta_salida, engine="openpyxl") as writer:
        df_asignaciones.to_excel(writer, sheet_name="Asignaciones", index=False)
        df_reuniones.to_excel(writer, sheet_name="Reuniones", index=False)
        df_slack.to_excel(writer, sheet_name="Slack", index=False)

    print(f"✅ Resultados exportados a: {os.path.abspath(ruta_salida)}")
