class HeapMaximos:
    """Heap binaria de máximos implementada a mano sobre una lista
    (sin usar el módulo heapq, como pide la cátedra).

    Cada elemento es una tupla (prioridad, obra). El que tiene MAYOR
    prioridad está siempre en la raíz (posición 0). Si dos obras empatan
    en prioridad, sale primero la de título alfabéticamente menor, para
    que el resultado sea siempre el mismo.

    La lista representa un árbol binario completo:
        hijo izquierdo de i  ->  2*i + 1
        hijo derecho de i    ->  2*i + 2
        padre de i           ->  (i - 1) // 2

    Complejidad:
        insertar      O(log n)
        ver_max       O(1)
        extraer_max   O(log n)
        construir     O(n)       (desde_lista, con heapify)
        top_n(k)      O(k log n)
    """

    def __init__(self):
        self._datos = []
        self.comparaciones = 0  # contador, solo para los experimentos

    # --- Construcción ---

    @classmethod
    def desde_lista(cls, elementos):
        """Arma la heap en O(n) a partir de una lista de (prioridad, obra),
        hundiendo cada nodo interno desde el último hasta la raíz. Es más
        rápido que insertar de a uno (que sería O(n log n))."""
        heap = cls()
        heap._datos = list(elementos)
        for i in range(len(heap._datos) // 2 - 1, -1, -1):
            heap._hundir(i)
        return heap

    # --- Comparación ---

    def _va_antes(self, a, b):
        """True si el elemento a debe estar más cerca de la raíz que b."""
        self.comparaciones += 1
        if a[0] != b[0]:
            return a[0] > b[0]
        return a[1].titulo < b[1].titulo

    # --- Movimientos internos ---

    def _subir(self, i):
        while i > 0:
            padre = (i - 1) // 2
            if self._va_antes(self._datos[i], self._datos[padre]):
                self._datos[i], self._datos[padre] = self._datos[padre], self._datos[i]
                i = padre
            else:
                break

    def _hundir(self, i):
        n = len(self._datos)
        while True:
            izq = 2 * i + 1
            der = 2 * i + 2
            mayor = i
            if izq < n and self._va_antes(self._datos[izq], self._datos[mayor]):
                mayor = izq
            if der < n and self._va_antes(self._datos[der], self._datos[mayor]):
                mayor = der
            if mayor == i:
                break
            self._datos[i], self._datos[mayor] = self._datos[mayor], self._datos[i]
            i = mayor

    # --- Operaciones públicas ---

    def insertar(self, prioridad, obra):
        self._datos.append((prioridad, obra))
        self._subir(len(self._datos) - 1)

    def ver_max(self):
        if not self._datos:
            return None
        return self._datos[0]

    def extraer_max(self):
        if not self._datos:
            return None
        raiz = self._datos[0]
        ultimo = self._datos.pop()
        if self._datos:
            self._datos[0] = ultimo
            self._hundir(0)
        return raiz

    def top_n(self, k):
        """Devuelve los k elementos de mayor prioridad (de mayor a menor)
        y deja la heap como estaba: extrae los k mejores y los vuelve a
        insertar. Cuesta O(k log n), sin depender de recorrer los n datos."""
        extraidos = []
        for _ in range(min(k, len(self._datos))):
            extraidos.append(self.extraer_max())
        for prioridad, obra in extraidos:
            self.insertar(prioridad, obra)
        return extraidos

    def __len__(self):
        return len(self._datos)

    def esta_vacia(self):
        return len(self._datos) == 0
