"""Pruebas de BFS y DFS — se corre con: python3 tests/test_recorridos.py"""
import sys
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from models.obra import Obra
from busqueda.grafo import Grafo
from busqueda.recorridos import bfs, dfs, camino_mas_corto, componentes_conexas
from gestor_datos import GestorDatos

RUTA_DATOS = os.path.join(RAIZ, "data", "obras.json")


def conectar(grafo, a, b):
    grafo.agregar_arista(a, b, 1, ["x"])
    grafo.agregar_arista(b, a, 1, ["x"])


def grafo_ejemplo():
    #   A --- B
    #   |     |
    #   C --- D --- E        F (aislada)
    grafo = Grafo()
    for t in "ABCDEF":
        grafo.agregar_vertice(Obra(t, "pelicula", 2020, 100, "Fase de prueba", 7.0))
    for a, b in [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E")]:
        conectar(grafo, a, b)
    return grafo


def test_bfs_visita_por_distancia():
    resultado = bfs(grafo_ejemplo(), "A")
    assert resultado == [("A", 0), ("B", 1), ("C", 1), ("D", 2), ("E", 3)], resultado
    distancias = [d for _, d in resultado]
    assert distancias == sorted(distancias), "BFS visita de menor a mayor distancia"
    print("OK - BFS visita por niveles de distancia")


def test_dfs_se_mete_hasta_el_fondo():
    resultado = dfs(grafo_ejemplo(), "A")
    assert resultado == [("A", 0), ("B", 1), ("D", 2), ("C", 3), ("E", 3)], resultado
    print("OK - DFS baja por un camino hasta el fondo y después vuelve")


def test_dfs_no_da_la_distancia_minima_pero_bfs_si():
    grafo = grafo_ejemplo()
    distancia_bfs = dict(bfs(grafo, "A"))
    profundidad_dfs = dict(dfs(grafo, "A"))
    assert distancia_bfs["C"] == 1
    assert profundidad_dfs["C"] == 3, "El DFS llegó a C dando una vuelta larga"
    print("OK - BFS da la distancia mínima; la profundidad del DFS puede ser mayor")


def test_ambos_visitan_lo_mismo():
    grafo = grafo_ejemplo()
    assert {t for t, _ in bfs(grafo, "A")} == {t for t, _ in dfs(grafo, "A")} == set("ABCDE")
    assert bfs(grafo, "F") == [("F", 0)] and dfs(grafo, "F") == [("F", 0)]
    assert bfs(grafo, "Z") == [] and dfs(grafo, "Z") == []
    print("OK - BFS y DFS alcanzan las mismas obras (y manejan aislada / inexistente)")


def test_camino_mas_corto():
    grafo = grafo_ejemplo()
    assert camino_mas_corto(grafo, "A", "E") == ["A", "B", "D", "E"]
    assert camino_mas_corto(grafo, "A", "C") == ["A", "C"]
    assert camino_mas_corto(grafo, "A", "A") == ["A"]
    assert camino_mas_corto(grafo, "A", "F") is None, "F no está conectada"
    assert camino_mas_corto(grafo, "A", "Z") is None, "Z no existe"
    assert camino_mas_corto(grafo, "Z", "A") is None
    print("OK - camino más corto (incluye sin camino y obra inexistente)")


def test_grupos_conectados():
    grupos = componentes_conexas(grafo_ejemplo())
    assert sorted(len(g) for g in grupos) == [1, 5]
    assert set(max(grupos, key=len)) == set("ABCDE")
    print("OK - grupos de obras conectadas (DFS)")


def test_dfs_no_se_rompe_con_cadenas_largas():
    # Una cadena de 3000 obras: un DFS recursivo superaría el límite de
    # recursión de Python (1000). El iterativo no.
    grafo = Grafo()
    cantidad = 3000
    for i in range(cantidad):
        grafo.agregar_vertice(Obra(f"O{i}", "pelicula", 2020, 100, "Fase de prueba", 7.0))
    for i in range(cantidad - 1):
        conectar(grafo, f"O{i}", f"O{i + 1}")
    resultado = dfs(grafo, "O0")
    assert len(resultado) == cantidad and resultado[-1] == (f"O{cantidad - 1}", cantidad - 1)
    assert len(camino_mas_corto(grafo, "O0", f"O{cantidad - 1}")) == cantidad
    print("OK - DFS y BFS soportan una cadena de 3000 obras sin recursión")


def test_con_datos_reales():
    gestor = GestorDatos(RUTA_DATOS)

    camino = gestor.camino_mas_corto("Iron Man", "Spider-Man: No Way Home")
    assert [o.titulo for o in camino] == ["Iron Man", "Avengers: Infinity War", "Spider-Man: No Way Home"]
    assert gestor.camino_mas_corto("Iron Man", "Loki") is None

    cercanas = gestor.obras_por_distancia("Iron Man")
    assert {o.titulo for o, d in cercanas if d == 1} == {"Avengers: Infinity War", "Avengers: Endgame"}
    assert all(d >= 1 for _, d in cercanas), "No debe incluir al origen"

    profundidad = {o.titulo: p for o, p in gestor.explorar_en_profundidad("Avengers: Infinity War")}
    distancia = {o.titulo: d for o, d in gestor.obras_por_distancia("Avengers: Infinity War")}
    assert distancia["Avengers: Endgame"] == 1 and profundidad["Avengers: Endgame"] == 2

    assert [len(g) for g in gestor.grupos_conectados()] == [5, 2, 1]
    print("OK - recorridos con los datos reales del catálogo")


if __name__ == "__main__":
    test_bfs_visita_por_distancia()
    test_dfs_se_mete_hasta_el_fondo()
    test_dfs_no_da_la_distancia_minima_pero_bfs_si()
    test_ambos_visitan_lo_mismo()
    test_camino_mas_corto()
    test_grupos_conectados()
    test_dfs_no_se_rompe_con_cadenas_largas()
    test_con_datos_reales()
    print("\nTodas las pruebas de los recorridos pasaron correctamente.")
