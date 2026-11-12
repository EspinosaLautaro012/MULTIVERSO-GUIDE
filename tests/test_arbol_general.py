"""Pruebas del árbol general — se corre con: python3 tests/test_arbol_general.py"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.obra import Obra
from busqueda.arbol_general import ArbolGeneral
from gestor_datos import GestorDatos, saga_de

RUTA_DATOS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "obras.json")


def armar_arbol_chico():
    #   Raiz
    #   ├── A
    #   │   ├── A1
    #   │   └── A2
    #   └── B
    arbol = ArbolGeneral("Raiz")
    a = arbol.agregar_hijo(arbol.raiz, "A")
    b = arbol.agregar_hijo(arbol.raiz, "B")
    arbol.agregar_hijo(a, "A1")
    arbol.agregar_hijo(a, "A2")
    return arbol


def nombres(recorrido):
    return [nodo.nombre for _, nodo in recorrido]


def test_preorden():
    assert nombres(armar_arbol_chico().recorrido_preorden()) == ["Raiz", "A", "A1", "A2", "B"]
    print("OK - recorrido preorden")


def test_postorden():
    assert nombres(armar_arbol_chico().recorrido_postorden()) == ["A1", "A2", "A", "B", "Raiz"]
    print("OK - recorrido postorden")


def test_por_niveles():
    assert nombres(armar_arbol_chico().recorrido_por_niveles()) == ["Raiz", "A", "B", "A1", "A2"]
    print("OK - recorrido por niveles")


def test_buscar_y_camino():
    arbol = armar_arbol_chico()
    assert arbol.buscar("a2").nombre == "A2"          # sin distinguir mayúsculas
    assert arbol.buscar("No existe") is None
    assert arbol.camino_a("A2") == ["Raiz", "A", "A2"]
    assert arbol.camino_a("No existe") is None
    print("OK - buscar y camino desde la raíz")


def test_altura():
    assert armar_arbol_chico().altura() == 3
    print("OK - altura")


def test_obras_de_y_contar():
    arbol = ArbolGeneral("Raiz")
    cat = arbol.agregar_hijo(arbol.raiz, "Cat")
    for t in ["X", "Y", "Z"]:
        arbol.agregar_hijo(cat, t, Obra(t, "pelicula", 2020, 100, "Fase 1", 7.0))
    assert arbol.contar_obras() == 3
    assert [o.titulo for o in arbol.obras_de(cat)] == ["X", "Y", "Z"]
    print("OK - obras_de y contar_obras")


def test_saga_de():
    assert saga_de("Fase 1") == "Saga del Infinito"
    assert saga_de("Fase 3") == "Saga del Infinito"
    assert saga_de("Fase 4") == "Saga del Multiverso"
    assert saga_de("Saga del Infinito") == "Saga del Infinito"
    print("OK - mapeo de fase a saga")


def test_jerarquia_con_datos_reales():
    gestor = GestorDatos(RUTA_DATOS)
    jerarquia = gestor.jerarquia
    assert jerarquia.contar_obras() == len(gestor.obras), "Todas las obras deben estar en el árbol"
    assert jerarquia.camino_a("Iron Man") == ["Marvel", "Saga del Infinito", "Películas", "Iron Man"]
    assert jerarquia.camino_a("Loki") == ["Marvel", "Saga del Multiverso", "Series", "Loki"]
    print("OK - jerarquía armada con los datos reales")


if __name__ == "__main__":
    test_preorden()
    test_postorden()
    test_por_niveles()
    test_buscar_y_camino()
    test_altura()
    test_obras_de_y_contar()
    test_saga_de()
    test_jerarquia_con_datos_reales()
    print("\nTodas las pruebas del árbol general pasaron correctamente.")
