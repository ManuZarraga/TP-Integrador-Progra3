class RedSocialBloqueos:
    def __init__(self, usuarios):
        self.usuarios = usuarios
        self.amistades = []

    def agregar_amistad(self, u, v, costo=1):
        self.amistades.append({'u': u, 'v': v, 'peso': costo})

    def eliminar_amistad(self, u, v):
        """Simula el bloqueo eliminando la conexión entre dos usuarios."""
        self.amistades = [a for a in self.amistades if not (
            (a['u'] == u and a['v'] == v) or (a['u'] == v and a['v'] == u)
        )]

    def obtener_componentes(self):
        """Identifica grupos conectados usando la lógica de 'Nro. Componente' [1]."""
        padre = {u: u for u in self.usuarios}

        def encontrar(i):
            if padre[i] == i: return i
            return encontrar(padre[i])

        def unir(i, j):
            raiz_i = encontrar(i)
            raiz_j = encontrar(j)
            if raiz_i != raiz_j:
                padre[raiz_i] = raiz_j
                return True
            return False

        for a in self.amistades:
            unir(a['u'], a['v'])

        componentes = {}
        for u in self.usuarios:
            raiz = encontrar(u)
            if raiz not in componentes: componentes[raiz] = []
            componentes[raiz].append(u)
        return list(componentes.values())