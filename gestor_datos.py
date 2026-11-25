import json
import os
import re
import unicodedata
from models.obra import Obra
from busqueda.avl import ArbolAVL
from busqueda.arbol_general import ArbolGeneral
from busqueda.heap import HeapMaximos
from busqueda.grafo import Grafo, construir_grafo_por_personajes
from busqueda import recorridos
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


def normalizar_texto(texto):
    """Pasa un texto a minúsculas, sin tildes y con todo lo que no sea letra
    o número reemplazado por un espacio. Sirve para comparar lo que escribe
    el usuario con los títulos sin que importen las mayúsculas, las tildes
    ni la puntuación (guiones, dos puntos, asteriscos, etc.)."""
    sin_tildes = "".join(
        c for c in unicodedata.normalize("NFD", texto.lower())
        if unicodedata.category(c) != "Mn"
    )
    return re.sub(r"[^a-z0-9]+", " ", sin_tildes).strip()


def interpretar_anios(texto):
    """Interpreta un año ('2021') o un rango de años ('2018-2022' o '2018 a 2022').
    Devuelve (desde, hasta) o None si el texto no es un año ni un rango."""
    m = re.fullmatch(r"\s*(\d{4})\s*(?:(?:-|–|a)\s*(\d{4}))?\s*", texto)
    if not m:
        return None
    desde = int(m.group(1))
    hasta = int(m.group(2)) if m.group(2) else desde
    return (desde, hasta) if desde <= hasta else (hasta, desde)


class GestorDatos:
    """Carga las obras desde un archivo JSON y ofrece las operaciones
    principales sobre esos datos: buscar, listar y filtrar.

    Desde el TP3, además de la lista plana de obras, se arma un árbol
    de búsqueda (ordenado por título) que se usa para la búsqueda exacta
    y para listar ordenado. Es un árbol AVL (TP4): tiene la misma
    interfaz que el árbol binario del TP3 (insertar, buscar,
    recorrido_inorder), pero se equilibra solo y no se degenera aunque
    los títulos se carguen ya ordenados."""

    def __init__(self, ruta_json):
        self._ruta_json = ruta_json
        self._obras = []
        self._arbol = ArbolAVL()
        self._jerarquia = ArbolGeneral("Marvel")
        self._grafo = Grafo()
        self._rutas = {}
        self._originales = {}   # titulo en espanol -> titulo original (solo para buscar)
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
                descripcion=item.get("descripcion",""),
            )
            for item in datos
        ]

        self._originales = {
            item["titulo"]: item["titulo_original"]
            for item in datos if item.get("titulo_original")
        }

        for obra in self._obras:
            self._arbol.insertar(obra)

        self._construir_jerarquia()
        self._construir_grafo()
        self._cargar_rutas()

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
    def _nombres_de(self, obra):
        """Títulos con los que se puede buscar una obra: el título en español
        y, si lo tiene, el título original (por ejemplo, en inglés)."""
        original = self._originales.get(obra.titulo)
        return [obra.titulo, original] if original else [obra.titulo]

    def buscar_por_titulo(self, texto):
        """Busca obras cuyo título coincida con el texto, aunque esté
        incompleto. Ignora mayúsculas, tildes y puntuación, acepta las
        palabras en cualquier orden o pegadas ('avengers endgame',
        'spiderman', 'x men') y también entiende el título original
        ('no way home' encuentra 'Spider-Man: Sin camino a casa')."""
        consulta = normalizar_texto(texto)
        palabras = consulta.split()
        pegada = consulta.replace(" ", "")
        resultado = []
        for obra in self._obras:
            for nombre in self._nombres_de(obra):
                titulo = normalizar_texto(nombre)
                if all(p in titulo for p in palabras) or pegada in titulo.replace(" ", ""):
                    resultado.append(obra)
                    break
        return resultado

    def titulo_exacto(self, texto):
        """Devuelve la obra cuyo título es el texto escrito, ignorando
        mayúsculas, tildes, signos y espacios ('avengers endgame' y
        'Avengers: Endgame' son el mismo título). También vale el título
        original ('ant-man' encuentra 'Ant-Man: El hombre hormiga').
        Devuelve None si ninguna coincide exactamente."""
        buscado = normalizar_texto(texto).replace(" ", "")
        if not buscado:
            return None
        for obra in self._obras:
            for nombre in self._nombres_de(obra):
                if normalizar_texto(nombre).replace(" ", "") == buscado:
                    return obra
        return None

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
    def filtrar(self, tipo=None, fase=None, personaje=None, anio_desde=None, anio_hasta=None):
        resultado = self._obras

        if tipo:
            # 'película', 'peliculas' y 'Pelicula' son lo mismo (sin tildes ni plural)
            buscado = normalizar_texto(tipo)
            if buscado.endswith("s"):
                buscado = buscado[:-1]
            resultado = [o for o in resultado if normalizar_texto(o.tipo) == buscado]
        if fase:
            buscada = normalizar_texto(fase)
            resultado = [
                o for o in resultado
                if buscada in normalizar_texto(o.fase) or buscada in normalizar_texto(saga_de(o.fase))
            ]
        if personaje:
            buscado = normalizar_texto(personaje)
            resultado = [
                o for o in resultado
                if any(buscado in normalizar_texto(p) for p in o.personajes)
            ]
        if anio_desde is not None:
            resultado = [o for o in resultado if o.anio >= anio_desde]
        if anio_hasta is not None:
            resultado = [o for o in resultado if o.anio <= anio_hasta]

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
            (calcular_prioridad(obra, perfil, self._relevancia(obra, perfil)), obra)
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

    # --- Recorridos del grafo (TP8, BFS y DFS) ---
    def camino_mas_corto(self, titulo_a, titulo_b):
        """Cadena con menos obras entre dos obras (BFS), como lista de
        Obra desde la primera hasta la última; None si no hay camino."""
        titulos = recorridos.camino_mas_corto(self._grafo, titulo_a, titulo_b)
        if titulos is None:
            return None
        return [self._grafo.obtener_obra(t) for t in titulos]

    def obras_por_distancia(self, titulo):
        """Obras alcanzables desde una obra, con su distancia en conexiones
        (BFS), de las más cercanas a las más lejanas. No incluye al origen."""
        return [
            (self._grafo.obtener_obra(t), distancia)
            for t, distancia in recorridos.bfs(self._grafo, titulo)
            if distancia > 0
        ]

    def explorar_en_profundidad(self, titulo):
        """Recorrido en profundidad (DFS) desde una obra, como lista de
        (Obra, profundidad). Incluye al origen con profundidad 0."""
        return [
            (self._grafo.obtener_obra(t), profundidad)
            for t, profundidad in recorridos.dfs(self._grafo, titulo)
        ]

    def grupos_conectados(self):
        """Grupos de obras conectadas entre sí (DFS), de mayor a menor."""
        grupos = [
            [self._grafo.obtener_obra(t) for t in grupo]
            for grupo in recorridos.componentes_conexas(self._grafo)
        ]
        grupos.sort(key=len, reverse=True)
        return grupos

    # --- Rutas recomendadas por perfil (data/rutas.json) ---
    def _cargar_rutas(self):
        """Carga las rutas recomendadas (una por perfil: casual y fan), si
        existe data/rutas.json. Cada ruta es una lista de secciones con
        títulos de obras, en el orden en que conviene verlas. Se valida
        que todos los títulos existan en obras.json."""
        archivo_rutas = os.path.join(os.path.dirname(self._ruta_json), "rutas.json")
        if not os.path.exists(archivo_rutas):
            return
        with open(archivo_rutas, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        por_titulo = {obra.titulo: obra for obra in self._obras}

        def obra_de(titulo):
            if titulo not in por_titulo:
                raise ValueError(f"rutas.json menciona una obra que no está en obras.json: {titulo}")
            return por_titulo[titulo]

        for perfil, ruta in datos.items():
            secciones = [
                (seccion["titulo"], [obra_de(t) for t in seccion["obras"]])
                for seccion in ruta["secciones"]
            ]
            obras_de_la_ruta = [obra for _, obras in secciones for obra in obras]
            self._rutas[perfil] = {
                "nombre": ruta["nombre"],
                "objetivo": ruta.get("objetivo", ""),
                "cierre": ruta.get("cierre", ""),
                "secciones": secciones,
                "obras": obras_de_la_ruta,
                "titulos": {obra.titulo for obra in obras_de_la_ruta},
                "prioridades": {obra_de(t).titulo for t in ruta.get("prioridades", [])},
                "opcionales": {obra_de(t).titulo for t in ruta.get("opcionales", [])},
                "puntaje_ruta": ruta.get("puntaje_ruta", 0),
                "puntaje_prioridad": ruta.get("puntaje_prioridad", 0),
            }

    def ruta(self, perfil):
        """Ruta recomendada para un perfil ('casual' o 'fan'), o None si no hay."""
        return self._rutas.get(perfil)

    def _relevancia(self, obra, perfil):
        """Qué tan importante es una obra en la ruta del perfil (0 a 10).
        Las prioridades absolutas valen lo máximo; el resto de la ruta
        vale lo que indique el archivo; fuera de la ruta, 0."""
        ruta = self._rutas.get(perfil)
        if ruta is None:
            return 0.0
        if obra.titulo in ruta["prioridades"]:
            return float(ruta["puntaje_prioridad"])
        if obra.titulo in ruta["titulos"]:
            return float(ruta["puntaje_ruta"])
        return 0.0

