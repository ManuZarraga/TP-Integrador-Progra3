"""
Módulo con datos iniciales de ejemplo para la red social.
"""

from red_social import RedSocial


def crear_red_ejemplo():
    """
    Crea una red social de ejemplo con múltiples usuarios y conexiones.
    
    Representa una red universitaria con diferentes facultades y niveles de interacción.
    
    Returns:
        RedSocial: Red social inicializada con datos de ejemplo
    """
    red = RedSocial()
    
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
    
    return red
