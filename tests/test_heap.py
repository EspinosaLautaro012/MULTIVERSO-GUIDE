"""Pruebas de la heap y el ranking — se corre con: python3 tests/test_heap.py"""
import sys
import os
import random

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from models.obra import Obra
from busqueda.heap import HeapMaximos
from busqueda.prioridad import calcular_prioridad
from gestor_datos import GestorDatos

RUTA_DATOS = os.path.join(RAIZ, "data", "obras.json")


def obra(titulo, rating=7.0, anio=2020, duracion=120):
    return Obra(titulo, "pelicula", anio, duracion, "Fase de prueba", rating)


def test_heap_vacia():
    heap = HeapMaximos()
    assert heap.esta_vacia() and len(heap) == 0
    assert heap.ver_max() is None
    assert heap.extraer_max() is None
    print("OK - heap vacía")


def test_extraer_sale_de_mayor_a_menor():
    heap = HeapMaximos()
    for puntaje in [5, 9, 1, 7, 3, 8]:
        heap.insertar(puntaje, obra(f"Obra{puntaje}"))
    assert heap.ver_max()[0] == 9
    salida = [heap.extraer_max()[0] for _ in range(6)]
    assert salida == [9, 8, 7, 5, 3, 1], f"Salió desordenado: {salida}"
    assert heap.esta_vacia()
    print("OK - extraer_max devuelve de mayor a menor")


def test_empate_desempata_por_titulo():
    heap = HeapMaximos()
    heap.insertar(7.0, obra("Zeta"))
    heap.insertar(7.0, obra("Alfa"))
    heap.insertar(7.0, obra("Medio"))
    orden = [heap.extraer_max()[1].titulo for _ in range(3)]
    assert orden == ["Alfa", "Medio", "Zeta"], f"Desempate incorrecto: {orden}"
    print("OK - desempate alfabético")


def test_desde_lista_equivale_a_insertar_de_a_uno():
    random.seed(1)
    elementos = [(random.randint(0, 1000) / 10, obra(f"T{i:04d}")) for i in range(500)]
    heap = HeapMaximos.desde_lista(elementos)
    salida = [heap.extraer_max() for _ in range(500)]
    esperado = sorted(elementos, key=lambda e: (-e[0], e[1].titulo))
    assert [(p, o.titulo) for p, o in salida] == [(p, o.titulo) for p, o in esperado]
    print("OK - desde_lista (heapify) coincide con el orden esperado en 500 elementos")


def test_top_n_no_modifica_la_heap():
    heap = HeapMaximos.desde_lista([(i, obra(f"O{i}")) for i in range(10)])
    top3 = heap.top_n(3)
    assert [p for p, _ in top3] == [9, 8, 7]
    assert len(heap) == 10, "top_n no debería sacar elementos de la heap original"
    assert len(heap.top_n(50)) == 10, "pedir más de los que hay devuelve todos"
    print("OK - top_n no modifica la heap")


def test_prioridad_dentro_de_rango_y_por_perfil():
    corta = obra("Corta", rating=8, anio=2024, duracion=100)
    larga = obra("Larga", rating=8, anio=2024, duracion=400)
    assert 0 <= calcular_prioridad(corta) <= 10
    assert calcular_prioridad(corta, "casual") > calcular_prioridad(larga, "casual"), \
        "Para el perfil casual la obra corta debería valer más"
    assert calcular_prioridad(corta, "fan") == calcular_prioridad(larga, "fan"), \
        "Para el perfil fan la duración no debería influir"
    print("OK - función de prioridad (rango y diferencia entre perfiles)")


def test_top_n_del_sistema_con_datos_reales():
    gestor = GestorDatos(RUTA_DATOS)
    ranking = gestor.top_n(5, perfil="casual")
    puntajes = [p for p, _ in ranking]
    assert len(ranking) == 5
    assert puntajes == sorted(puntajes, reverse=True), "El ranking debe venir ordenado"

    primero = ranking[0][1].titulo
    sin_primero = gestor.top_n(5, perfil="casual", excluir=[primero])
    assert primero not in [o.titulo for _, o in sin_primero], "La obra excluida no debe aparecer"
    assert len(gestor.top_n(100)) == len(gestor.obras), "Pedir de más devuelve todas, sin romper"
    print("OK - Top-N del sistema (orden, exclusión de vistas y N mayor al total)")


if __name__ == "__main__":
    test_heap_vacia()
    test_extraer_sale_de_mayor_a_menor()
    test_empate_desempata_por_titulo()
    test_desde_lista_equivale_a_insertar_de_a_uno()
    test_top_n_no_modifica_la_heap()
    test_prioridad_dentro_de_rango_y_por_perfil()
    test_top_n_del_sistema_con_datos_reales()
    print("\nTodas las pruebas de la heap pasaron correctamente.")
