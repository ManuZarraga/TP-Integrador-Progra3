import heapq

def calcular_distancias_minimas(red, usuario_origen):
    """
    Implementación del Algoritmo de Dijkstra.
    Busca el costo del camino más corto entre el origen y todos los demás [1].
    """
    # Candidatos: Conjunto de vértices sacando el origen [3]
    pendientes = []
    # Función Objetivo: Mapa con el valor de todos los caminos mínimos [3]
    distancias = {usuario: float('inf') for usuario in red.usuarios}
    distancias[usuario_origen] = 0
    
    # Usamos una cola de prioridad para la Función de Selección [3]
    heapq.heappush(pendientes, (0, usuario_origen))
    visitados = set()

    while pendientes:
        # Selección: elegir el de menor costo desde el origen [3]
        costo_actual, u_actual = heapq.heappop(pendientes)

        if u_actual in visitados:
            continue
        
        visitados.add(u_actual)

        # Función de factibilidad: actualizar si el camino por aquí es mejor [3, 4]
        for amigo, peso in red.usuarios.get(u_actual, []):
            nueva_distancia = costo_actual + peso
            if nueva_distancia < distancias[amigo]:
                distancias[amigo] = nueva_distancia
                heapq.heappush(pendientes, (nueva_distancia, amigo))

    return distancias