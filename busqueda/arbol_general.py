from collections import deque


class NodoGeneral:
    """Nodo de un árbol general: puede tener cualquier cantidad de hijos.
    Puede ser una categoría (Saga, Tipo) o una hoja que guarda una Obra."""

    def __init__(self, nombre, obra=None):
        self.nombre = nombre
        self.obra = obra          # solo las hojas guardan una Obra
        self.hijos = []
        self.padre = None

    def es_hoja(self):
        return len(self.hijos) == 0


class ArbolGeneral:
    """Árbol general (n-ario) que organiza el catálogo como jerarquía:

        Marvel
        ├── Saga del Infinito
        │   ├── Películas
        │   │   ├── Iron Man
        │   │   └── ...
        │   └── Series
        └── Saga del Multiverso
            └── ...

    A diferencia del BST/AVL (que ordenan por una clave y buscan por
    comparación), acá cada nodo puede tener cualquier cantidad de hijos
    y el árbol representa una relación de "pertenece a", no de orden.
    """

    def __init__(self, nombre_raiz):
        self._raiz = NodoGeneral(nombre_raiz)

    @property
    def raiz(self):
        return self._raiz

    # --- Construcción ---

    def agregar_hijo(self, nodo_padre, nombre, obra=None):
        """Agrega un hijo al nodo dado y lo devuelve."""
        hijo = NodoGeneral(nombre, obra)
        hijo.padre = nodo_padre
        nodo_padre.hijos.append(hijo)
        return hijo

    def obtener_o_crear_hijo(self, nodo_padre, nombre):
        """Devuelve el hijo con ese nombre; si no existe, lo crea.
        Se usa al construir el árbol desde los datos."""
        for hijo in nodo_padre.hijos:
            if hijo.nombre == nombre and hijo.obra is None:
                return hijo
        return self.agregar_hijo(nodo_padre, nombre)

    # --- Búsqueda ---

    def buscar(self, nombre):
        """Busca un nodo por nombre (sin distinguir mayúsculas) con un
        recorrido en profundidad. Devuelve el nodo o None.
        Complejidad: O(n) — en el peor caso visita todos los nodos,
        porque un árbol general no tiene criterio de orden que permita
        descartar ramas."""
        nombre = nombre.strip().lower()
        return self._buscar_recursivo(self._raiz, nombre)

    def _buscar_recursivo(self, nodo, nombre):
        if nodo.nombre.lower() == nombre:
            return nodo
        for hijo in nodo.hijos:
            encontrado = self._buscar_recursivo(hijo, nombre)
            if encontrado:
                return encontrado
        return None

    def camino_a(self, nombre):
        """Devuelve la ruta desde la raíz hasta el nodo (lista de
        nombres), o None si no existe. Ej: ['Marvel', 'Saga del
        Infinito', 'Películas', 'Iron Man']."""
        nodo = self.buscar(nombre)
        if nodo is None:
            return None
        ruta = []
        while nodo is not None:
            ruta.append(nodo.nombre)
            nodo = nodo.padre
        return list(reversed(ruta))

    # --- Recorridos ---

    def recorrido_preorden(self, nodo=None):
        """Raíz primero, después cada hijo (de izquierda a derecha).
        Devuelve lista de (nivel, nodo). Es el recorrido natural para
        mostrar el árbol con sangría, como un índice."""
        resultado = []
        self._preorden(nodo or self._raiz, 0, resultado)
        return resultado

    def _preorden(self, nodo, nivel, resultado):
        resultado.append((nivel, nodo))
        for hijo in nodo.hijos:
            self._preorden(hijo, nivel + 1, resultado)

    def recorrido_postorden(self, nodo=None):
        """Primero todos los hijos, después el nodo. Útil para calcular
        algo de una categoría a partir de lo que tiene adentro (por
        ejemplo, contar obras o sumar duraciones)."""
        resultado = []
        self._postorden(nodo or self._raiz, 0, resultado)
        return resultado

    def _postorden(self, nodo, nivel, resultado):
        for hijo in nodo.hijos:
            self._postorden(hijo, nivel + 1, resultado)
        resultado.append((nivel, nodo))

    def recorrido_por_niveles(self, nodo=None):
        """Recorrido en anchura (BFS): nivel por nivel, usando una cola.
        Devuelve lista de (nivel, nodo)."""
        resultado = []
        cola = deque([(0, nodo or self._raiz)])
        while cola:
            nivel, actual = cola.popleft()
            resultado.append((nivel, actual))
            for hijo in actual.hijos:
                cola.append((nivel + 1, hijo))
        return resultado

    # --- Consultas sobre una categoría ---

    def obras_de(self, nodo):
        """Todas las obras que cuelgan de un nodo (recorre sus hojas)."""
        obras = []
        for _, n in self.recorrido_preorden(nodo):
            if n.obra is not None:
                obras.append(n.obra)
        return obras

    def contar_obras(self, nodo=None):
        return len(self.obras_de(nodo or self._raiz))

    def altura(self, nodo=None):
        nodo = nodo or self._raiz
        if nodo.es_hoja():
            return 1
        return 1 + max(self.altura(h) for h in nodo.hijos)
