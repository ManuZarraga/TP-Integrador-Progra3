def restaurar_conectividad(componentes, conexiones_posibles):
    """
    Estrategia de Búsqueda Exhaustiva (Backtracking) [2].
    Busca la combinación mínima de aristas para unir todos los componentes.
    """
    mejor_solucion = None
    min_costo = float('inf')

    def backtrack(idx_inicio, conexiones_actuales, costo_actual, componentes_actuales):
        nonlocal mejor_solucion, min_costo

        # Caso Base: Si solo queda 1 componente, la red es conexa [3]
        if len(componentes_actuales) == 1:
            if costo_actual < min_costo:
                min_costo = costo_actual
                mejor_solucion = list(conexiones_actuales)
            return

        # Exploración de combinaciones de aristas candidatas
        for i in range(idx_inicio, len(conexiones_posibles)):
            u, v, peso = conexiones_posibles[i]
            
            # Verificar si esta arista une dos componentes distintos
            comp_u = next(c for c in componentes_actuales if u in c)
            comp_v = next(c for c in componentes_actuales if v in c)

            if comp_u != comp_v:
                # Paso: Unificar componentes
                nuevos_comp = [c for c in componentes_actuales if c != comp_u and c != comp_v]
                nuevos_comp.append(comp_u + comp_v)
                
                conexiones_actuales.append((u, v))
                backtrack(i + 1, conexiones_actuales, costo_actual + peso, nuevos_comp)
                
                # Retroceso (Backtrack): Quitar la última decisión
                conexiones_actuales.pop()

    backtrack(0, [], 0, componentes)
    return mejor_solucion, min_costo