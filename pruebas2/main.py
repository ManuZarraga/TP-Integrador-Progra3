"""
Módulo principal del Sistema de Red Social Universitaria.

Estructura modular:
- interfaz.py: Funciones de interfaz de usuario
- menu_opciones.py: Opciones del menú
- datos_ejemplo.py: Datos iniciales
- red_social.py: Clase RedSocial
- algoritmos.py: Algoritmos principales
"""

from interfaz import (
    mostrar_menu, mostrar_estado_red, mostrar_bienvenida,
    mensaje_opcion_invalida, mensaje_despedida, esperar_continuar
)
from menu_opciones import (
    opcion_agregar_conexion, opcion_red_minima, opcion_recomendar_amigos,
    opcion_simular_bloqueo, opcion_analizar_complejidad
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
            mostrar_estado_red(red)
        
        elif opc == "2":
            opcion_agregar_conexion(red)
        
        elif opc == "3":
            opcion_red_minima(red)
        
        elif opc == "4":
            opcion_recomendar_amigos(red)
        
        elif opc == "5":
            opcion_simular_bloqueo(red)
        
        elif opc == "6":
            red = crear_red_ejemplo()
            print("✅ Red reiniciada con datos de ejemplo")
        
        elif opc == "7":
            mensaje_despedida()
            break
        
        else:
            mensaje_opcion_invalida()
        
        esperar_continuar()


if __name__ == "__main__":
    ejecutar()