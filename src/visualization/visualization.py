"""
Modulo para presentar los resultados de la asignación de días y escritorios.
"""

from collections import defaultdict

def presentar_resultados(modelo, param, MIN_DIAS=2, MAX_DIAS=3):
    print("\n📋 ASIGNACIÓN POR EMPLEADO:")
    for e in modelo.E:
        dias_asignados = []
        escritorios_usados = set()

        for d in param["Days"]:
            if d in param["Days_E"][e] and round(modelo.x[e, d].value) == 1:
                asignado = False
                for k in param["Desks_E"][e]:
                    if round(modelo.y[e, d, k].value) == 1:
                        dias_asignados.append((d, k))
                        escritorios_usados.add(k)
                        asignado = True
                        break
                if not asignado:
                    dias_asignados.append((d, "⚠️ Sin escritorio"))

        if dias_asignados:
            print(f"\n👤 {e} ({len(dias_asignados)} día(s) asignado(s))")
            for d, k in sorted(dias_asignados):
                print(f"   📆 {d}: 🪑 {k}")
        else:
            print(f"\n❌ {e}: No tiene días asignados")

        if len(escritorios_usados) > 1:
            print(f"   🔁 Usó múltiples escritorios: {sorted(escritorios_usados)}")
        elif len(escritorios_usados) == 1:
            print(f"   🪑 Escritorio único: {list(escritorios_usados)[0]}")
        else:
            print("   ⚠️ Ningún escritorio asignado")

    print("\n📅 ASIGNACIONES POR DÍA:")
    asignaciones_por_dia = defaultdict(list)
    for e in modelo.E:
        for d in param["Days"]:
            if d in param["Days_E"][e] and round(modelo.x[e, d].value) == 1:
                asignaciones_por_dia[d].append(e)
    for d in param["Days"]:
        empleados = asignaciones_por_dia[d]
        print(f"📆 {d}: {len(empleados)} empleados → {empleados}")

    print("\n🧑‍🤝‍🧑 ASISTENCIA A REUNIONES DE GRUPO:")
    for g in modelo.G:
        encontro = False
        for d in modelo.D:
            if round(modelo.reunion[g, d].value) == 1:
                encontro = True
                miembros = param["Employees_G"][g]
                faltaron = [e for e in miembros if round(modelo.x[e, d].value) != 1]
                if faltaron:
                    print(f"❌ Grupo {g} tuvo reunión el {d}, faltaron: {faltaron}")
                else:
                    print(f"✅ Grupo {g} tuvo reunión completa el {d}")
        if not encontro:
            print(f"⚠️ Grupo {g} no tiene día de reunión asignado")

    print("\n📍 ZONAS USADAS POR GRUPO:")
    for g in modelo.G:
        for d in modelo.D:
            zonas = [z for z in modelo.Z if round(modelo.u[g, z, d].value) == 1]
            if zonas:
                print(f"Grupo {g} el {d} está en zonas: {zonas}")
                if len(zonas) > 2:
                    print(f"⚠️ Exceso de zonas: {len(zonas)}")

    print("\n📛 EMPLEADOS CON DÍAS NO PREFERIDOS:")
    for e in modelo.E:
        dias_forzados = [d for d in param["Days"] if d not in param["Days_E"][e] and round(modelo.x[e, d].value) == 1]
        if dias_forzados:
            print(f"⚠️ {e}: días no preferidos asignados → {dias_forzados}")

    print("\n🧾 VALIDACIÓN DE DÍAS MÍNIMOS Y USO DE SLACK:")
    
    empleados_con_slack_o_incompletos = []
    
    for e in modelo.E:
        asignados = sum(round(modelo.x[e, d].value) for d in modelo.D)
        slack = round(modelo.slack[e].value)
        total_con_slack = asignados + slack
    
        if slack > 0 or total_con_slack < MIN_DIAS:
            empleados_con_slack_o_incompletos.append((e, asignados, slack, total_con_slack))
    
    if empleados_con_slack_o_incompletos:
        for e, asignados, slack, total in empleados_con_slack_o_incompletos:
            estado = "❌" if total < MIN_DIAS else "⚠️"
            print(f"{estado} {e}: {asignados} días asignados + slack {slack} → total: {total} (mínimo requerido: {MIN_DIAS})")
    else:
        print("✅ Todos los empleados cumplen con el mínimo de días presenciales sin requerir slack.")

    print("\n🚨 VALIDACIÓN DE AISLAMIENTO POR ZONA (por grupo y día):")
    
    for g in modelo.G:
        miembros = param["Employees_G"][g]
        for d in modelo.D:
            zonas_usadas = defaultdict(list)
    
            # Construir la asignación de empleados a zonas
            for e in miembros:
                for k in param["Desks_E"][e]:
                    if round(modelo.y[e, d, k].value) == 1:
                        z = param["Escritorio_Zona"][k]
                        zonas_usadas[z].append(e)
                        break  # solo un escritorio por día
    
            # Revisar si hay zonas con solo 1 empleado (aislamiento)
            zonas_aisladas = {z: emps for z, emps in zonas_usadas.items() if len(emps) == 1}
    
            if zonas_aisladas:
                for z, emp in zonas_aisladas.items():
                    print(f"⚠️ {emp[0]} del grupo {g} está solo en la zona {z} el día {d}")
            else:
                if zonas_usadas:
                    resumen = "; ".join(
                        f"zona {z}: {emps}" for z, emps in zonas_usadas.items()
                    )
                    print(f"✅ Grupo {g} el día {d} tiene buena distribución → {resumen}")


    total_empleados = len(modelo.E)
    total_asignaciones = sum(round(modelo.x[e, d].value) for e in modelo.E for d in modelo.D)
    total_slack = sum(round(modelo.slack[e].value) for e in modelo.E)

    print("\n📊 RESUMEN GENERAL:")
    print(f"👥 Empleados totales: {total_empleados}")
    print(f"📆 Días asignados: {total_asignaciones}")
    print(f"⏳ Slack total: {total_slack}")
    print(f"✅ ¿Asignación dentro del rango permitido?: {MIN_DIAS * total_empleados <= total_asignaciones <= MAX_DIAS * total_empleados}")