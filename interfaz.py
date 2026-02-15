"""
Módulo con funciones de interfaz de usuario.
Maneja la presentación de menús e información.
"""


def mostrar_menu():
    """Muestra el menú principal y retorna la opción elegida."""
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


def mostrar_estado_red(red):
    """Muestra el estado actual de la red social."""
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


def mostrar_bienvenida(red):
    """Muestra el mensaje de bienvenida."""
    print("Inicializando red social con múltiples conexiones...\n")
    print(f"✅ Red cargada con {len(red.usuarios)} usuarios y {len(red.aristas)} conexiones\n")


def mostrar_red_minima(mst, costo):
    """Muestra el resultado del algoritmo de red mínima."""
    print(f"\n🌳 Red Mínima necesaria (Costo total: {costo}):")
    for a in mst:
        print(f"  • {a['u']:12} -- {a['v']:12} (Costo: {a['peso']})")


def mostrar_recomendaciones(usuario, distancias):
    """Muestra las recomendaciones de amigos."""
    print(f"\n🤝 Distancias desde {usuario}:")
    for usr, dist in sorted(distancias.items()):
        if dist != float('inf'):
            print(f"  • {usr:12} - Distancia: {dist}")


def mostrar_bloqueo_resultado(u1, u2, componentes, nuevas, costo):
    """Muestra el resultado del bloqueo y restauración."""
    print(f"\n🚫 Bloqueo realizado: {u1} ⛔ {u2}")
    print(f"Evaluando conectividad...")
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


def mensaje_error(texto):
    """Muestra un mensaje de error."""
    print(f"❌ {texto}")


def mensaje_exito(texto):
    """Muestra un mensaje de éxito."""
    print(f"✅ {texto}")


def mensaje_despedida():
    """Muestra mensaje de despedida."""
    print("\n👋 ¡Gracias por usar el sistema! Hasta pronto.")
