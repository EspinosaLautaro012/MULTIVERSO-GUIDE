import random
import string
import sys
import time
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.obra import Obra
from busqueda.secuencial import busqueda_secuencial
from busqueda.arbol import ArbolBusquedaObras


def generar_obras(cantidad, semilla=42):
    """Genera 'cantidad' de obras de prueba con títulos aleatorios únicos."""
    random.seed(semilla)
    titulos = set()
    while len(titulos) < cantidad:
        titulo = "".join(random.choices(string.ascii_uppercase, k=8))
        titulos.add(titulo)

    obras = []
    for titulo in titulos:
        obras.append(
            Obra(
                titulo=titulo,
                tipo="pelicula",
                anio=2020,
                duracion_min=120,
                fase="Fase de prueba",
                rating=7.0,
            )
        )
    return obras


def armar_arbol(obras):
    arbol = ArbolBusquedaObras()
    orden_aleatorio = obras[:]
    random.shuffle(orden_aleatorio)  # evita insertar ya ordenado (peor caso)
    for obra in orden_aleatorio:
        arbol.insertar(obra)
    return arbol


def medir_tiempo(funcion, repeticiones=200):
    inicio = time.perf_counter()
    for _ in range(repeticiones):
        funcion()
    fin = time.perf_counter()
    return (fin - inicio) / repeticiones * 1000  # ms promedio por búsqueda


def correr_experimento(tamanios, repeticiones=200):
    resultados = []

    for n in tamanios:
        obras = generar_obras(n)
        arbol = armar_arbol(obras)

        # Buscamos un título que existe pero está "lejos" del inicio
        # de la lista, para no favorecer artificialmente a la secuencial.
        titulo_buscado = obras[-1].titulo

        tiempo_secuencial = medir_tiempo(
            lambda: busqueda_secuencial(obras, titulo_buscado), repeticiones
        )
        tiempo_arbol = medir_tiempo(
            lambda: arbol.buscar(titulo_buscado), repeticiones
        )

        resultados.append((n, tiempo_secuencial, tiempo_arbol))

    return resultados


def imprimir_tabla(resultados):
    print(f"{'N elementos':<15}{'Búsqueda secuencial':<22}{'Búsqueda en árbol':<20}")
    print("-" * 57)
    for n, t_sec, t_arbol in resultados:
        print(f"{n:<15}{t_sec:<22.4f}{t_arbol:<20.4f}")


if __name__ == "__main__":
    tamanios = [100, 1000, 10000]
    resultados = correr_experimento(tamanios)
    imprimir_tabla(resultados)
