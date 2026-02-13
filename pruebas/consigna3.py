class Arista:
    def __init__(self, u, v, peso):
        self.u = u  # Usuario origen
        self.v = v  # Usuario destino
        self.peso = peso # Costo de la conexión

# Estructura Union-Find para gestionar componentes y evitar bucles
class UnionFind:
    def __init__(self, nodos):
        # Inicialmente cada nodo es su propio padre (un subárbol independiente) [4]
        self.padre = {nodo: nodo for nodo in nodos}

    def encontrar(self, nodo):
        # Busca la raíz del componente al que pertenece el nodo
        if self.padre[nodo] == nodo:
            return nodo
        self.padre[nodo] = self.encontrar(self.padre[nodo])
        return self.padre[nodo]

    def unir(self, u, v):
        # Une dos subárboles diferentes [3]
        raiz_u = self.encontrar(u)
        raiz_v = self.encontrar(v)
        if raiz_u != raiz_v:
            self.padre[raiz_u] = raiz_v
            return True
        return False

def algoritmo_kruskal(usuarios, conexiones):
    """
    Entrada: 
        usuarios: Lista de IDs de usuarios
        conexiones: Lista de objetos Arista
    Salida:
        MST: Lista de aristas que forman la red mínima
    """
    # 1. Candidatos: Todas las conexiones del grafo [4]
    # 2. Selección: Ordenar conexiones por costo de menor a mayor [3, 4]
    conexiones_ordenadas = sorted(conexiones, key=lambda x: x.peso)
    
    uf = UnionFind(usuarios)
    red_minima = []
    costo_total = 0

    # 3. Iterar sobre las conexiones más baratas [3]
    for conexion in conexiones_ordenadas:
        # Función de factibilidad: ¿Están en diferentes subárboles? [4]
        if uf.encontrar(conexion.u) != uf.encontrar(conexion.v):
            # Si es factible, se agrega a la solución [4, 8]
            uf.unir(conexion.u, conexion.v)
            red_minima.append(conexion)
            costo_total += conexion.peso
            
            # Condición de salida: Si ya tenemos N-1 aristas, todos están conectados
            if len(red_minima) == len(usuarios) - 1:
                break

    return red_minima, costo_total

# Ejemplo de uso basado en el escenario del campus
if __name__ == "__main__":
    # Lista de usuarios en el campus
    campus_usuarios = ["U1", "U2", "U3", "U4", "U5", "U6"]
    
    # Lista de posibles conexiones con sus costos (infraestructura/dependencia)
    posibles_conexiones = [
        Arista("U5", "U4", 1),
        Arista("U6", "U4", 1),
        Arista("U2", "U1", 2),
        Arista("U2", "U5", 2),
        Arista("U1", "U6", 3),
        Arista("U2", "U3", 3),
        Arista("U3", "U6", 3),
        Arista("U5", "U6", 3)
    ]

    resultado_mst, costo_optimo = algoritmo_kruskal(campus_usuarios, posibles_conexiones)

    print("--- Red de Amistad de Mínima Conectividad ---")
    for arista in resultado_mst:
        print(f"Conexión: {arista.u} <-> {arista.v} | Costo: {arista.peso}")
    print(f"Costo total de infraestructura: {costo_optimo}")