from modelo_red_social import RedSocial
from algoritmo_recomendacion import calcular_distancias_minimas

def recomendar_amigos(usuario_id, distancias, limite=3):
    """Sugiere amigos basados en la menor distancia (excluyendo al usuario mismo)."""
    # Ordenar por distancia (el vínculo más corto)
    sugerencias = sorted(distancias.items(), key=lambda x: x[1])
    return [u for u, d in sugerencias if u != usuario_id and d > 0][:limite]

if __name__ == "__main__":
    red_uade = RedSocial()
    # Datos de ejemplo: (Usuario1, Usuario2, Costo/Interacciones)
    red_uade.agregar_amistad("Ana", "Bob", 2)
    red_uade.agregar_amistad("Ana", "Carlos", 5)
    red_uade.agregar_amistad("Bob", "Carlos", 1)
    red_uade.agregar_amistad("Bob", "Diana", 10)
    red_uade.agregar_amistad("Carlos", "Diana", 3)
    red_uade.agregar_amistad("Diana", "Esteban", 1)

    usuario_objetivo = "Ana"
    print(f"--- Recomendaciones para {usuario_objetivo} ---")
    
    # 1. Ejecutar Dijkstra
    todas_distancias = calcular_distancias_minimas(red_uade, usuario_objetivo)
    
    # 2. Obtener los vínculos más cortos
    recomendados = recomendar_amigos(usuario_objetivo, todas_distancias)
    
    for i, user in enumerate(recomendados, 1):
        dist = todas_distancias[user]
        print(f"{i}. {user} (Distancia total: {dist})")