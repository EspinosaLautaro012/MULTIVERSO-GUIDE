import json
import os
from models.obra import Obra
from busqueda.arbol import ArbolBusquedaObras
from busqueda.arbol_general import ArbolGeneral
from busqueda.heap import HeapMaximos
from busqueda.grafo import Grafo, construir_grafo_por_personajes
from busqueda.prioridad import calcular_prioridad

NOMBRES_TIPO = {"pelicula": "Películas", "serie": "Series", "comic": "Cómics"}


def saga_de(fase):
    """Devuelve el nombre de la saga a la que pertenece una fase.
    Fases 1-3 -> Saga del Infinito, fases 4-6 -> Saga del Multiverso.
    Si el dato ya viene como nombre de saga, se respeta tal cual."""
    texto = fase.lower()
    if "infinito" in texto:
        return "Saga del Infinito"
    if "multiverso" in texto:
        return "Saga del Multiverso"
    digitos = [c for c in texto if c.isdigit()]
    if digitos:
        numero = int("".join(digitos))
        return "Saga del Infinito" if numero <= 3 else "Saga del Multiverso"
    return fase


class GestorDatos:
    """Carga las obras desde un archivo JSON y ofrece las operaciones
    principales sobre esos datos: buscar, listar y filtrar.

    Desde el TP3, además de la lista plana de obras, se arma un árbol
    binario de búsqueda (ordenado por título) que se usa para la
    búsqueda exacta y para listar ordenado — ya no es un árbol aislado
    de prueba, sino parte real del flujo de datos de la app."""

    def __init__(self, ruta_json):
        self._ruta_json = ruta_json
        self._obras = []
        self._arbol = ArbolBusquedaObras()
        self._jerarquia = ArbolGeneral("Marvel")
        self._grafo = Grafo()
        self._cargar_datos()

    def _cargar_datos(self):
        if not os.path.exists(self._ruta_json):
            raise FileNotFoundError(f"No se encontró el archivo de datos: {self._ruta_json}")

        with open(self._ruta_json, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        self._obras = [
            Obra(
                titulo=item["titulo"],
                tipo=item["tipo"],
                anio=item["anio"],
                duracion_min=item["duracion_min"],
                fase=item["fase"],
                rating=item["rating"],
                personajes=item.get("personajes", []),
            )
            for item in datos
        ]

        for obra in self._obras:
            self._arbol.insertar(obra)

        self._construir_jerarquia()
        self._construir_grafo()

    def _construir_jerarquia(self):
        """Arma el árbol general: Marvel -> Saga -> Tipo -> Obra."""
        for obra in self._obras:
            saga = self._jerarquia.obtener_o_crear_hijo(
                self._jerarquia.raiz, saga_de(obra.fase))
            tipo = self._jerarquia.obtener_o_crear_hijo(
                saga, NOMBRES_TIPO.get(obra.tipo, obra.tipo.capitalize()))
            self._jerarquia.agregar_hijo(tipo, obra.titulo, obra)

    @property
    def obras(self):
        return list(self._obras)

    # --- Operación 1: Buscar (coincidencia parcial, recorrido secuencial) ---
    def buscar_por_titulo(self, texto):
        texto = texto.lower().strip()
        return [obra for obra in self._obras if texto in obra.titulo.lower()]

    # --- Búsqueda exacta usando el árbol (TP3) ---
    def buscar_exacto_arbol(self, titulo):
        """Busca una obra por título EXACTO usando el árbol binario de
        búsqueda, en vez de recorrer la lista entera. Pensada para cuando
        se conoce el título completo (ej. al seleccionar de una lista)."""
        return self._arbol.buscar(titulo.strip())

    # --- Listar ordenado alfabéticamente usando el árbol (TP3) ---
    def listar_ordenado_por_titulo(self):
        """Devuelve las obras ordenadas por título usando el recorrido
        inorder del árbol — más eficiente que ordenar la lista cada vez
        que se pide, porque el árbol ya mantiene el orden."""
        return self._arbol.recorrido_inorder()

    # --- Operación 2: Listar ---
    def listar_todas(self, orden_por_anio=True):
        if orden_por_anio:
            return sorted(self._obras, key=lambda obra: obra.anio)
        return list(self._obras)

    # --- Operación 3: Filtrar ---
    def filtrar(self, tipo=None, fase=None, personaje=None):
        resultado = self._obras

        if tipo:
            resultado = [o for o in resultado if o.tipo.lower() == tipo.lower()]
        if fase:
            resultado = [o for o in resultado if fase.lower() in o.fase.lower()]
        if personaje:
            resultado = [
                o for o in resultado
                if any(personaje.lower() in p.lower() for p in o.personajes)
            ]

        return resultado

    # --- Jerarquía de categorías (TP5, árbol general) ---
    @property
    def jerarquia(self):
        return self._jerarquia

    # --- Ranking de imprescindibles (TP6, heap) ---
    def top_n(self, n, perfil="casual", excluir=None):
        """Devuelve las n obras más prioritarias para el perfil dado, como
        lista de (puntaje, obra) de mayor a menor.

        Se arma una heap con todas las obras (O(n)) y se extraen solo las n
        primeras (O(n log m)), en vez de ordenar el catálogo completo cada
        vez. 'excluir' es una lista de títulos que no deben aparecer
        (por ejemplo, las obras que el usuario ya vio)."""
        excluir = set(excluir or [])
        elementos = [
            (calcular_prioridad(obra, perfil), obra)
            for obra in self._obras
            if obra.titulo not in excluir
        ]
        heap = HeapMaximos.desde_lista(elementos)
        return heap.top_n(n)

    # --- Grafo de conexiones entre obras (TP7) ---
    def _construir_grafo(self):
        """Arma el grafo de conexiones (ver construir_grafo_por_personajes)."""
        self._grafo = construir_grafo_por_personajes(self._obras)

    @property
    def grafo(self):
        return self._grafo

    def obras_conectadas(self, titulo):
        """Obras conectadas con la dada, como lista de (obra, personajes en
        común). Primero las que más personajes comparten."""
        resultado = [
            (self._grafo.obtener_obra(a.destino), a.personajes)
            for a in self._grafo.vecinos(titulo)
        ]
        resultado.sort(key=lambda par: (-len(par[1]), par[0].titulo))
        return resultado

    def conexion_entre(self, titulo_a, titulo_b):
        """Personajes que comparten dos obras, o None si no están conectadas."""
        arista = self._grafo.obtener_arista(titulo_a, titulo_b)
        return list(arista.personajes) if arista else None
