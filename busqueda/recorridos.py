"""Recorridos del grafo de obras: BFS (en anchura) y DFS (en profundidad).

Los dos visitan cada obra alcanzable una sola vez y recorren cada conexión
una sola vez, así que cuestan O(V + E) con lista de adyacencia. La
diferencia está en el ORDEN en que visitan:

    BFS  usa una COLA: visita primero todo lo que está a 1 paso, después a
         2 pasos, y así. Por eso encuentra el camino con menos pasos.
    DFS  usa una PILA: se mete lo más adentro posible por un camino y recién
         cuando no puede avanzar vuelve para atrás. Explora a fondo, pero
         el camino por el que llega a una obra NO es el más corto.

El orden exacto de visita depende del orden de las conexiones en la lista
de adyacencia (es siempre el mismo para los mismos datos).
"""
from collections import deque


def bfs(grafo, origen):
    """Recorrido en anchura desde una obra.

    Devuelve una lista de (título, distancia) en el orden en que se visitó,
    donde distancia es la cantidad de conexiones entre el origen y esa obra
    (el origen tiene distancia 0). Solo aparecen las obras alcanzables.
    Si la obra no existe, devuelve una lista vacía.

    Complejidad: tiempo O(V + E), espacio O(V) (cola y distancias).
    """
    if not grafo.tiene_vertice(origen):
        return []

    distancia = {origen: 0}
    cola = deque([origen])
    orden = []
    while cola:
        actual = cola.popleft()
        orden.append((actual, distancia[actual]))
        for arista in grafo.vecinos(actual):
            if arista.destino not in distancia:   # se marca al encolar, no al sacar
                distancia[arista.destino] = distancia[actual] + 1
                cola.append(arista.destino)
    return orden


def camino_mas_corto(grafo, origen, destino):
    """Camino con MENOS obras entre dos obras, usando BFS.

    Devuelve la lista de títulos desde el origen hasta el destino (ambos
    incluidos), o None si alguna no existe o no hay camino entre ellas.
    Corta apenas encuentra el destino, sin recorrer el resto del grafo.

    OJO: minimiza la cantidad de obras, no los minutos de contenido. Para
    minimizar minutos haría falta un algoritmo que use los pesos (Dijkstra).

    Complejidad: tiempo O(V + E) en el peor caso, espacio O(V).
    """
    if not (grafo.tiene_vertice(origen) and grafo.tiene_vertice(destino)):
        return None
    if origen == destino:
        return [origen]

    padre = {origen: None}
    cola = deque([origen])
    while cola:
        actual = cola.popleft()
        for arista in grafo.vecinos(actual):
            if arista.destino in padre:
                continue
            padre[arista.destino] = actual
            if arista.destino == destino:
                camino = []
                nodo = destino
                while nodo is not None:       # se reconstruye yendo hacia atrás
                    camino.append(nodo)
                    nodo = padre[nodo]
                camino.reverse()
                return camino
            cola.append(arista.destino)
    return None


def dfs(grafo, origen):
    """Recorrido en profundidad desde una obra.

    Devuelve una lista de (título, profundidad) en el orden en que se
    visitó. La profundidad es cuántos pasos hay que dar por el camino que
    siguió el DFS para llegar a esa obra (el origen tiene profundidad 0).
    Ojo: NO es la distancia mínima, es la del camino que le tocó al DFS.

    Está hecho con una pila explícita (no con recursión) para que un
    catálogo con cadenas largas de obras no supere el límite de recursión
    de Python. Visita en el mismo orden que la versión recursiva.

    Complejidad: tiempo O(V + E), espacio O(V) (pila y visitados).
    """
    if not grafo.tiene_vertice(origen):
        return []

    visitados = {origen}
    orden = [(origen, 0)]
    pila = [(origen, iter(grafo.vecinos(origen)))]   # (obra, conexiones que le faltan)
    while pila:
        _, pendientes = pila[-1]
        for arista in pendientes:
            if arista.destino not in visitados:
                visitados.add(arista.destino)
                orden.append((arista.destino, len(pila)))
                pila.append((arista.destino, iter(grafo.vecinos(arista.destino))))
                break                                 # baja un nivel más
        else:
            pila.pop()                                # sin pendientes: vuelve atrás
    return orden


def componentes_conexas(grafo):
    """Grupos de obras conectadas entre sí (directa o indirectamente),
    encontrados con DFS. Entre obras de grupos distintos no existe ningún
    camino. Sirve porque las conexiones del grafo son simétricas.

    Devuelve una lista de grupos, cada uno con los títulos de sus obras.
    Complejidad total: O(V + E), porque cada obra se visita una sola vez.
    """
    visitados = set()
    grupos = []
    for obra in grafo.vertices():
        if obra.titulo in visitados:
            continue
        grupo = [titulo for titulo, _ in dfs(grafo, obra.titulo)]
        visitados.update(grupo)
        grupos.append(grupo)
    return grupos
