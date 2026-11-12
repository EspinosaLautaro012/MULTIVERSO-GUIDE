"""Compara las dos representaciones posibles del grafo (lista de adyacencia
vs matriz de adyacencia) sobre catálogos sintéticos de distinto tamaño.

Cada obra recibe 3 personajes tomados al azar de un conjunto de tantos
personajes como obras, así que cada personaje aparece en promedio en 3
obras. Es un catálogo inventado: sirve para ver cómo escala cada
representación, no para describir el MCU real.
"""
import sys
import os
import random
import time
import tracemalloc

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.obra import Obra
from busqueda.grafo import construir_grafo_por_personajes


def generar_catalogo(cantidad, semilla=11):
    random.seed(semilla)
    pool = [f"Personaje{i}" for i in range(cantidad)]
    obras = []
    for i in range(cantidad):
        personajes = random.sample(pool, 3)
        obras.append(Obra(f"Obra{i:05d}", "pelicula", 2020, random.randint(90, 180),
                          "Fase de prueba", 7.0, personajes))
    return obras


def construir_matriz(grafo, titulos):
    """Matriz V x V: matriz[i][j] = peso del arco i -> j (0 si no hay)."""
    indice = {titulo: i for i, titulo in enumerate(titulos)}
    n = len(titulos)
    matriz = [[0] * n for _ in range(n)]
    for titulo in titulos:
        for arista in grafo.vecinos(titulo):
            matriz[indice[titulo]][indice[arista.destino]] = arista.peso
    return matriz, indice


def memoria_kb(funcion):
    tracemalloc.start()
    resultado = funcion()
    _, pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return resultado, pico / 1024


def medir_vecinos(consulta, titulos, repeticiones=300):
    random.seed(3)
    elegidos = [random.choice(titulos) for _ in range(repeticiones)]
    inicio = time.perf_counter()
    for t in elegidos:
        consulta(t)
    return (time.perf_counter() - inicio) / repeticiones * 1e6  # microsegundos


def correr(tamanios):
    filas = []
    for n in tamanios:
        obras = generar_catalogo(n)
        titulos = [o.titulo for o in obras]

        grafo, mem_lista = memoria_kb(lambda: construir_grafo_por_personajes(obras))
        (matriz, indice), mem_matriz = memoria_kb(lambda: construir_matriz(grafo, titulos))

        t_lista = medir_vecinos(lambda t: grafo.vecinos(t), titulos)
        t_matriz = medir_vecinos(
            lambda t: [j for j, peso in enumerate(matriz[indice[t]]) if peso], titulos)

        filas.append((n, grafo.cantidad_aristas(), grafo.densidad(),
                      mem_lista, mem_matriz, t_lista, t_matriz))
    return filas


if __name__ == "__main__":
    filas = correr([200, 1000, 2000])
    cab = (f"{'Obras':<8}{'Arcos':<9}{'Densidad':<10}{'Mem. lista (KB)':<17}"
           f"{'Mem. matriz (KB)':<18}{'Vecinos lista (us)':<20}{'Vecinos matriz (us)':<20}")
    print(cab)
    print("-" * len(cab))
    for n, arcos, dens, ml, mm, tl, tm in filas:
        print(f"{n:<8}{arcos:<9}{dens:<10.2%}{ml:<17.0f}{mm:<18.0f}{tl:<20.1f}{tm:<20.1f}")
