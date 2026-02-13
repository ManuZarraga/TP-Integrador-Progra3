import heapq

# --- 1. Red de Amistad Mínima (Kruskal - Greedy) ---
def obtener_red_minima(red):
    # Ordenar candidatos por peso (Criterio Greedy) [3]
    aristas_ordenadas = sorted(red.aristas, key=lambda x: x['peso'])
    padre = {u: u for u in red.usuarios}

    def encontrar(i):
        if padre[i] == i: return i
        return encontrar(padre[i])

    red_minima = []
    costo_total = 0
    for a in aristas_ordenadas:
        raiz_u, raiz_v = encontrar(a['u']), encontrar(a['v'])
        if raiz_u != raiz_v: # Función de factibilidad: evita bucles [5]
            padre[raiz_u] = raiz_v
            red_minima.append(a)
            costo_total += a['peso']
    return red_minima, costo_total

# --- 2. Recomendación de Amigos (Dijkstra - Greedy) ---
def recomendar_amigos(red, origen):
    distancias = {u: float('inf') for u in red.usuarios}
    distancias[origen] = 0
    cola = [(0, origen)] # Función de selección: el de menor costo acumulado [1, 6]

    while cola:
        d_actual, u_actual = heapq.heappop(cola)
        if d_actual > distancias[u_actual]: continue

        for vecino, peso in red.adyacencia[u_actual]:
            dist = d_actual + peso
            if dist < distancias[vecino]: # Función de factibilidad [6]
                distancias[vecino] = dist
                heapq.heappush(cola, (dist, vecino))
    return distancias

# --- 3. Restauración por Bloqueo (Backtracking - Búsqueda Exhaustiva) ---
def restaurar_red(red, candidatos):
    componentes = red.obtener_componentes()
    if len(componentes) == 1: return [], 0
    
    mejor_sol = None
    min_costo = float('inf')

    def backtrack(idx, comps_actuales, conexiones, costo):
        nonlocal mejor_sol, min_costo
        if len(comps_actuales) == 1:
            if costo < min_costo:
                min_costo = costo
                mejor_sol = list(conexiones)
            return

        for i in range(idx, len(candidatos)):
            u, v, p = candidatos[i]
            
            # Buscamos a qué componente pertenece cada usuario del candidato
            # Si el usuario no existe en la red, comp_u o comp_v serán None
            comp_u = next((c for c in comps_actuales if u in c), None)
            comp_v = next((c for c in comps_actuales if v in c), None)

            # VALIDACIÓN: Si alguno de los usuarios no existe en la red social, 
            # simplemente ignoramos este candidato y seguimos con el siguiente.
            if comp_u is None or comp_v is None:
                continue

            if comp_u != comp_v:
                # Paso: Unificar componentes (Función de Selección Greedy aplicada a Backtracking)
                nuevos_comps = [c for c in comps_actuales if c != comp_u and c != comp_v]
                nuevos_comps.append(comp_u + comp_v)
                
                conexiones.append((u, v))
                backtrack(i + 1, nuevos_comps, conexiones, costo + p)
                
                # Retroceso (Backtrack)
                conexiones.pop()

    backtrack(0, componentes, [], 0)
    return mejor_sol, min_costo