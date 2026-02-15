# --- 1. Red de Amistad Mínima (Kruskal - Greedy) ---
def obtener_red_minima(red):
    # Ordenar todas las aristas por peso ascendente (criterio greedy)
    aristas_ordenadas = sorted(red.aristas, key=lambda x: x['peso'])
    
    # cada usuario comienza siendo su propio representante
    padre = {u: u for u in red.usuarios}

    # Función encontrar: obtiene el representante (raíz) del conjunto
    def encontrar(i):
        # Caso base: si es su propio padre, es la raíz
        if padre[i] == i: 
            return i
        # Búsqueda recursiva del representante
        return encontrar(padre[i])

    red_minima = []      # Lista que almacenará las aristas del árbol generador mínimo
    costo_total = 0      # Acumulador del costo total de la red mínima

    # Se recorren las aristas ordenadas
    for a in aristas_ordenadas:
        # Se obtiene la raíz de cada extremo de la arista
        raiz_u = encontrar(a['u'])
        raiz_v = encontrar(a['v'])

        # Función de factibilidad: solo unir si pertenecen a componentes distintas
        if raiz_u != raiz_v:
            # Unión de conjuntos: se conecta una raíz con la otra
            padre[raiz_u] = raiz_v
            
            # Se agrega la arista válida al resultado
            red_minima.append(a)
            
            # Se acumula su costo
            costo_total += a['peso']

    # Resultado: conjunto mínimo de conexiones y su costo total
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
    
    # Se obtienen las componentes conexas actuales de la red
    componentes = red.obtener_componentes()
    
    # Si ya está completamente conectada, no se necesitan nuevas conexiones
    if len(componentes) == 1: 
        return [], 0
    
    mejor_sol = None          # Mejor conjunto de conexiones encontrado
    min_costo = float('inf')  # Mejor costo acumulado encontrado

    # Función recursiva que explora combinaciones posibles
    def backtrack(idx, comps_actuales, conexiones, costo):
        nonlocal mejor_sol, min_costo

        # Condición de solución: la red queda completamente conexa
        if len(comps_actuales) == 1:
            # Si el costo es menor al mejor conocido, se actualiza
            if costo < min_costo:
                min_costo = costo
                mejor_sol = list(conexiones)
            return

        # Se recorren los candidatos restantes a partir del índice actual
        for i in range(idx, len(candidatos)):
            u, v, p = candidatos[i]
            
            # Determinar a qué componente pertenece cada usuario
            comp_u = next((c for c in comps_actuales if u in c), None)
            comp_v = next((c for c in comps_actuales if v in c), None)

            # Validación: si alguno no pertenece a la red, se descarta
            if comp_u is None or comp_v is None:
                continue

            # Solo se considera la conexión si une componentes distintas
            if comp_u != comp_v:
                
                # Se generan nuevas componentes unificando ambas
                nuevos_comps = [
                    c for c in comps_actuales 
                    if c != comp_u and c != comp_v
                ]
                nuevos_comps.append(comp_u + comp_v)
                
                # Se agrega la conexión a la solución parcial
                conexiones.append((u, v))
                
                # Llamada recursiva avanzando al siguiente candidato
                backtrack(i + 1, nuevos_comps, conexiones, costo + p)
                
                # Retroceso: se elimina la última conexión agregada
                conexiones.pop()

    # Se inicia la exploración desde el primer candidato
    backtrack(0, componentes, [], 0)

    # Retorna la mejor combinación encontrada y su costo
    return mejor_sol, min_costo
