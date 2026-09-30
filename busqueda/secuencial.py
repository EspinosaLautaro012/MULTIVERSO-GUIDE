def busqueda_secuencial(obras, titulo):
    """Recorre la lista de obras una por una hasta encontrar el título.

    Complejidad:
        Mejor caso (Ω): O(1) — el elemento buscado es el primero.
        Peor caso (O):  O(n) — el elemento está al final o no existe,
                         hay que recorrer las n obras.
        Caso promedio (Θ): O(n) — en promedio hay que recorrer la mitad
                            de la lista, y eso sigue siendo lineal en n.
    """
    for obra in obras:
        if obra.titulo == titulo:
            return obra
    return None
