class Arista:
    """Un arco del grafo: desde una obra hacia otra.

    destino    -> título de la obra a la que se llega.
    peso       -> costo de llegar a ese destino (en MultiversoGuide, los
                  minutos que dura el destino).
    personajes -> personajes que comparten las dos obras (el motivo de
                  la conexión).
    """

    __slots__ = ("destino", "peso", "personajes")

    def __init__(self, destino, peso=1, personajes=None):
        self.destino = destino
        self.peso = peso
        self.personajes = list(personajes) if personajes else []

    def __repr__(self):
        return f"Arista(-> {self.destino}, peso={self.peso})"


class Grafo:
    """Grafo DIRIGIDO y PESADO, representado con LISTA DE ADYACENCIA.

    Modelo para MultiversoGuide:
        Vértice: una obra (película, serie o cómic), identificada por
                 su título.
        Arista:  hay conexión entre dos obras si comparten al menos un
                 personaje.
        Peso:    el costo de "ir" a una obra = lo que dura verla.
        Dirección: compartir un personaje es simétrico, así que cada
                 conexión se guarda como DOS arcos (A->B y B->A). Pero el
                 peso es distinto en cada sentido (ir hacia B cuesta lo
                 que dura B; ir hacia A cuesta lo que dura A). Por eso el
                 grafo es dirigido.

    Representación: un diccionario {título: [Arista, ...]}.
        Espacio:                 O(V + E)
        Recorrer los vecinos:    O(grado del vértice)
        ¿Existe la arista u->v?: O(grado de u)
    """

    def __init__(self):
        self._obras = {}        # título -> Obra
        self._adyacencia = {}   # título -> lista de Arista

    # --- Vértices ---

    def agregar_vertice(self, obra):
        if obra.titulo not in self._obras:
            self._obras[obra.titulo] = obra
            self._adyacencia[obra.titulo] = []

    def tiene_vertice(self, titulo):
        return titulo in self._obras

    def obtener_obra(self, titulo):
        return self._obras.get(titulo)

    def vertices(self):
        return list(self._obras.values())

    # --- Aristas ---

    def agregar_arista(self, origen, destino, peso=1, personajes=None):
        """Agrega el arco origen -> destino. Si ya existía, lo reemplaza."""
        if origen not in self._obras or destino not in self._obras:
            raise ValueError("Los dos vértices deben existir antes de conectarlos.")
        if origen == destino:
            raise ValueError("Una obra no se conecta consigo misma.")
        self._adyacencia[origen] = [
            a for a in self._adyacencia[origen] if a.destino != destino
        ]
        self._adyacencia[origen].append(Arista(destino, peso, personajes))

    def existe_arista(self, origen, destino):
        return self.obtener_arista(origen, destino) is not None

    def obtener_arista(self, origen, destino):
        for arista in self._adyacencia.get(origen, []):
            if arista.destino == destino:
                return arista
        return None

    def vecinos(self, titulo):
        """Aristas que salen de una obra (lista vacía si no existe)."""
        return list(self._adyacencia.get(titulo, []))

    # --- Consultas sobre la estructura ---

    def grado(self, titulo):
        return len(self._adyacencia.get(titulo, []))

    def aislados(self):
        """Obras sin ninguna conexión."""
        return [obra for titulo, obra in self._obras.items() if self.grado(titulo) == 0]

    def cantidad_vertices(self):
        return len(self._obras)

    def cantidad_aristas(self):
        """Cantidad de ARCOS dirigidos. Como cada conexión entre obras
        se guarda en ambos sentidos, las conexiones reales son la mitad."""
        return sum(len(lista) for lista in self._adyacencia.values())

    def densidad(self):
        """Proporción de arcos que existen sobre los posibles (V*(V-1)).
        Va de 0 (sin conexiones) a 1 (todas conectadas con todas)."""
        v = self.cantidad_vertices()
        if v < 2:
            return 0.0
        return self.cantidad_aristas() / (v * (v - 1))


def construir_grafo_por_personajes(obras):
    """Arma el grafo de conexiones a partir de una lista de obras: un
    vértice por obra y una conexión entre dos obras que comparten al
    menos un personaje.

    Para no comparar todas las obras contra todas (O(n^2)), primero se
    arma un índice personaje -> obras donde aparece, y solo se conectan
    las obras que figuran juntas en esa lista. Cada conexión se guarda
    como dos arcos; ir hacia una obra cuesta lo que dura esa obra."""
    grafo = Grafo()
    for obra in obras:
        grafo.agregar_vertice(obra)

    por_personaje = {}
    for obra in obras:
        for personaje in obra.personajes:
            por_personaje.setdefault(personaje, []).append(obra)

    compartidos = {}  # (título A, título B) -> personajes en común
    for personaje, obras_del_personaje in por_personaje.items():
        for i in range(len(obras_del_personaje)):
            for j in range(i + 1, len(obras_del_personaje)):
                clave = (obras_del_personaje[i].titulo, obras_del_personaje[j].titulo)
                compartidos.setdefault(clave, []).append(personaje)

    for (titulo_a, titulo_b), personajes in compartidos.items():
        personajes.sort()
        obra_a = grafo.obtener_obra(titulo_a)
        obra_b = grafo.obtener_obra(titulo_b)
        grafo.agregar_arista(titulo_a, titulo_b, obra_b.duracion_min, personajes)
        grafo.agregar_arista(titulo_b, titulo_a, obra_a.duracion_min, personajes)

    return grafo

