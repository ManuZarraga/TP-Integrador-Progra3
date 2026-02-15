class RedSocial:
    def __init__(self):
        # Conjunto de usuarios (vértices del grafo)
        self.usuarios = set()
        
        # Lista de adyacencia: 
        # clave = usuario, valor = lista de tuplas (vecino, peso)
        # Utilizada principalmente por Dijkstra
        self.adyacencia = {}
        
        # Lista de aristas en formato explícito
        # Utilizada por Kruskal
        self.aristas = []

    def agregar_usuario(self, u):
        # Agrega un nuevo usuario si aún no existe en la red
        if u not in self.usuarios:
            self.usuarios.add(u)
            
            # Se inicializa su lista de vecinos vacía
            self.adyacencia[u] = []

    def agregar_conexion(self, u, v, peso):
        # Asegura que ambos usuarios existan en la red
        self.agregar_usuario(u)
        self.agregar_usuario(v)
        
        # Se agrega la conexión en ambos sentidos (grafo no dirigido)
        # Representa una relación de amistad bidireccional
        self.adyacencia[u].append((v, peso))
        self.adyacencia[v].append((u, peso))
        
        # Se almacena también como arista independiente
        # Esto facilita el procesamiento en Kruskal
        self.aristas.append({'u': u, 'v': v, 'peso': peso})

    def obtener_componentes(self):
        """
        Determina las componentes conexas del grafo actual.
        Utiliza la lógica de Union-Find para agrupar usuarios conectados.
        """
        
        # Inicialmente cada usuario es su propio representante
        padre = {u: u for u in self.usuarios}
        
        # Función FIND: obtiene la raíz del conjunto
        def encontrar(i):
            if padre[i] == i:
                return i
            return encontrar(padre[i])

        # Función UNION: une dos conjuntos si sus raíces son distintas
        def unir(i, j):
            raiz_i = encontrar(i)
            raiz_j = encontrar(j)
            if raiz_i != raiz_j:
                padre[raiz_i] = raiz_j

        # Se recorren todas las aristas para unificar conjuntos conectados
        for a in self.aristas:
            unir(a['u'], a['v'])

        # Se agrupan los usuarios según su representante final
        comps = {}
        for u in self.usuarios:
            r = encontrar(u)
            
            # Si la raíz aún no fue registrada, se crea una nueva componente
            if r not in comps:
                comps[r] = []
            
            comps[r].append(u)

        # Se devuelve la lista de componentes conexas
        return list(comps.values())
