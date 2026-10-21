"""Pruebas manuales del árbol AVL — se corre con: python3 tests/test_avl.py"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.obra import Obra
from busqueda.avl import ArbolAVL


def obra_de_prueba(titulo):
    return Obra(titulo, "pelicula", 2020, 120, "Fase de prueba", 7.0)


def factor_balance_de_todos_los_nodos(avl, nodo=None, primero=True):
    """Recorre el árbol y devuelve True si TODOS los nodos tienen
    factor de balance entre -1 y 1 (condición de un AVL válido)."""
    if primero:
        nodo = avl._raiz
    if nodo is None:
        return True
    balance = avl._factor_balance(nodo)
    if abs(balance) > 1:
        return False
    return (
        factor_balance_de_todos_los_nodos(avl, nodo.izquierda, False)
        and factor_balance_de_todos_los_nodos(avl, nodo.derecha, False)
    )


def test_rotacion_simple_derecha_caso_LL():
    # Insertar en orden descendente fuerza una rotación LL
    avl = ArbolAVL()
    for t in ["C", "B", "A"]:
        avl.insertar(obra_de_prueba(t))
    assert avl.altura_total() == 2, "Después de la rotación LL la altura debería ser 2, no 3"
    assert avl._raiz.obra.titulo == "B", "La raíz debería ser 'B' tras la rotación"
    print("OK - rotación LL (derecha)")


def test_rotacion_simple_izquierda_caso_RR():
    # Insertar en orden ascendente fuerza una rotación RR
    avl = ArbolAVL()
    for t in ["A", "B", "C"]:
        avl.insertar(obra_de_prueba(t))
    assert avl.altura_total() == 2, "Después de la rotación RR la altura debería ser 2, no 3"
    assert avl._raiz.obra.titulo == "B", "La raíz debería ser 'B' tras la rotación"
    print("OK - rotación RR (izquierda)")


def test_rotacion_doble_izquierda_derecha_caso_LR():
    # A, C, B -> fuerza rotación izquierda-derecha
    avl = ArbolAVL()
    for t in ["C", "A", "B"]:
        avl.insertar(obra_de_prueba(t))
    assert avl._raiz.obra.titulo == "B"
    print("OK - rotación LR (doble)")


def test_rotacion_doble_derecha_izquierda_caso_RL():
    # A, C, B -> fuerza rotación derecha-izquierda
    avl = ArbolAVL()
    for t in ["A", "C", "B"]:
        avl.insertar(obra_de_prueba(t))
    assert avl._raiz.obra.titulo == "B"
    print("OK - rotación RL (doble)")


def test_arbol_grande_queda_siempre_balanceado():
    # Insertar 200 títulos ya ordenados (el peor caso para un BST común)
    avl = ArbolAVL()
    for i in range(200):
        avl.insertar(obra_de_prueba(f"Obra{i:04d}"))

    assert factor_balance_de_todos_los_nodos(avl), "Hay nodos desbalanceados"

    import math
    altura_ideal = math.log2(200)
    assert avl.altura_total() <= altura_ideal * 1.5, (
        f"Altura {avl.altura_total()} muy lejos del ideal log2(200)={altura_ideal:.1f}"
    )
    print(f"OK - árbol de 200 nodos ordenados se mantiene balanceado "
          f"(altura real: {avl.altura_total()}, ideal: {altura_ideal:.1f})")


def test_busqueda_sigue_funcionando_tras_rotaciones():
    avl = ArbolAVL()
    titulos = [f"Obra{i:03d}" for i in range(50)]
    for t in titulos:
        avl.insertar(obra_de_prueba(t))

    for t in titulos:
        assert avl.buscar(t) is not None, f"No encontró '{t}' después de las rotaciones"

    assert avl.buscar("No Existe") is None
    print("OK - búsqueda correcta después de todas las rotaciones")


if __name__ == "__main__":
    test_rotacion_simple_derecha_caso_LL()
    test_rotacion_simple_izquierda_caso_RR()
    test_rotacion_doble_izquierda_derecha_caso_LR()
    test_rotacion_doble_derecha_izquierda_caso_RL()
    test_arbol_grande_queda_siempre_balanceado()
    test_busqueda_sigue_funcionando_tras_rotaciones()
    print("\nTodas las pruebas del AVL pasaron correctamente.")
