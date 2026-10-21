class NodoAVL:
    def __init__(self, obra):
        self.obra = obra
        self.izquierda = None
        self.derecha = None
        self.altura = 1  # altura de un nodo hoja recién creado


class ArbolAVL:
    """Árbol binario de búsqueda AUTOBALANCEADO (AVL), ordenado por
    título, igual que el BST del TP3 — pero con la diferencia clave de
    que después de cada inserción se verifica el balance de cada nodo
    y, si hace falta, se aplican rotaciones para corregirlo.

    Esto garantiza que la altura del árbol se mantenga siempre en
    O(log n), sin importar en qué orden se inserten los datos — a
    diferencia del BST común del TP3, que podía degenerar en una lista
    enlazada (O(n)) si los datos entraban ya ordenados.

    Complejidad de la búsqueda:
        Mejor caso (Ω): O(1) — el elemento está en la raíz.
        Caso promedio (Θ): O(log n).
        Peor caso (O): O(log n) — gracias al balanceo, el peor caso deja
                        de ser O(n); esa es la mejora central del AVL.
    """

    def __init__(self):
        self._raiz = None

    # --- Utilidades de altura y balance ---

    def _altura(self, nodo):
        return nodo.altura if nodo else 0

    def _factor_balance(self, nodo):
        if nodo is None:
            return 0
        return self._altura(nodo.izquierda) - self._altura(nodo.derecha)

    def _actualizar_altura(self, nodo):
        nodo.altura = 1 + max(self._altura(nodo.izquierda), self._altura(nodo.derecha))

    # --- Rotaciones ---

    def _rotacion_derecha(self, y):
        """Caso Izquierda-Izquierda (LL): el subárbol izquierdo pesa
        demasiado, se 'gira' el árbol hacia la derecha."""
        x = y.izquierda
        t2 = x.derecha

        x.derecha = y
        y.izquierda = t2

        self._actualizar_altura(y)
        self._actualizar_altura(x)
        return x

    def _rotacion_izquierda(self, x):
        """Caso Derecha-Derecha (RR): el subárbol derecho pesa
        demasiado, se 'gira' el árbol hacia la izquierda."""
        y = x.derecha
        t2 = y.izquierda

        y.izquierda = x
        x.derecha = t2

        self._actualizar_altura(x)
        self._actualizar_altura(y)
        return y

    # --- Inserción balanceada ---

    def insertar(self, obra):
        self._raiz = self._insertar_recursivo(self._raiz, obra)

    def _insertar_recursivo(self, nodo, obra):
        # 1. Inserción normal de BST
        if nodo is None:
            return NodoAVL(obra)

        if obra.titulo < nodo.obra.titulo:
            nodo.izquierda = self._insertar_recursivo(nodo.izquierda, obra)
        elif obra.titulo > nodo.obra.titulo:
            nodo.derecha = self._insertar_recursivo(nodo.derecha, obra)
        else:
            return nodo  # título duplicado, no se inserta de nuevo

        # 2. Actualizar altura del nodo actual
        self._actualizar_altura(nodo)

        # 3. Calcular el factor de balance para ver si hace falta rotar
        balance = self._factor_balance(nodo)

        # Caso Izquierda-Izquierda
        if balance > 1 and obra.titulo < nodo.izquierda.obra.titulo:
            return self._rotacion_derecha(nodo)

        # Caso Derecha-Derecha
        if balance < -1 and obra.titulo > nodo.derecha.obra.titulo:
            return self._rotacion_izquierda(nodo)

        # Caso Izquierda-Derecha
        if balance > 1 and obra.titulo > nodo.izquierda.obra.titulo:
            nodo.izquierda = self._rotacion_izquierda(nodo.izquierda)
            return self._rotacion_derecha(nodo)

        # Caso Derecha-Izquierda
        if balance < -1 and obra.titulo < nodo.derecha.obra.titulo:
            nodo.derecha = self._rotacion_derecha(nodo.derecha)
            return self._rotacion_izquierda(nodo)

        # Ya estaba balanceado, no hace falta rotar
        return nodo

    # --- Búsqueda (igual que en el BST del TP3) ---

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

    # --- Recorridos (igual que en el BST del TP3) ---

    def recorrido_inorder(self):
        resultado = []
        self._inorder_recursivo(self._raiz, resultado)
        return resultado

    def _inorder_recursivo(self, nodo, resultado):
        if nodo is not None:
            self._inorder_recursivo(nodo.izquierda, resultado)
            resultado.append(nodo.obra)
            self._inorder_recursivo(nodo.derecha, resultado)

    def altura_total(self):
        """Altura del árbol completo — útil para comparar el balance
        contra un BST común armado con los mismos datos."""
        return self._altura(self._raiz)

    def esta_vacio(self):
        return self._raiz is None
