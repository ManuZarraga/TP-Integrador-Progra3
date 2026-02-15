"""
Módulo con funciones para cada opción del menú.
"""

import algoritmos
from interfaz import (
    mensaje_error, mensaje_exito, mostrar_red_minima,
    mostrar_recomendaciones, mostrar_bloqueo_resultado
)


def opcion_agregar_conexion(red):
    """Opción 1: Agregar una nueva conexión a la red."""
    u1 = input("Usuario 1: ").strip()
    u2 = input("Usuario 2: ").strip()
    
    if not u1 or not u2:
        mensaje_error("Los nombres no pueden estar vacíos")
        return
    
    if u1 == u2:
        mensaje_error("Un usuario no puede conectarse consigo mismo")
        return
    
    try:
        p = int(input("Peso/Interacciones: ").strip())
        if p < 0:
            mensaje_error("El peso debe ser positivo")
            return
        
        red.agregar_conexion(u1, u2, p)
        mensaje_exito("Conexión agregada.")
    except ValueError:
        mensaje_error("El peso debe ser un número entero.")


def opcion_red_minima(red):
    """Opción 2: Calcular y mostrar la red de amistad mínima."""
    if len(red.usuarios) == 0:
        mensaje_error("La red está vacía.")
        return
    
    mst, costo = algoritmos.obtener_red_minima(red)
    mostrar_red_minima(mst, costo)


def opcion_sugerir_amigos(red):
    """Opción 3: Generar recomendaciones de amigos."""
    usr = input("Usuario para recomendaciones: ").strip()
    
    if usr not in red.usuarios:
        mensaje_error("Usuario no encontrado.")
        return
    
    distancias = algoritmos.recomendar_amigos(red, usr)
    mostrar_recomendaciones(usr, distancias)


def opcion_simular_bloqueo(red):
    """Opción 4: Simular un bloqueo y restaurar conectividad."""
    if len(red.aristas) == 0:
        mensaje_error("No hay conexiones en la red.")
        return
    
    u1 = input("Usuario que bloquea: ").strip()
    u2 = input("Usuario bloqueado: ").strip()
    
    # Validaciones
    if u1 not in red.usuarios or u2 not in red.usuarios:
        mensaje_error("Uno o ambos usuarios no existen.")
        return
    
    # Verificar si existe la conexión
    conexion_existe = any(
        (a['u'] == u1 and a['v'] == u2) or (a['u'] == u2 and a['v'] == u1)
        for a in red.aristas
    )
    
    if not conexion_existe:
        mensaje_error(f"No existe conexión directa entre {u1} y {u2}")
        return
    
    # Eliminar la conexión
    red.aristas = [a for a in red.aristas if not (
        (a['u'] == u1 and a['v'] == u2) or (a['u'] == u2 and a['v'] == u1))]
    
    red.adyacencia[u1] = [(vec, peso) for vec, peso in red.adyacencia[u1] if vec != u2]
    red.adyacencia[u2] = [(vec, peso) for vec, peso in red.adyacencia[u2] if vec != u1]
    
    # Generar candidatos de reconexión automáticamente
    posibles = _generar_candidatos(red)
    
    # Buscar solución
    nuevas, costo = algoritmos.restaurar_red(red, posibles if posibles else [])
    componentes = red.obtener_componentes()
    
    # Mostrar resultado
    mostrar_bloqueo_resultado(u1, u2, componentes, nuevas, costo)


def _generar_candidatos(red):
    """
    Genera automáticamente los candidatos de reconexión.
    Retorna las conexiones posibles que no existen actualmente.
    """
    posibles = []
    usuarios_lista = sorted(red.usuarios)
    
    # Crear set de conexiones existentes
    existentes = set()
    for a in red.aristas:
        existentes.add((min(a['u'], a['v']), max(a['u'], a['v'])))
    
    # Generar posibles conexiones que no existen
    for i, usuario1 in enumerate(usuarios_lista):
        for usuario2 in usuarios_lista[i+1:]:
            if (usuario1, usuario2) not in existentes:
                posibles.append((usuario1, usuario2, 5))  # Peso por defecto
    
    return posibles
