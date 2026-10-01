"""Pruebas manuales del árbol binario de búsqueda.

Se corre con: python3 tests/test_arbol.py
No usa librerías externas (sin pytest), para no agregar dependencias.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.obra import Obra
from busqueda.arbol import ArbolBusquedaObras


def obra_de_prueba(titulo, anio=2020):
    return Obra(titulo, "pelicula", anio, 120, "Fase de prueba", 7.0)


def test_insertar_y_buscar():
    arbol = ArbolBusquedaObras()
    titulos = ["Matrix", "Inception", "Titanic", "Avatar", "Joker"]
    for t in titulos:
        arbol.insertar(obra_de_prueba(t))

    for t in titulos:
        resultado = arbol.buscar(t)
        assert resultado is not None, f"No encontró '{t}'"
        assert resultado.titulo == t

    assert arbol.buscar("No Existe") is None
    print("OK - insertar y buscar")


def test_arbol_vacio():
    arbol = ArbolBusquedaObras()
    assert arbol.esta_vacio()
    assert arbol.buscar("Cualquiera") is None
    print("OK - árbol vacío")


def test_recorrido_inorder_queda_ordenado():
    arbol = ArbolBusquedaObras()
    titulos = ["Matrix", "Inception", "Titanic", "Avatar", "Joker"]
    for t in titulos:
        arbol.insertar(obra_de_prueba(t))

    inorder = [obra.titulo for obra in arbol.recorrido_inorder()]
    assert inorder == sorted(titulos), f"No quedó ordenado: {inorder}"
    print("OK - recorrido inorder (orden alfabético correcto)")


def test_recorrido_preorder_empieza_en_raiz():
    arbol = ArbolBusquedaObras()
    arbol.insertar(obra_de_prueba("Matrix"))
    arbol.insertar(obra_de_prueba("Inception"))
    arbol.insertar(obra_de_prueba("Titanic"))

    preorder = [obra.titulo for obra in arbol.recorrido_preorder()]
    assert preorder[0] == "Matrix", "El preorder debería arrancar en la raíz"
    assert set(preorder) == {"Matrix", "Inception", "Titanic"}
    print("OK - recorrido preorder")


def test_recorrido_postorder_termina_en_raiz():
    arbol = ArbolBusquedaObras()
    arbol.insertar(obra_de_prueba("Matrix"))
    arbol.insertar(obra_de_prueba("Inception"))
    arbol.insertar(obra_de_prueba("Titanic"))

    postorder = [obra.titulo for obra in arbol.recorrido_postorder()]
    assert postorder[-1] == "Matrix", "El postorder debería terminar en la raíz"
    assert set(postorder) == {"Matrix", "Inception", "Titanic"}
    print("OK - recorrido postorder")


if __name__ == "__main__":
    test_arbol_vacio()
    test_insertar_y_buscar()
    test_recorrido_inorder_queda_ordenado()
    test_recorrido_preorder_empieza_en_raiz()
    test_recorrido_postorder_termina_en_raiz()
    print("\nTodas las pruebas del árbol pasaron correctamente.")
