import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.setrecursionlimit(20000)  # el BST degenerado necesita más profundidad
                                # de la que Python permite por defecto (1000)

from models.obra import Obra
from busqueda.arbol import ArbolBusquedaObras
from busqueda.avl import ArbolAVL


def generar_obras_ordenadas(cantidad):
    """Genera obras con títulos YA ORDENADOS alfabéticamente
    (Obra0000, Obra0001, Obra0002, ...) — el peor caso posible
    para insertar en un BST común."""
    obras = []
    ancho = len(str(cantidad))
    for i in range(cantidad):
        titulo = f"Obra{str(i).zfill(ancho)}"
        obras.append(Obra(titulo, "pelicula", 2020, 120, "Fase de prueba", 7.0))
    return obras


def medir_tiempo(funcion, repeticiones=200):
    inicio = time.perf_counter()
    for _ in range(repeticiones):
        funcion()
    fin = time.perf_counter()
    return (fin - inicio) / repeticiones * 1000  # ms promedio


def correr_experimento_desbalance(tamanios):
    resultados = []

    for n in tamanios:
        obras = generar_obras_ordenadas(n)

        bst = ArbolBusquedaObras()
        avl = ArbolAVL()
        for obra in obras:
            bst.insertar(obra)
            avl.insertar(obra)

        titulo_buscado = obras[-1].titulo  # el último insertado, peor caso para BST

        altura_bst = bst.altura_total()
        altura_avl = avl.altura_total()

        repeticiones = 200 if n <= 1000 else 20
        tiempo_bst = medir_tiempo(lambda: bst.buscar(titulo_buscado), repeticiones)
        tiempo_avl = medir_tiempo(lambda: avl.buscar(titulo_buscado), repeticiones)

        resultados.append((n, altura_bst, altura_avl, tiempo_bst, tiempo_avl))

    return resultados


def imprimir_tabla(resultados):
    encabezado = f"{'N':<8}{'Altura BST':<13}{'Altura AVL':<13}{'Tiempo BST (ms)':<18}{'Tiempo AVL (ms)':<18}"
    print(encabezado)
    print("-" * len(encabezado))
    for n, h_bst, h_avl, t_bst, t_avl in resultados:
        print(f"{n:<8}{h_bst:<13}{h_avl:<13}{t_bst:<18.4f}{t_avl:<18.4f}")


if __name__ == "__main__":
    print("=== Caso de desbalance: títulos insertados YA ORDENADOS ===\n")
    tamanios = [100, 1000, 10000]
    resultados = correr_experimento_desbalance(tamanios)
    imprimir_tabla(resultados)

    print("\nAltura ideal (log2 n) de referencia:")
    import math
    for n in tamanios:
        print(f"  n={n}: log2({n}) ≈ {math.log2(n):.1f}")
