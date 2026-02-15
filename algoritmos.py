# --- 1. Red de Amistad Mínima (Kruskal - Greedy) ---
def obtener_red_minima(red):
    # Ordenar candidatos por peso (Criterio Greedy) 
    aristas_ordenadas = sorted(red.aristas, key=lambda x: x['peso'])
    padre = {u: u for u in red.usuarios}

    def encontrar(i):
        if padre[i] == i: return i
        return encontrar(padre[i])

    red_minima = []
    costo_total = 0
    for a in aristas_ordenadas:
        raiz_u, raiz_v = encontrar(a['u']), encontrar(a['v'])
        if raiz_u != raiz_v: # Función de factibilidad: evita bucles 
            padre[raiz_u] = raiz_v
            red_minima.append(a)
            costo_total += a['peso']
    return red_minima, costo_total

# --- 2. Recomendación de Amigos (Dijkstra - Greedy) ---
def recomendar_amigos(red, usuario_origen):

    # Visitados: nodos con costo definitivo
    visitados = set()

    # Pendientes: candidatos a procesar
    pendientes = set(red.usuarios)
    
    # Grafo de distancias (A): guardará el costo mínimo desde el origen 
    # Inicializamos todos con infinito, excepto el origen que es 0 
    distancias = {usuario: float('inf') for usuario in red.usuarios}
    distancias[usuario_origen] = 0

    # Función SOLUCIÓN: una vez que sale del while ya habrá trabajado con todos los nodos candidatos
    # Mientras haya nodos candidatos sin procesar
    while pendientes:
        # Función SELECCIÓN: elegir el nodo pendiente con menor costo acumulado 
        usuario_actual = min(pendientes, key=lambda u: distancias[u])
        
        # Si la distancia es infinita, los nodos restantes son inalcanzables
        if distancias[usuario_actual] == float('inf'):
            break

        # Marcar como visitado y sacar de pendientes 
        visitados.add(usuario_actual)
        pendientes.remove(usuario_actual)

        # Función FACTIBILIDAD: intentar mejorar las rutas de los vecinos 
        for vecino, peso_interaccion in red.adyacencia[usuario_actual]:
            if vecino in pendientes:
                nuevo_costo = distancias[usuario_actual] + peso_interaccion
                
                # Si el nuevo camino es más corto, se actualiza la distancia
                if nuevo_costo < distancias[vecino]:
                    distancias[vecino] = nuevo_costo

    # Función OBJETIVO: grafo con el valor de todos los caminos mínimos desde el nodo origen dado.
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