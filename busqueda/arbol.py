class NodoArbol:
    def __init__(self, obra):
        self.obra = obra
        self.izquierda = None
        self.derecha = None


class ArbolBusquedaObras:
    """Árbol binario de búsqueda (sin balanceo) que ordena las obras
    alfabéticamente por título, para poder buscarlas más rápido que
    con una lista recorrida de punta a punta.

    Complejidad de la búsqueda:
        Mejor caso (Ω): O(1) — el elemento buscado está en la raíz.
        Caso promedio (Θ): O(log n) — si el árbol queda razonablemente
                            balanceado (dataset cargado en orden variado),
                            cada comparación descarta la mitad del árbol.
        Peor caso (O): O(n) — si los títulos se insertan ya ordenados,
                        el árbol degenera en una lista enlazada (todo
                        hacia un solo lado). Este caso se resuelve recién
                        en TP4 con un árbol AVL balanceado.
    """

    def __init__(self):
        self._raiz = None

    def insertar(self, obra):
        self._raiz = self._insertar_recursivo(self._raiz, obra)

    def _insertar_recursivo(self, nodo, obra):
        if nodo is None:
            return NodoArbol(obra)
        if obra.titulo < nodo.obra.titulo:
            nodo.izquierda = self._insertar_recursivo(nodo.izquierda, obra)
        else:
            nodo.derecha = self._insertar_recursivo(nodo.derecha, obra)
        return nodo

    def buscar(self, titulo):
        return self._buscar_recursivo(self._raiz, titulo)

    def _buscar_recursivo(self, nodo, titulo):
        if nodo is None:
            return None
        if titulo == nodo.obra.titulo:
            return nodo.obra
        if titulo < nodo.obra.titulo:
            return self._buscar_recursivo(nodo.izquierda, titulo)
        return self._buscar_recursivo(nodo.derecha, titulo)
