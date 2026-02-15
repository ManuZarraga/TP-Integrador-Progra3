import heapq

# ==========================================
# 1. RED DE AMISTAD MÍNIMA (Kruskal - Greedy)
# ==========================================
def obtener_red_minima(red):
    """
    Encuentra el Árbol de Expansión Mínima (MST) usando el algoritmo de Kruskal.
    
    Estrategia Greedy:
    - Criterio de selección: Elegir la arista de menor peso
    - Función de factibilidad: No crear ciclos (usando Union-Find)
    
    Complejidad: O(E log E) donde E es el número de aristas
    
    Args:
        red: Objeto RedSocial
        
    Returns:
        tuple: (lista de aristas del MST, costo total)
    """
    if len(red.usuarios) == 0:
        return [], 0
    
    # Ordenar candidatos por peso (Criterio Greedy)
    aristas_ordenadas = sorted(red.aristas, key=lambda x: x['peso'])
    
    # Inicializar Union-Find
    padre = {u: u for u in red.usuarios}
    rango = {u: 0 for u in red.usuarios}  # Optimización: Union by rank

    def encontrar(i):
        if padre[i] == i: 
            return i
        # Path compression
        padre[i] = encontrar(padre[i])
        return padre[i]
    
    def unir(i, j):
        raiz_i = encontrar(i)
        raiz_j = encontrar(j)
        
        if raiz_i == raiz_j:
            return False
        
        # Union by rank
        if rango[raiz_i] < rango[raiz_j]:
            padre[raiz_i] = raiz_j
        elif rango[raiz_i] > rango[raiz_j]:
            padre[raiz_j] = raiz_i
        else:
            padre[raiz_j] = raiz_i
            rango[raiz_i] += 1
        return True

    red_minima = []
    costo_total = 0
    aristas_necesarias = len(red.usuarios) - 1  # Un árbol tiene n-1 aristas
    
    for a in aristas_ordenadas:
        # Función de factibilidad: evita ciclos
        if unir(a['u'], a['v']):
            red_minima.append(a)
            costo_total += a['peso']
            
            # Optimización: parar cuando tenemos el MST completo
            if len(red_minima) == aristas_necesarias:
                break
    
    return red_minima, costo_total


# ==========================================
# 2. RECOMENDACIÓN DE AMIGOS (Dijkstra - Greedy)
# ==========================================
def recomendar_amigos(red, origen):
    """
    Encuentra los caminos más cortos desde un usuario a todos los demás usando Dijkstra.
    
    Estrategia Greedy:
    - Función de selección: Nodo con menor distancia acumulada
    - Función de factibilidad: Relajación de aristas (si hay mejor camino, actualizar)
    
    Complejidad: O((V + E) log V) con heap binario
    
    Args:
        red: Objeto RedSocial
        origen: Usuario desde el cual calcular distancias
        
    Returns:
        dict: {usuario: distancia_mínima} desde el origen
    """
    if origen not in red.usuarios:
        return {}
    
    # Inicializar distancias
    distancias = {u: float('inf') for u in red.usuarios}
    distancias[origen] = 0
    
    # Cola de prioridad: (distancia, usuario)
    cola = [(0, origen)]
    visitados = set()
    
    while cola:
        d_actual, u_actual = heapq.heappop(cola)
        
        # Skip si ya procesamos este nodo con mejor distancia
        if u_actual in visitados:
            continue
        
        visitados.add(u_actual)
        
        # Si la distancia en la cola es mayor a la registrada, skip
        if d_actual > distancias[u_actual]:
            continue

        # Explorar vecinos
        for vecino, peso in red.adyacencia[u_actual]:
            dist = d_actual + peso
            
            # Función de factibilidad: relajación
            if dist < distancias[vecino]:
                distancias[vecino] = dist
                heapq.heappush(cola, (dist, vecino))
    
    return distancias


def obtener_amigos_sugeridos(red, usuario, max_sugerencias=5):
    """
    Obtiene sugerencias de amigos ordenadas por cercanía en la red.
    
    Args:
        red: Objeto RedSocial
        usuario: Usuario para quien generar sugerencias
        max_sugerencias: Máximo número de sugerencias a retornar
        
    Returns:
        list: Lista de tuplas (usuario, distancia) ordenadas por distancia
    """
    distancias = recomendar_amigos(red, usuario)
    
    # Filtrar amigos directos y usuarios inalcanzables
    amigos_directos = {vec for vec, _ in red.adyacencia[usuario]}
    sugerencias = [
        (u, d) for u, d in distancias.items() 
        if u != usuario and u not in amigos_directos and d != float('inf')
    ]
    
    # Ordenar por distancia y retornar top N
    sugerencias.sort(key=lambda x: x[1])
    return sugerencias[:max_sugerencias]


# ==========================================
# 3. RESTAURACIÓN POR BLOQUEO (Backtracking)
# ==========================================
def restaurar_red(red, candidatos_con_peso=None):
    """
    Encuentra el conjunto mínimo de conexiones para restaurar conectividad total.
    
    Estrategia: Búsqueda exhaustiva con backtracking
    - Prueba todas las combinaciones posibles de candidatos
    - Busca la solución de menor costo que reconecte todos los componentes
    
    Complejidad: O(2^C) donde C es el número de candidatos
    ADVERTENCIA: Costoso para muchos candidatos (>20)
    
    Args:
        red: Objeto RedSocial
        candidatos_con_peso: Lista de tuplas (u, v, peso). Si es None, se generan automáticamente.
        
    Returns:
        tuple: (lista de conexiones [(u, v)], costo total)
    """
    componentes = red.obtener_componentes()
    
    # Si ya está conexa, no hay nada que hacer
    if len(componentes) == 1:
        return [], 0
    
    # Generar candidatos si no se proporcionan
    if candidatos_con_peso is None:
        candidatos_con_peso = []
        posibles = red.obtener_conexiones_posibles()
        
        # Asignar pesos basados en un heurístico simple
        # (en la práctica, estos pesos podrían venir de datos reales)
        for u, v in posibles:
            # Peso heurístico: promedio de conexiones existentes
            peso = 5  # Peso por defecto
            candidatos_con_peso.append((u, v, peso))
    
    # Filtrar candidatos inválidos (usuarios que no existen)
    candidatos_validos = [
        (u, v, p) for u, v, p in candidatos_con_peso 
        if u in red.usuarios and v in red.usuarios
    ]
    
    if not candidatos_validos:
        return None, float('inf')
    
    # Ordenar candidatos por peso (heurística para mejorar poda)
    candidatos_validos.sort(key=lambda x: x[2])
    
    mejor_sol = None
    min_costo = float('inf')
    
    # Límite de seguridad para evitar explosión combinatoria
    MAX_CANDIDATOS = 25
    if len(candidatos_validos) > MAX_CANDIDATOS:
        print(f"⚠️  ADVERTENCIA: {len(candidatos_validos)} candidatos es demasiado. "
              f"Limitando a los {MAX_CANDIDATOS} más baratos.")
        candidatos_validos = candidatos_validos[:MAX_CANDIDATOS]

    def backtrack(idx, comps_actuales, conexiones, costo):
        nonlocal mejor_sol, min_costo
        
        # Caso base: todos conectados
        if len(comps_actuales) == 1:
            if costo < min_costo:
                min_costo = costo
                mejor_sol = list(conexiones)
            return
        
        # Poda: si el costo actual ya supera el mejor, no seguir
        if costo >= min_costo:
            return
        
        # Poda: si no quedan suficientes candidatos para conectar
        componentes_faltantes = len(comps_actuales) - 1
        candidatos_restantes = len(candidatos_validos) - idx
        if candidatos_restantes < componentes_faltantes:
            return
        
        # Probar cada candidato
        for i in range(idx, len(candidatos_validos)):
            u, v, p = candidatos_validos[i]
            
            # Encontrar componentes de cada usuario
            comp_u = next((c for c in comps_actuales if u in c), None)
            comp_v = next((c for c in comps_actuales if v in c), None)
            
            # Si conecta dos componentes diferentes
            if comp_u is not None and comp_v is not None and comp_u != comp_v:
                # Unificar componentes
                nuevos_comps = [c for c in comps_actuales if c != comp_u and c != comp_v]
                nuevos_comps.append(comp_u + comp_v)
                
                # Recursión
                conexiones.append((u, v))
                backtrack(i + 1, nuevos_comps, conexiones, costo + p)
                
                # Retroceso (Backtrack)
                conexiones.pop()
    
    backtrack(0, componentes, [], 0)
    
    return mejor_sol, min_costo
