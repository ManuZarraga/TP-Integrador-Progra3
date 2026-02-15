class RedSocial:
    def __init__(self):
        self.usuarios = set()
        self.adyacencia = {}  # Dijkstra
        self.aristas = []     # Kruskal

    def agregar_usuario(self, u):
        if u not in self.usuarios:
            self.usuarios.add(u)
            self.adyacencia[u] = []

    def agregar_conexion(self, u, v, peso):
        self.agregar_usuario(u)
        self.agregar_usuario(v)
        # Grafo no dirigido
        self.adyacencia[u].append((v, peso))
        self.adyacencia[v].append((u, peso))
        self.aristas.append({'u': u, 'v': v, 'peso': peso})

    def obtener_componentes(self):
        """Usa la lógica de Union-Find para identificar grupos conexos."""
        padre = {u: u for u in self.usuarios}
        
        def encontrar(i):
            if padre[i] == i: return i
            return encontrar(padre[i])

        def unir(i, j):
            raiz_i, raiz_j = encontrar(i), encontrar(j)
            if raiz_i != raiz_j: padre[raiz_i] = raiz_j

        for a in self.aristas:
            unir(a['u'], a['v'])

        comps = {}
        for u in self.usuarios:
            r = encontrar(u)
            if r not in comps: comps[r] = []
            comps[r].append(u)
        return list(comps.values())