"""Experimentos de BFS y DFS sobre catálogos sintéticos (mismo generador del
TP7: cada obra con 3 personajes al azar de un conjunto de tantos personajes
como obras). Sirven para ver cómo escalan los algoritmos, no para describir
el MCU real.
"""
import gc
import sys
import os
import random
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from experimentos.tp7_representacion import generar_catalogo
from busqueda.grafo import construir_grafo_por_personajes
from busqueda.recorridos import bfs, dfs


def medir_ms(funcion, repeticiones=5):
    inicio = time.perf_counter()
    for _ in range(repeticiones):
        funcion()
    return (time.perf_counter() - inicio) / repeticiones * 1000


def experimento_escalabilidad(tamanios):
    """Tiempo de un BFS y un DFS completos desde una obra."""
    filas = []
    for n in tamanios:
        obras = generar_catalogo(n)
        grafo = construir_grafo_por_personajes(obras)
        origen = obras[0].titulo

        alcanzadas = len(bfs(grafo, origen))
        assert alcanzadas == len(dfs(grafo, origen)), "Deben alcanzar las mismas obras"

        t_bfs = medir_ms(lambda: bfs(grafo, origen))
        t_dfs = medir_ms(lambda: dfs(grafo, origen))

        # Mismo recorrido con el recolector de basura de Python apagado,
        # para separar el costo del algoritmo del costo de la memoria.
        gc.disable()
        try:
            t_bfs_sin_gc = medir_ms(lambda: bfs(grafo, origen))
            t_dfs_sin_gc = medir_ms(lambda: dfs(grafo, origen))
        finally:
            gc.enable()

        filas.append((n, grafo.cantidad_aristas(), alcanzadas,
                      t_bfs, t_dfs, t_bfs_sin_gc, t_dfs_sin_gc))
    return filas


def experimento_calidad_de_camino(n=2000, pares=300, semilla=5):
    """Para pares de obras del mismo grupo conectado, compara la cantidad de
    pasos del camino que da el BFS (el mínimo) con los que da el DFS."""
    obras = generar_catalogo(n)
    grafo = construir_grafo_por_personajes(obras)
    random.seed(semilla)

    distancias_bfs, pasos_dfs = [], []
    while len(distancias_bfs) < pares:
        origen = random.choice(obras).titulo
        alcanzables = bfs(grafo, origen)
        destino, distancia = random.choice(alcanzables)
        if distancia == 0:
            continue
        distancias_bfs.append(distancia)
        pasos_dfs.append(dict(dfs(grafo, origen))[destino])

    return distancias_bfs, pasos_dfs


if __name__ == "__main__":
    print("=== Experimento 1: tiempo de un recorrido completo ===\n")
    cab = (f"{'Obras':<8}{'Arcos':<9}{'Alcanzadas':<12}{'BFS (ms)':<10}{'DFS (ms)':<10}"
           f"{'BFS sin GC':<12}{'DFS sin GC':<12}")
    print(cab)
    print("-" * len(cab))
    for n, arcos, alc, t_b, t_d, t_bs, t_ds in experimento_escalabilidad([1000, 5000, 20000]):
        print(f"{n:<8}{arcos:<9}{alc:<12}{t_b:<10.2f}{t_d:<10.2f}{t_bs:<12.2f}{t_ds:<12.2f}")

    print("\n=== Experimento 2: largo del camino que encuentra cada algoritmo ===")
    bfs_d, dfs_d = experimento_calidad_de_camino()
    print(f"({len(bfs_d)} pares de obras al azar, catálogo de 2000 obras)\n")
    print(f"{'':<22}{'Promedio':<12}{'Máximo':<10}")
    print("-" * 44)
    print(f"{'Pasos con BFS':<22}{sum(bfs_d) / len(bfs_d):<12.1f}{max(bfs_d):<10}")
    print(f"{'Pasos con DFS':<22}{sum(dfs_d) / len(dfs_d):<12.1f}{max(dfs_d):<10}")
    mas_largos = sum(1 for b, d in zip(bfs_d, dfs_d) if d > b)
    print(f"\nEl camino del DFS fue más largo que el mínimo en {mas_largos} de {len(bfs_d)} pares.")
