from red_social import RedSocial
import algoritmos

def mostrar_menu():
    print("\n--- SISTEMA DE RED SOCIAL UNIVERSITARIA ---")
    print("1. Agregar relación de amistad")
    print("2. Ver Red de Amistad Mínima (Infraestructura)")
    print("3. Sugerir Amigos (Vínculo más Corto)")
    print("4. Simular Bloqueo y Sugerir Conexiones Alternativas")
    print("5. Salir")
    return input("Elija una opción: ")

def ejecutar():
    red = RedSocial()
    # Datos iniciales opcionales
    red.agregar_conexion("Ana", "Bob", 2)
    red.agregar_conexion("Bob", "Carlos", 1)

    while True:
        opc = mostrar_menu()
        
        if opc == "1":
            u1 = input("Usuario 1: ")
            u2 = input("Usuario 2: ")
            p = int(input("Peso/Interacciones: "))
            red.agregar_conexion(u1, u2, p)
            print("Conexión agregada.")

        elif opc == "2":
            mst, costo = algoritmos.obtener_red_minima(red)
            print(f"\nRed Mínima necesaria (Costo: {costo}):")
            for a in mst: 
                # CAMBIO: Usar 'peso' en lugar de 'p'
                print(f"{a['u']} -- {a['v']} (Costo: {a['peso']})")

        elif opc == "3":
            usr = input("Usuario para recomendaciones: ")
            if usr in red.usuarios:
                dists = algoritmos.recomendar_amigos(red, usr)
                print(f"Distancias desde {usr}: {dists}")
            else: print("Usuario no encontrado.")

        elif opc == "4":
            u1 = input("Usuario bloqueador: ") # Ejemplo: Bob
            u2 = input("Usuario bloqueado: ")  # Ejemplo: Ana
            
            # 1. Eliminar la amistad (Simulación de ruptura de conexión) [1]
            red.aristas = [a for a in red.aristas if not (
                (a['u'] == u1 and a['v'] == u2) or (a['u'] == u2 and a['v'] == u1))]
            
            # 2. También actualizamos la lista de adyacencia
            red.adyacencia[u1] = [vec for vec in red.adyacencia[u1] if vec != u2]
            red.adyacencia[u2] = [vec for vec in red.adyacencia[u2] if vec != u1]

            print(f"\nBloqueo entre {u1} y {u2} realizado.")
            
            # 3. Definir candidatos de reconexión dinámicamente
            # Aquí usamos solo usuarios que sabemos que existen en tu ejecución
            posibles = [("Ana", "Carlos", 10)] 
            
            print("Evaluando si la red sigue conexa...")
            nuevas, costo = algoritmos.restaurar_red(red, posibles)
            
            if nuevas:
                print(f"La red se fragmentó. Para restaurarla se sugiere: {nuevas}")
                print(f"Costo total de reconexión: {costo}")
            else:
                print("La red sigue siendo conexa o no hay candidatos para unir los grupos.")

        elif opc == "5": break

if __name__ == "__main__":
    ejecutar()