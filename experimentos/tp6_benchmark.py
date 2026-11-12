import sys
import os
import random
import time
from functools import cmp_to_key

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.obra import Obra
from busqueda.heap import HeapMaximos

K = 10  # cantidad de obras del ranking


def generar_elementos(cantidad, semilla=7):
    """Obras de prueba con un puntaje aleatorio de 0 a 10."""
    random.seed(semilla)
    elementos = []
    for i in range(cantidad):
        obra = Obra(f"Obra{i:07d}", "pelicula", 2020, 120, "Fase de prueba", 7.0)
        elementos.append((round(random.uniform(0, 10), 4), obra))
    return elementos


def ordenar_y_cortar(elementos, k):
    """Estrategia 'ordenar todo': ordena el catálogo entero y se queda
    con los primeros k. Cuenta cuántas comparaciones hace el ordenamiento."""
    contador = [0]

    def comparar(a, b):
        contador[0] += 1
        if a[0] != b[0]:
            return -1 if a[0] > b[0] else 1
        return -1 if a[1].titulo < b[1].titulo else 1

    ordenados = sorted(elementos, key=cmp_to_key(comparar))
    return ordenados[:k], contador[0]


def heap_top_k(elementos, k):
    """Estrategia 'heap': arma la heap (O(n)) y extrae solo los k mejores."""
    heap = HeapMaximos.desde_lista(elementos)
    resultado = heap.top_n(k)
    return resultado, heap.comparaciones


def experimento_una_consulta(tamanios):
    """Un solo Top-K sobre un catálogo de n obras."""
    filas = []
    for n in tamanios:
        elementos = generar_elementos(n)

        t0 = time.perf_counter()
        top_sort, comp_sort = ordenar_y_cortar(elementos, K)
        t_sort = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        top_heap, comp_heap = heap_top_k(elementos, K)
        t_heap = (time.perf_counter() - t0) * 1000

        assert [(p, o.titulo) for p, o in top_sort] == [(p, o.titulo) for p, o in top_heap], \
            "Las dos estrategias deben dar el mismo ranking"
        filas.append((n, comp_sort, comp_heap, t_sort, t_heap))
    return filas


def experimento_ranking_dinamico(n_inicial, rondas):
    """Ranking dinámico: en cada ronda llega UNA obra nueva y se pide
    el Top-K. 'Ordenar todo' reordena el catálogo en cada ronda; la heap
    persistente solo inserta la obra nueva y extrae los K mejores."""
    elementos = generar_elementos(n_inicial + rondas)
    base, nuevas = elementos[:n_inicial], elementos[n_inicial:]

    # Estrategia 1: ordenar todo cada vez
    catalogo = list(base)
    comp_sort_total = 0
    t0 = time.perf_counter()
    for nueva in nuevas:
        catalogo.append(nueva)
        top_sort, comparaciones = ordenar_y_cortar(catalogo, K)
        comp_sort_total += comparaciones
    t_sort = (time.perf_counter() - t0) * 1000

    # Estrategia 2: heap persistente
    heap = HeapMaximos.desde_lista(base)
    heap.comparaciones = 0
    t0 = time.perf_counter()
    for nueva in nuevas:
        heap.insertar(*nueva)
        top_heap = heap.top_n(K)
    t_heap = (time.perf_counter() - t0) * 1000

    assert [(p, o.titulo) for p, o in top_sort] == [(p, o.titulo) for p, o in top_heap]
    return comp_sort_total, heap.comparaciones, t_sort, t_heap


def imprimir_una_consulta(filas):
    cab = f"{'N':<9}{'Comp. ordenar':<16}{'Comp. heap':<13}{'Tiempo ordenar (ms)':<22}{'Tiempo heap (ms)':<18}"
    print(cab)
    print("-" * len(cab))
    for n, cs, ch, ts, th in filas:
        print(f"{n:<9}{cs:<16}{ch:<13}{ts:<22.2f}{th:<18.2f}")


if __name__ == "__main__":
    print(f"=== Experimento 1: UNA consulta Top-{K} sobre n obras ===\n")
    imprimir_una_consulta(experimento_una_consulta([1000, 10000, 100000]))

    n, rondas = 10000, 200
    print(f"\n=== Experimento 2: ranking dinámico "
          f"({n} obras, {rondas} rondas de 'llega una obra nueva + Top-{K}') ===\n")
    cs, ch, ts, th = experimento_ranking_dinamico(n, rondas)
    print(f"{'Estrategia':<22}{'Comparaciones':<17}{'Tiempo total (ms)':<20}")
    print("-" * 59)
    print(f"{'Ordenar todo':<22}{cs:<17}{ts:<20.1f}")
    print(f"{'Heap persistente':<22}{ch:<17}{th:<20.1f}")
