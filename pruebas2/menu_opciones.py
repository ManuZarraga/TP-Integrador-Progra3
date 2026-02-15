"""
Módulo con las funciones para cada opción del menú.
Cada función corresponde a una opción seleccionada por el usuario.
"""

import algoritmos


def opcion_agregar_conexion(red):
    """Maneja la opción de agregar una nueva conexión."""
    print("\n--- AGREGAR NUEVA CONEXIÓN ---")
    u1 = input("Usuario 1: ").strip()
    u2 = input("Usuario 2: ").strip()
    
    if not u1 or not u2:
        print("❌ Los nombres no pueden estar vacíos")
        return
    
    if u1 == u2:
        print("❌ Un usuario no puede conectarse consigo mismo")
        return
    
    try:
        peso = int(input("Peso/Nivel de interacción (número positivo): ").strip())
        if peso < 0:
            print("❌ El peso debe ser positivo")
            return
        
        red.agregar_conexion(u1, u2, peso)
        print(f"✅ Conexión agregada: {u1} -- {u2} (peso: {peso})")
    except ValueError:
        print("❌ El peso debe ser un número entero")


def opcion_red_minima(red):
    """Calcula y muestra la red de amistad mínima."""
    print("\n" + "="*60)
    print("RED DE AMISTAD MÍNIMA (Algoritmo de Kruskal)")
    print("="*60)
    print("Objetivo: Conectar a todos los usuarios con el mínimo costo")
    print("Aplicación: Optimizar infraestructura de comunicación\n")
    
    if len(red.usuarios) == 0:
        print("❌ La red está vacía")
        return
    
    mst, costo = algoritmos.obtener_red_minima(red)
    
    if len(mst) == 0:
        print("⚠️  No hay conexiones en la red")
        return
    
    print(f"💰 Costo total mínimo: {costo}")
    print(f"🔗 Conexiones necesarias: {len(mst)}/{len(red.aristas)}\n")
    print("Conexiones en la red mínima:")
    for a in mst:
        print(f"  • {a['u']:12} -- {a['v']:12} (costo: {a['peso']})")
    
    # Calcular ahorro
    costo_total_original = sum(a['peso'] for a in red.aristas)
    ahorro = costo_total_original - costo
    porcentaje = (ahorro / costo_total_original * 100) if costo_total_original > 0 else 0
    print(f"\n💡 Ahorro: {ahorro} ({porcentaje:.1f}% del costo total)")


def opcion_recomendar_amigos(red):
    """Genera recomendaciones de amigos para un usuario."""
    print("\n" + "="*60)
    print("RECOMENDACIÓN DE AMIGOS (Algoritmo de Dijkstra)")
    print("="*60)
    
    usr = input("Ingrese el nombre del usuario: ").strip()
    
    if usr not in red.usuarios:
        print(f"❌ El usuario '{usr}' no existe en la red")
        print(f"Usuarios disponibles: {sorted(red.usuarios)}")
        return
    
    # Calcular distancias
    distancias = algoritmos.recomendar_amigos(red, usr)
    sugerencias = algoritmos.obtener_amigos_sugeridos(red, usr, max_sugerencias=10)
    
    # Mostrar amigos directos
    amigos_directos = [(vec, peso) for vec, peso in red.adyacencia[usr]]
    print(f"\n👥 Amigos directos de {usr}:")
    if amigos_directos:
        for amigo, peso in sorted(amigos_directos, key=lambda x: x[1]):
            print(f"  • {amigo:12} (interacciones: {peso})")
    else:
        print("  (ninguno)")
    
    # Mostrar sugerencias
    print(f"\n🤝 Amigos sugeridos para {usr} (ordenados por cercanía):")
    if sugerencias:
        for i, (amigo, dist) in enumerate(sugerencias, 1):
            nivel = "⭐⭐⭐" if dist <= 2 else "⭐⭐" if dist <= 4 else "⭐"
            print(f"  {i}. {amigo:12} - Distancia: {dist:3.0f} {nivel}")
    else:
        print("  (no hay sugerencias disponibles)")
    
    # Mostrar usuarios inalcanzables
    inalcanzables = [u for u, d in distancias.items() if d == float('inf') and u != usr]
    if inalcanzables:
        print(f"\n⚠️  Usuarios no alcanzables desde {usr}:")
        print(f"  {sorted(inalcanzables)}")


def opcion_simular_bloqueo(red):
    """Simula un bloqueo y sugiere conexiones para restaurar conectividad."""
    print("\n" + "="*60)
    print("SIMULACIÓN DE BLOQUEO Y RESTAURACIÓN")
    print("="*60)
    
    # Mostrar conexiones existentes
    if len(red.aristas) == 0:
        print("❌ No hay conexiones en la red")
        return
    
    print("Conexiones actuales:")
    for i, a in enumerate(red.aristas[:10], 1):
        print(f"  {i}. {a['u']} -- {a['v']} (peso: {a['peso']})")
    if len(red.aristas) > 10:
        print(f"  ... y {len(red.aristas) - 10} más")
    
    u1 = input("\nUsuario que bloquea: ").strip()
    u2 = input("Usuario bloqueado: ").strip()
    
    if u1 not in red.usuarios or u2 not in red.usuarios:
        print("❌ Uno o ambos usuarios no existen en la red")
        return
    
    # Verificar si existe la conexión
    conexion_existe = any(
        (a['u'] == u1 and a['v'] == u2) or (a['u'] == u2 and a['v'] == u1)
        for a in red.aristas
    )
    
    if not conexion_existe:
        print(f"⚠️  No existe una conexión directa entre {u1} y {u2}")
        return
    
    # Realizar el bloqueo
    red.eliminar_conexion(u1, u2)
    print(f"\n🚫 Bloqueo realizado: {u1} ⛔ {u2}")
    
    # Evaluar conectividad
    componentes = red.obtener_componentes()
    print(f"\n📊 Evaluando conectividad...")
    print(f"   Componentes conexos: {len(componentes)}")
    
    if len(componentes) == 1:
        print("✅ La red sigue siendo conexa. No se necesitan cambios.")
        return
    
    # La red se fragmentó
    print("⚠️  ¡La red se ha fragmentado!")
    print("\n🔍 Grupos aislados:")
    for i, comp in enumerate(componentes, 1):
        print(f"   Grupo {i}: {sorted(comp)}")
    
    print("\n🔄 Buscando conexiones para restaurar conectividad...")
    print("   (Esto puede tomar unos momentos...)")
    
    # Buscar solución
    nuevas, costo = algoritmos.restaurar_red(red)
    
    if nuevas and costo < float('inf'):
        print(f"\n✅ Solución encontrada!")
        print(f"💰 Costo total de reconexión: {costo}")
        print(f"🔗 Conexiones sugeridas ({len(nuevas)}):")
        for u, v in nuevas:
            print(f"   • {u} -- {v}")
        
        # Preguntar si quiere aplicar los cambios
        respuesta = input("\n¿Desea aplicar estas conexiones? (s/n): ").strip().lower()
        if respuesta == 's':
            for u, v in nuevas:
                red.agregar_conexion(u, v, 5)  # Peso por defecto
            print("✅ Conexiones aplicadas. La red está restaurada.")
    else:
        print("❌ No se encontró una solución viable con los candidatos disponibles.")


def opcion_analizar_complejidad(red):
    """Muestra un análisis de la complejidad y características de la red."""
    print("\n" + "="*60)
    print("ANÁLISIS DE COMPLEJIDAD")
    print("="*60)
    
    info = algoritmos.analizar_complejidad_red(red)
    
    print(f"👥 Usuarios: {info['usuarios']}")
    print(f"🔗 Conexiones: {info['conexiones']}")
    print(f"🌐 Componentes: {info['componentes']}")
    print(f"📊 Densidad: {info['densidad']}")
    print(f"✅ ¿Es conexa?: {'Sí' if info['es_conexo'] else 'No'}")
    
    print(f"\n⏱️  Complejidad de algoritmos:")
    print(f"   • Dijkstra (camino más corto): {info['complejidad_dijkstra']}")
    print(f"   • Kruskal (MST): {info['complejidad_kruskal']}")
    
    if info['usuarios'] > 0:
        promedio_conexiones = info['conexiones'] * 2 / info['usuarios']
        print(f"\n📈 Promedio de conexiones por usuario: {promedio_conexiones:.2f}")
