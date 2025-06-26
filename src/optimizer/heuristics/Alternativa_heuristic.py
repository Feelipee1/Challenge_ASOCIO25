def construir_heuristica_alternativa(param):
    """
    Heurística alternativa que asigna 2 días preferidos con el mismo escritorio,
    respetando disponibilidad por día.
    """
    x_heur = {}
    y_heur = {}

    empleados = param["Employees"]
    dias = param["Days"]
    escritorios = param["Desks"]
    desks_e = param["Desks_E"]
    preferencias = param["Days_E"]

    # Control de escritorios ocupados por día
    ocupados_dia_k = {d: set() for d in dias}

    for e in empleados:
        dias_pref = preferencias[e]
        posibles_k = sorted(desks_e[e], key=lambda k: sum(k in ocupados_dia_k[d] for d in dias))

        asignados = 0
        for k in posibles_k:
            dias_asignables = []
            for d in dias_pref:
                if k not in ocupados_dia_k[d]:
                    dias_asignables.append(d)
                if len(dias_asignables) == 2:
                    break
            if len(dias_asignables) >= 2:
                for d in dias_asignables:
                    x_heur[(e, d)] = 1
                    y_heur[(e, d, k)] = 1
                    ocupados_dia_k[d].add(k)
                    asignados += 1
                break  # Ya asignamos dos días
            elif len(dias_asignables) == 1:
                d = dias_asignables[0]
                x_heur[(e, d)] = 1
                y_heur[(e, d, k)] = 1
                ocupados_dia_k[d].add(k)
                asignados += 1
                break

    return x_heur, y_heur

