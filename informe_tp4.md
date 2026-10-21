# TP4 — El árbol también puede enfermarse

## Caso de desbalance generado

Se insertaron títulos **ya ordenados alfabéticamente**
(`Obra000`, `Obra001`, `Obra002`, ...) en ambas estructuras. Es el peor
caso posible para un BST común: como cada título nuevo es siempre mayor
al anterior, el árbol inserta todo hacia la derecha y termina pareciendo
una lista enlazada, no un árbol.

## Implementación del AVL (`busqueda/avl.py`)

Se construyó `ArbolAVL` como una variante balanceada del BST del TP3,
con la misma interfaz (`insertar`, `buscar`, `recorrido_inorder`), pero
agregando:

- **Altura por nodo**: cada nodo guarda su propia altura, actualizada
  después de cada inserción.
- **Factor de balance**: `altura(izquierda) - altura(derecha)`. Si da
  más de 1 o menos de -1, el nodo está desbalanceado.
- **4 rotaciones**, aplicadas automáticamente después de insertar:
  - **LL** (Izquierda-Izquierda): rotación simple a la derecha.
  - **RR** (Derecha-Derecha): rotación simple a la izquierda.
  - **LR** (Izquierda-Derecha): rotación izquierda seguida de derecha.
  - **RL** (Derecha-Izquierda): rotación derecha seguida de izquierda.

## Pruebas (`tests/test_avl.py`)

6 pruebas, todas corridas y verificadas:
1-4. Cada uno de los 4 casos de rotación (LL, RR, LR, RL) produce el
   árbol esperado.
5. Insertar 200 títulos ya ordenados mantiene el árbol balanceado
   (factor de balance de todos los nodos entre -1 y 1), con una altura
   cercana al ideal teórico `log2(n)`.
6. La búsqueda sigue encontrando todo correctamente después de las
   rotaciones (no se "pierden" nodos en el proceso).

## Comparación BST común vs. AVL (medición real)

Script: `experimentos/tp4_benchmark.py`. Se insertaron títulos ya
ordenados en ambas estructuras y se midió la **altura resultante** y el
**tiempo de búsqueda** del último título insertado (peor caso para el
BST común).

| N elementos | Altura BST | Altura AVL | Tiempo BST (ms) | Tiempo AVL (ms) |
|-------------|------------|------------|-------------------|-------------------|
| 100         | 100        | 7          | 0.0081            | 0.0007            |
| 1.000       | 1.000      | 10         | 0.1409            | 0.0008            |
| 10.000      | 10.000     | 14         | 1.7143            | 0.0015            |

Como referencia, la altura ideal (`log2 n`) sería ≈6.6, ≈10.0 y ≈13.3
para esos tamaños — el AVL se mantiene prácticamente pegado a ese ideal
en los tres casos.

**Dato extra, no planeado pero revelador:** con este dataset ordenado,
el BST común de Python literalmente **no pudo correr con los parámetros
por defecto** — la inserción recursiva superó el límite de recursión de
Python (1000 llamadas anidadas) al llegar a los 1.000 elementos, porque
la altura del árbol (1.000) se volvió igual a la cantidad de datos. Hubo
que subir manualmente ese límite (`sys.setrecursionlimit`) solo para
poder medirlo. El AVL nunca tuvo ese problema, porque su altura jamás
pasa de `~1.44 × log2(n)` sin importar el orden de inserción.

## Por qué importa el balance (relación con O(log n) vs O(n))

La altura de un árbol determina directamente cuántas comparaciones hacen
falta para encontrar un elemento: cada paso de la búsqueda baja un nivel.
- Un árbol **balanceado** tiene altura `O(log n)` → cada búsqueda
  descarta aproximadamente la mitad de los nodos restantes en cada paso.
- Un árbol **degenerado** (como el BST con datos ordenados) tiene altura
  `O(n)` → se convierte, en la práctica, en la misma búsqueda secuencial
  del TP2, con el costo extra de la recursión.

El AVL resuelve esto pagando un costo pequeño en cada inserción (calcular
alturas y, ocasionalmente, rotar), para **garantizar** que la altura
nunca se dispare, sin importar en qué orden lleguen los datos. Para
MultiversoGuide, donde no se puede controlar el orden en que se cargan o
agregan nuevas obras al catálogo, esto es una garantía valiosa: sin AVL,
alcanzaría con que alguien cargue el dataset ya ordenado alfabéticamente
para que el sistema se vuelva lento silenciosamente.

## Conclusión técnica

El experimento confirma que el "balance" no es un detalle de
implementación menor: es lo que separa a un árbol que realmente funciona
como árbol (`O(log n)`) de uno que, en el peor caso, degenera a una
lista (`O(n)`) sin que el código "avise" que algo salió mal — simplemente
se vuelve más lento a medida que crecen los datos, hasta el punto de
romper por límite de recursión en este experimento. A partir de este TP,
**el AVL (`busqueda/avl.py`) es la estructura recomendada** para la
búsqueda y el ordenamiento por título en MultiversoGuide; el BST simple
del TP3 queda documentado como referencia histórica del problema que el
AVL vino a resolver.
