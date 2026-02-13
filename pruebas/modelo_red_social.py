class RedSocial:
    """Clase para modelar la red de amistades mediante un grafo."""
    def __init__(self):
        # Diccionario de adyacencia: {usuario: [(amigo, interacciones), ...]}
        self.usuarios = {}

    def agregar_usuario(self, usuario):
        if usuario not in self.usuarios:
            self.usuarios[usuario] = []

    def agregar_amistad(self, u1, u2, interacciones):
        """Agrega una relación ponderada (las distancias deben ser positivas)."""
        self.agregar_usuario(u1)
        self.agregar_usuario(u2)
        # Se asume grafo no dirigido: la amistad es recíproca
        self.usuarios[u1].append((u2, interacciones))
        self.usuarios[u2].append((u1, interacciones))