"""
Módulo con funciones de interfaz de usuario.
Maneja la presentación de información y menús.
"""


def mostrar_menu():
    """Muestra el menú principal y retorna la opción elegida."""
    print("\n" + "="*60)
    print("   SISTEMA DE RED SOCIAL UNIVERSITARIA")
    print("="*60)
    print("1. 📊 Ver estado actual de la red")
    print("2. ➕ Agregar nueva relación de amistad")
    print("3. 🌳 Calcular Red de Amistad Mínima (MST)")
    print("4. 🤝 Sugerir Amigos (Camino más corto)")
    print("5. 🚫 Simular Bloqueo y Restaurar Conectividad")
    print("6. 🔄 Reiniciar con red de ejemplo")
    print("7. ❌ Salir")
    print("="*60)
    return input("Elija una opción: ").strip()


def mostrar_estado_red(red):
    """Muestra información general sobre el estado de la red."""
    print("\n" + "="*60)
    print("ESTADO DE LA RED")
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
    
    print(f"\n📋 Usuarios en la red:")
    usuarios_ordenados = sorted(red.usuarios)
    for i in range(0, len(usuarios_ordenados), 5):
        print("   " + ", ".join(usuarios_ordenados[i:i+5]))


def mostrar_bienvenida(red):
    """Muestra el mensaje de bienvenida con información inicial."""
    print("🎓 Bienvenido al Sistema de Red Social Universitaria")
    print("Inicializando red de ejemplo...")
    print(f"✅ Red cargada con {len(red.usuarios)} usuarios y {len(red.aristas)} conexiones")


def mensaje_opcion_invalida():
    """Muestra mensaje de opción inválida."""
    print("❌ Opción inválida. Por favor, elija una opción del 1 al 7.")


def mensaje_despedida():
    """Muestra mensaje de despedida."""
    print("\n👋 ¡Gracias por usar el sistema! Hasta pronto.")


def esperar_continuar():
    """Pausa la ejecución esperando que el usuario presione ENTER."""
    input("\nPresione ENTER para continuar...")
