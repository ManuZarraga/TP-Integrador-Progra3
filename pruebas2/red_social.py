class RedSocial:
    def __init__(self):
        self.usuarios = set()
        self.adyacencia = {}  # Para Dijkstra: {usuario: [(vecino, peso), ...]}
        self.aristas = []     # Para Kruskal: [{'u': usuario, 'v': vecino, 'peso': int}, ...]

    def agregar_usuario(self, u):
        """Agrega un usuario a la red si no existe."""
        if u not in self.usuarios:
            self.usuarios.add(u)
            self.adyacencia[u] = []

    def agregar_conexion(self, u, v, peso):
        """
        Agrega una conexión bidireccional entre dos usuarios.
        
        Args:
            u: Usuario 1
            v: Usuario 2
            peso: Peso de la conexión (número de interacciones, distancia, etc.)
        """
        if peso < 0:
            raise ValueError("El peso no puede ser negativo")
        
        self.agregar_usuario(u)
        self.agregar_usuario(v)
        
        # Evitar conexiones duplicadas
        if not any(vecino == v for vecino, _ in self.adyacencia[u]):
            # Grafo no dirigido
            self.adyacencia[u].append((v, peso))
            self.adyacencia[v].append((u, peso))
            self.aristas.append({'u': u, 'v': v, 'peso': peso})

    def eliminar_conexion(self, u1, u2):
        """
        Elimina la conexión entre dos usuarios (simula un bloqueo).
        
        Returns:
            bool: True si se eliminó, False si no existía la conexión
        """
        # Eliminar de aristas
        aristas_antes = len(self.aristas)
        self.aristas = [a for a in self.aristas if not (
            (a['u'] == u1 and a['v'] == u2) or (a['u'] == u2 and a['v'] == u1))]
        
        # Eliminar de adyacencia (CORREGIDO: comparar con vec[0])
        if u1 in self.adyacencia:
            self.adyacencia[u1] = [(vec, peso) for vec, peso in self.adyacencia[u1] if vec != u2]
        if u2 in self.adyacencia:
            self.adyacencia[u2] = [(vec, peso) for vec, peso in self.adyacencia[u2] if vec != u1]
        
        return len(self.aristas) < aristas_antes

    def obtener_componentes(self):
        """
        Usa Union-Find para identificar grupos conexos.
        
        Returns:
            list: Lista de componentes, donde cada componente es una lista de usuarios
        """
        padre = {u: u for u in self.usuarios}
        
        def encontrar(i):
            if padre[i] == i: 
                return i
            # Path compression para optimizar
            padre[i] = encontrar(padre[i])
            return padre[i]

        def unir(i, j):
            raiz_i, raiz_j = encontrar(i), encontrar(j)
            if raiz_i != raiz_j: 
                padre[raiz_i] = raiz_j

        # Unir todos los usuarios conectados
        for a in self.aristas:
            unir(a['u'], a['v'])

        # Agrupar por componente
        comps = {}
        for u in self.usuarios:
            r = encontrar(u)
            if r not in comps: 
                comps[r] = []
            comps[r].append(u)
        
        return list(comps.values())

    def obtener_conexiones_posibles(self):
        """
        Genera todas las conexiones posibles que NO existen actualmente.
        Útil para el algoritmo de restauración.
        
        Returns:
            list: Lista de tuplas (u, v) de conexiones posibles
        """
        existentes = set()
        for a in self.aristas:
            existentes.add((min(a['u'], a['v']), max(a['u'], a['v'])))
        
        posibles = []
        usuarios_lista = sorted(self.usuarios)
        for i, u in enumerate(usuarios_lista):
            for v in usuarios_lista[i+1:]:
                if (u, v) not in existentes:
                    posibles.append((u, v))
        
        return posibles

    def __str__(self):
        """Representación en string de la red."""
        resultado = f"Red Social con {len(self.usuarios)} usuarios y {len(self.aristas)} conexiones\n"
        resultado += f"Usuarios: {sorted(self.usuarios)}\n"
        resultado += "Conexiones:\n"
        for a in sorted(self.aristas, key=lambda x: x['peso']):
            resultado += f"  {a['u']} -- {a['v']} (peso: {a['peso']})\n"
        return resultado