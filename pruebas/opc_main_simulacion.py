from opc_red_grafos import RedSocialBloqueos
from opc_algoritmos_busqueda import restaurar_conectividad

if __name__ == "__main__":
    usuarios = ["A", "B", "C", "D", "E"]
    red = RedSocialBloqueos(usuarios)
    
    # Red conexa inicial
    red.agregar_amistad("A", "B")
    red.agregar_amistad("B", "C")
    red.agregar_amistad("C", "D")
    red.agregar_amistad("D", "E")

    print("--- Simulación de Bloqueo ---")
    print("El usuario B bloquea al usuario C.")
    red.eliminar_amistad("B", "C")

    componentes = red.obtener_componentes()
    if len(componentes) > 1:
        print(f"Red fragmentada en {len(componentes)} grupos.")
        
        # Posibles conexiones alternativas (usuarios que podrían hacerse amigos)
        candidatos = [
            ("A", "E", 10), ("B", "D", 5), ("A", "D", 8)
        ]
        
        print("Buscando conjunto mínimo de nuevas conexiones...")
        nuevas, costo = restaurar_conectividad(componentes, candidatos)
        
        print(f"Propuesta de restauración: {nuevas}")
        print(f"Costo total de reconexión: {costo}")
    else:
        print("La red sigue siendo conexa.")