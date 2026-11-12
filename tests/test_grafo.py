"""Pruebas del grafo — se corre con: python3 tests/test_grafo.py"""
import sys
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from models.obra import Obra
from busqueda.grafo import Grafo
from gestor_datos import GestorDatos

RUTA_DATOS = os.path.join(RAIZ, "data", "obras.json")


def obra(titulo, duracion=100):
    return Obra(titulo, "pelicula", 2020, duracion, "Fase de prueba", 7.0)


def grafo_chico():
    #  A -- B -- C        D (aislada)
    grafo = Grafo()
    for t in "ABCD":
        grafo.agregar_vertice(obra(t))
    grafo.agregar_arista("A", "B", 10, ["x"])
    grafo.agregar_arista("B", "A", 20, ["x"])
    grafo.agregar_arista("B", "C", 30, ["y"])
    grafo.agregar_arista("C", "B", 40, ["y"])
    return grafo


def test_grafo_vacio():
    grafo = Grafo()
    assert grafo.cantidad_vertices() == 0 and grafo.cantidad_aristas() == 0
    assert grafo.densidad() == 0.0
    assert grafo.vecinos("X") == [] and grafo.grado("X") == 0
    print("OK - grafo vacío")


def test_vertices_y_aristas():
    grafo = grafo_chico()
    assert grafo.cantidad_vertices() == 4
    assert grafo.cantidad_aristas() == 4
    assert grafo.existe_arista("A", "B") and grafo.existe_arista("B", "A")
    assert not grafo.existe_arista("A", "C")
    assert grafo.grado("B") == 2 and grafo.grado("D") == 0
    assert [o.titulo for o in grafo.aislados()] == ["D"]
    print("OK - vértices, aristas, grado y aislados")


def test_los_pesos_dependen_del_sentido():
    grafo = grafo_chico()
    assert grafo.obtener_arista("A", "B").peso == 10
    assert grafo.obtener_arista("B", "A").peso == 20
    assert grafo.obtener_arista("A", "B").personajes == ["x"]
    print("OK - el peso depende del sentido (grafo dirigido)")


def test_no_duplica_aristas_y_valida_extremos():
    grafo = grafo_chico()
    grafo.agregar_arista("A", "B", 99)  # reemplaza, no duplica
    assert grafo.grado("A") == 1 and grafo.obtener_arista("A", "B").peso == 99
    for origen, destino in [("A", "Z"), ("Z", "A"), ("A", "A")]:
        try:
            grafo.agregar_arista(origen, destino)
            assert False, f"Debió rechazar {origen}->{destino}"
        except ValueError:
            pass
    print("OK - no duplica aristas y rechaza extremos inválidos")


def test_densidad():
    grafo = grafo_chico()
    assert abs(grafo.densidad() - 4 / (4 * 3)) < 1e-9
    print("OK - densidad")


def test_grafo_con_datos_reales():
    gestor = GestorDatos(RUTA_DATOS)
    grafo = gestor.grafo
    assert grafo.cantidad_vertices() == len(gestor.obras)

    # Las conexiones salen de los personajes compartidos
    assert gestor.conexion_entre("Iron Man", "Avengers: Infinity War") == ["Tony Stark"]
    assert gestor.conexion_entre("Avengers: Infinity War", "Avengers: Endgame") == ["Thanos", "Tony Stark"]
    assert gestor.conexion_entre("Iron Man", "Loki") is None

    # Cada conexión existe en los dos sentidos, y el peso es la duración del destino
    assert grafo.cantidad_aristas() % 2 == 0
    assert grafo.obtener_arista("Iron Man", "Avengers: Infinity War").peso == 149
    assert grafo.obtener_arista("Avengers: Infinity War", "Iron Man").peso == 126

    # Obra sin personajes en común con nadie
    assert [o.titulo for o in grafo.aislados()] == ["Secret Invasion"]

    # La suma de grados coincide con la cantidad de arcos
    assert sum(grafo.grado(o.titulo) for o in grafo.vertices()) == grafo.cantidad_aristas()
    print("OK - grafo armado con los datos reales")


def test_obras_conectadas_ordenadas_por_personajes_compartidos():
    gestor = GestorDatos(RUTA_DATOS)
    conectadas = gestor.obras_conectadas("Avengers: Infinity War")
    titulos = [o.titulo for o, _ in conectadas]
    assert titulos[0] == "Avengers: Endgame", "La que más personajes comparte va primera"
    assert len(titulos) == 4
    assert gestor.obras_conectadas("Secret Invasion") == []
    assert gestor.obras_conectadas("No existe") == []
    print("OK - obras conectadas (orden y casos sin conexiones)")


if __name__ == "__main__":
    test_grafo_vacio()
    test_vertices_y_aristas()
    test_los_pesos_dependen_del_sentido()
    test_no_duplica_aristas_y_valida_extremos()
    test_densidad()
    test_grafo_con_datos_reales()
    test_obras_conectadas_ordenadas_por_personajes_compartidos()
    print("\nTodas las pruebas del grafo pasaron correctamente.")
