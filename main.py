"""
Módulo principal del Sistema de Red Social Universitaria.

Estructura modular:
- interfaz.py: Funciones de interfaz de usuario
- menu_opciones.py: Funciones para cada opción del menú
- datos_ejemplo.py: Datos iniciales
- red_social.py: Clase RedSocial
- algoritmos.py: Algoritmos principales
"""

from interfaz import mostrar_menu, mostrar_estado_red, mostrar_bienvenida, mensaje_despedida
from menu_opciones import (
    opcion_agregar_conexion, opcion_red_minima, opcion_sugerir_amigos,
    opcion_simular_bloqueo
)
from datos_ejemplo import crear_red_ejemplo


def ejecutar():
    """
    Función principal del programa.
    Gestiona el flujo de ejecución y el bucle principal del menú.
    """
    red = crear_red_ejemplo()
    mostrar_bienvenida(red)
    
    while True:
        opc = mostrar_menu()
        
        if opc == "1":
            opcion_agregar_conexion(red)
        
        elif opc == "2":
            opcion_red_minima(red)
        
        elif opc == "3":
            opcion_sugerir_amigos(red)
        
        elif opc == "4":
            opcion_simular_bloqueo(red)
        
        elif opc == "5":
            mostrar_estado_red(red)
        
        elif opc == "6":
            mensaje_despedida()
            break
        
        else:
            print("❌ Opción inválida. Intente de nuevo.")


if __name__ == "__main__":
    ejecutar()