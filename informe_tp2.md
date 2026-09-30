# TP2 — ¿Qué tan rápido es?

## Operación elegida

**Búsqueda de una obra por título.** Es la operación más usada en
MultiversoGuide: se dispara cada vez que un usuario busca una obra o el
sistema necesita verificar si un título ya existe en el catálogo.

## Estrategias implementadas

### 1. Búsqueda secuencial (`busqueda/secuencial.py`)

Recorre la lista de obras una por una, de principio a fin, comparando el
título en cada paso hasta encontrar coincidencia (o llegar al final).

### 2. Búsqueda en árbol binario de búsqueda (`busqueda/arbol.py`)

Las obras se insertan en un árbol binario de búsqueda (sin balancear,
todavía) ordenado alfabéticamente por título. En cada nodo se decide ir a
la izquierda o a la derecha según si el título buscado es menor o mayor
al del nodo actual, descartando en cada paso una porción del árbol.

## Análisis de complejidad

| Estrategia            | Mejor caso (Ω) | Caso promedio (Θ) | Peor caso (O) |
|------------------------|----------------|--------------------|----------------|
| Búsqueda secuencial    | O(1)           | O(n)               | O(n)           |
| Búsqueda en árbol (BST)| O(1)           | O(log n)           | O(n)*          |

*El peor caso del árbol ocurre si las obras se insertan ya ordenadas por
título: el árbol degenera en una lista (todos los nodos hacia el mismo
lado) y la búsqueda se vuelve tan lenta como la secuencial. Este problema
se resuelve recién en el TP4, balanceando el árbol con un AVL. Para este
experimento insertamos las obras en orden aleatorio para evitar ese caso
degenerado y medir el comportamiento típico (Θ) del árbol.

## Script de experimentos

`experimentos/tp2_benchmark.py` genera datasets de obras de prueba con
títulos aleatorios únicos, arma ambas estructuras, y mide el tiempo
promedio de 200 búsquedas del mismo título (siempre uno "lejano" al
inicio, para no favorecer a la secuencial) con tamaños de entrada de
100, 1.000 y 10.000 obras.

Se ejecuta con:
```bash
python3 experimentos/tp2_benchmark.py
```

## Tabla de resultados (medición real)

| N elementos | Búsqueda secuencial | Búsqueda en árbol |
|-------------|----------------------|---------------------|
| 100         | 0.0031 ms            | 0.0008 ms           |
| 1.000       | 0.0254 ms            | 0.0011 ms           |
| 10.000      | 0.3204 ms            | 0.0014 ms           |

*(tiempos promedio por búsqueda, en milisegundos, medidos con `time.perf_counter`)*

## Conclusión técnica

Los tiempos medidos confirman lo que predice la teoría: la búsqueda
secuencial crece **linealmente** con la cantidad de obras — al pasar de
100 a 10.000 elementos (100 veces más datos), el tiempo se multiplica
también por un factor cercano a 100 (de 0.003 ms a 0.32 ms). En cambio,
la búsqueda en árbol crece de forma **logarítmica**: ese mismo salto de
100x en los datos apenas duplica el tiempo de búsqueda (de 0.0008 ms a
0.0014 ms), porque cada comparación descarta la mitad del árbol restante.

Para el dominio de MultiversoGuide, donde el catálogo de obras puede
crecer con el tiempo (más películas, series y cómics agregados), **conviene
usar la búsqueda en árbol** para las consultas frecuentes por título: la
diferencia es marginal con pocos datos, pero se vuelve significativa a
medida que el catálogo crece. La búsqueda secuencial solo tendría sentido
si el dataset fuera muy chico y estable, o si no se puede garantizar un
criterio de orden para construir el árbol.
