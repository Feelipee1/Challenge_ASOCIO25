def ajustar_slack(param, x_heur):
    """
    Ajusta solo el slack necesario para los empleados que no alcanzan los días mínimos.
    Retorna {e: slack[e]} solo si requiere slack (> 0).
    """
    MIN_DIAS = 2
    slack_heur = {}

    for e in param["Employees"]:
        dias_asignados = sum(1 for d in param["Days"] if x_heur.get((e, d), 0) == 1)
        slack = MIN_DIAS - dias_asignados
        if slack > 0:
            slack_heur[e] = slack  # Solo asignar si realmente necesita slack

    return slack_heur
