from red_social import RedSocial
import algoritmos

def mostrar_menu():
    print("\n" + "="*60)
    print("   SISTEMA DE RED SOCIAL UNIVERSITARIA")
    print("="*60)
    print("1. Agregar relación de amistad")
    print("2. Ver Red de Amistad Mínima (Infraestructura)")
    print("3. Sugerir Amigos (Vínculo más Corto)")
    print("4. Simular Bloqueo y Sugerir Conexiones Alternativas")
    print("5. Ver estado actual de la red")
    print("6. Salir")
    print("="*60)
    return input("Elija una opción: ")

def ejecutar():
    red = RedSocial()
    # Datos iniciales
    print("Inicializando red social con múltiples conexiones...\n")
    
    red.agregar_conexion("Ana", "Bruno", 5)
    red.agregar_conexion("Ana", "Carlos", 3)
    red.agregar_conexion("Bruno", "Carlos", 2)
    red.agregar_conexion("Bruno", "Diana", 4)
    red.agregar_conexion("Carlos", "Elena", 6)
    red.agregar_conexion("Diana", "Elena", 3)
    red.agregar_conexion("Felipe", "Gloria", 4)
    red.agregar_conexion("Felipe", "Hugo", 2)
    red.agregar_conexion("Gloria", "Hugo", 5)
    red.agregar_conexion("Gloria", "Irene", 3)
    red.agregar_conexion("Hugo", "Julián", 4)
    red.agregar_conexion("Karen", "Luis", 6)
    red.agregar_conexion("Luis", "María", 2)
    red.agregar_conexion("Karen", "María", 4)
    red.agregar_conexion("Elena", "Felipe", 8)
    red.agregar_conexion("Irene", "Karen", 7)
    red.agregar_conexion("Carlos", "Hugo", 9)
    red.agregar_conexion("Natalia", "Ana", 10)
    red.agregar_conexion("Omar", "Felipe", 8)
    red.agregar_conexion("Pedro", "Quintín", 1)
    red.agregar_conexion("Quintín", "Rosa", 2)
    red.agregar_conexion("Pedro", "Bruno", 7)
    
    print(f"✅ Red cargada con {len(red.usuarios)} usuarios y {len(red.aristas)} conexiones\n")

    while True:
        opc = mostrar_menu()
        
        if opc == "1":
            u1 = input("Usuario 1: ")
            u2 = input("Usuario 2: ")
            try:
                p = int(input("Peso/Interacciones: "))
                red.agregar_conexion(u1, u2, p)
                print("✅ Conexión agregada.")
            except ValueError:
                print("❌ El peso debe ser un número entero.")

        elif opc == "2":
            if len(red.usuarios) == 0:
                print("❌ La red está vacía.")
                continue
            mst, costo = algoritmos.obtener_red_minima(red)
            print(f"\n🌳 Red Mínima necesaria (Costo total: {costo}):")
            for a in mst: 
                print(f"  • {a['u']:12} -- {a['v']:12} (Costo: {a['peso']})")

        elif opc == "3":
            usr = input("Usuario para recomendaciones: ")
            if usr in red.usuarios:
                dists = algoritmos.recomendar_amigos(red, usr)
                print(f"\n🤝 Distancias desde {usr}:")
                for usuario, dist in sorted(dists.items()):
                    if dist != float('inf'):
                        print(f"  • {usuario:12} - Distancia: {dist}")
            else: 
                print("❌ Usuario no encontrado.")

        elif opc == "4":
            if len(red.aristas) == 0:
                print("❌ No hay conexiones en la red.")
                continue
                
            u1 = input("Usuario que bloquea: ")
            u2 = input("Usuario bloqueado: ")
            
            if u1 not in red.usuarios or u2 not in red.usuarios:
                print("❌ Uno o ambos usuarios no existen.")
                continue
            
            # Verificar si existe la conexión
            conexion_existe = any(
                (a['u'] == u1 and a['v'] == u2) or (a['u'] == u2 and a['v'] == u1)
                for a in red.aristas
            )
            
            if not conexion_existe:
                print(f"❌ No existe conexión directa entre {u1} y {u2}")
                continue
            
            # Eliminar la conexión
            red.aristas = [a for a in red.aristas if not (
                (a['u'] == u1 and a['v'] == u2) or (a['u'] == u2 and a['v'] == u1))]
            
            red.adyacencia[u1] = [(vec, peso) for vec, peso in red.adyacencia[u1] if vec != u2]
            red.adyacencia[u2] = [(vec, peso) for vec, peso in red.adyacencia[u2] if vec != u1]

            print(f"\n🚫 Bloqueo realizado: {u1} ⛔ {u2}")
            
            # Generar candidatos de reconexión automáticamente
            posibles = []
            usuarios_lista = sorted(red.usuarios)
            existentes = set()
            for a in red.aristas:
                existentes.add((min(a['u'], a['v']), max(a['u'], a['v'])))
            
            for i, usuario1 in enumerate(usuarios_lista):
                for usuario2 in usuarios_lista[i+1:]:
                    if (usuario1, usuario2) not in existentes:
                        posibles.append((usuario1, usuario2, 5))  # Peso por defecto
            
            print(f"Evaluando conectividad...")
            nuevas, costo = algoritmos.restaurar_red(red, posibles if posibles else [])
            
            componentes = red.obtener_componentes()
            print(f"📊 Componentes conexos: {len(componentes)}")
            
            if len(componentes) == 1:
                print("✅ La red sigue siendo conexa.")
            elif nuevas:
                print(f"\n⚠️  La red se fragmentó en {len(componentes)} grupos.")
                print(f"Para restaurarla se sugiere:")
                for u, v in nuevas:
                    print(f"  • Conectar {u} -- {v}")
                print(f"Costo total de reconexión: {costo}")
            else:
                print("❌ No se encontró solución para restaurar la red.")

        elif opc == "5":
            print("\n" + "="*60)
            print("ESTADO ACTUAL DE LA RED")
            print("="*60)
            print(f"👥 Total de usuarios: {len(red.usuarios)}")
            print(f"🔗 Total de conexiones: {len(red.aristas)}")
            componentes = red.obtener_componentes()
            print(f"🌐 Componentes conexos: {len(componentes)}")
            
            if len(componentes) == 1:
                print("✅ La red está completamente conectada")
            else:
                print("⚠️  La red está fragmentada en los siguientes grupos:")
                for i, comp in enumerate(componentes, 1):
                    print(f"   Grupo {i}: {sorted(comp)}")
            
            print(f"\n📋 Usuarios: {sorted(red.usuarios)}")

        elif opc == "6": 
            print("\n👋 ¡Gracias por usar el sistema! Hasta pronto.")
            break
        
        else:
            print("❌ Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    ejecutar()