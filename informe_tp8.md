# TP8 — Explorá la red

Se implementaron los dos recorridos clásicos de grafos, BFS y DFS, sobre
el grafo de conexiones entre obras del TP7 (`busqueda/recorridos.py`), y
se usaron para resolver dos preguntas reales del sistema.

## Qué hace cada algoritmo

Los dos visitan cada obra alcanzable una sola vez y recorren cada
conexión una sola vez. La diferencia es **el orden** en que visitan, que
depende de la estructura que usan para guardar lo pendiente.

### BFS (búsqueda en anchura) — usa una cola

Visita primero todas las obras a 1 paso del origen, después las que
están a 2 pasos, después a 3, y así. Como siempre agota un nivel antes de
pasar al siguiente, la primera vez que llega a una obra lo hace por el
camino con **menos conexiones**.

Desde *Iron Man*, con los datos reales:

```
A 0 pasos:  Iron Man
A 1 paso:   Avengers: Infinity War, Avengers: Endgame
A 2 pasos:  Doctor Strange en el Multiverso de la Locura, Spider-Man: No Way Home
```

### DFS (búsqueda en profundidad) — usa una pila

Elige una conexión y se mete lo más adentro posible; cuando llega a una
obra sin conexiones nuevas, **vuelve para atrás** hasta la última que
todavía tenía alternativas y prueba por ahí. Explora a fondo, pero el
camino por el que llega a cada obra es el que le tocó, no el más corto.

Desde *Avengers: Infinity War* (cada sangría es un paso más adentro):

```
Avengers: Infinity War
    └── Iron Man
        └── Avengers: Endgame
    └── Doctor Strange en el Multiverso de la Locura
        └── Spider-Man: No Way Home
```

Fijate en *Avengers: Endgame*: está conectada **directamente** con
*Infinity War* (distancia 1), pero el DFS llegó a ella pasando por
*Iron Man* (profundidad 2). Es la diferencia central entre los dos,
visible con datos reales.

## Implementación (`busqueda/recorridos.py`)

| Función | Qué hace | Algoritmo |
|---|---|---|
| `bfs(grafo, origen)` | Obras alcanzables con su distancia, de cerca a lejos | BFS con cola |
| `camino_mas_corto(grafo, origen, destino)` | Cadena con menos obras entre dos obras | BFS con punteros al padre; corta al encontrar el destino |
| `dfs(grafo, origen)` | Obras alcanzables con su profundidad, en orden de exploración | DFS con pila |
| `componentes_conexas(grafo)` | Grupos de obras conectadas entre sí | DFS repetido desde cada obra no visitada |

**El DFS es iterativo (con pila explícita), no recursivo.** En el TP4
vimos que Python tiene un límite de recursión de 1.000 llamadas y que un
árbol degenerado lo superaba. Un catálogo con una cadena larga de obras
conectadas tendría el mismo problema con un DFS recursivo. La versión
iterativa visita en el mismo orden que la recursiva, y hay una prueba con
una cadena de 3.000 obras que lo comprueba.

## Casos de uso reales

### Caso 1 (BFS): "¿Cuál es el camino más corto para llegar a esta obra?"

Es la funcionalidad "camino mínimo entre dos obras" prometida desde el
TP0. El usuario indica una obra que **ya vio** y una que **quiere ver**, y
el sistema devuelve la cadena con menos obras, explicando por qué se
conecta cada paso:

```
Camino con menos obras de 'Iron Man' a 'Spider-Man: No Way Home':
  0. Iron Man  (donde empezás)
  1. Avengers: Infinity War  (se conecta con la anterior por: Tony Stark)
  2. Spider-Man: No Way Home  (se conecta con la anterior por: Doctor Strange)

Te faltaría ver 2 obra(s): 4 h 57 min en total.
```

Se usa BFS porque lo que se busca es el camino con menos conexiones, y
BFS lo garantiza. Si no hay camino (por ejemplo, entre *Iron Man* y
*Loki*), el sistema lo informa y explica que están en grupos distintos.
También está disponible la consulta "obras relacionadas por cercanía"
(menú [f]), que muestra el resultado de BFS agrupado por distancia.

### Caso 2 (DFS): "Explorar todo el lore relacionado con una obra"

Es la consulta "explorar todo el lore relacionado con X en profundidad"
del TP0. El usuario elige una obra y el sistema sigue el hilo de
conexiones lo más lejos posible antes de volver a probar otro camino (el
ejemplo de arriba, desde *Infinity War*). Se usa DFS porque lo que
interesa es recorrer toda la red relacionada siguiendo cadenas de
conexiones, no la distancia a cada obra.

### Extra (DFS): grupos de obras conectadas

`componentes_conexas` usa DFS para detectar los "grupos" del catálogo.
Con los datos actuales encuentra 3: *Iron Man / Infinity War / Endgame /
Doctor Strange en el Multiverso de la Locura / No Way Home* (5 obras),
*Loki / Deadpool & Wolverine* (2) y *Secret Invasion* (1, sola). Entre
grupos distintos no existe ningún camino. Sirve también para detectar
qué obras habría que conectar mejor al ampliar el catálogo.

## Análisis de complejidad

V = cantidad de obras, E = cantidad de conexiones (arcos), con el grafo
guardado como lista de adyacencia (TP7).

| | BFS | DFS |
|---|---|---|
| **Tiempo** | O(V + E) | O(V + E) |
| **Espacio** | O(V) | O(V) |
| Estructura auxiliar | cola | pila |
| Qué ocupa el espacio | la cola puede llegar a tener casi todas las obras (grafo muy ancho) | la pila puede llegar a tener todas las obras (cadena larga) |
| Garantiza el camino más corto | **Sí** | **No** |

**Por qué O(V + E):** cada obra entra una sola vez a la cola o a la pila
(se marca como visitada al encolarla o apilarla) y cada conexión se mira
una sola vez al recorrer los vecinos de su obra de origen.
`camino_mas_corto` tiene el mismo costo en el peor caso, pero corta apenas
encuentra el destino.

**Relación con el TP7:** este costo depende de haber elegido lista de
adyacencia. Con una matriz de adyacencia, para recorrer los vecinos de
una obra habría que revisar una fila entera de V celdas, y el recorrido
completo pasaría a costar O(V²).

## Diferencias y cuándo conviene cada uno

| | BFS | DFS |
|---|---|---|
| Orden de visita | por niveles de distancia | lo más profundo posible, después vuelve |
| Camino más corto (en conexiones) | siempre | no, puede ser larguísimo |
| Conviene para | "lo más cercano", "camino con menos pasos", "obras a 1 o 2 pasos" | "explorar todo lo relacionado", detectar grupos aislados, seguir cadenas |
| Uso en MultiversoGuide | camino más corto, obras por cercanía | exploración del lore, grupos conectados |

## Experimentos (`experimentos/tp8_benchmark.py`)

Catálogos sintéticos (cada obra con 3 personajes al azar), con el mismo
generador del TP7. No describen el MCU real; sirven para ver cómo se
comportan los algoritmos al crecer el catálogo.

### Experimento 1 — tiempo de un recorrido completo

| Obras | Arcos | BFS | DFS | BFS sin GC | DFS sin GC |
|---|---|---|---|---|---|
| 1.000 | 8.878 | 0,59 ms | 0,91 ms | 0,59 ms | 0,65 ms |
| 5.000 | 44.344 | 4,88 ms | 13,75 ms | 4,71 ms | 6,09 ms |
| 20.000 | 180.168 | 28,35 ms | 95,87 ms | 29,68 ms | 38,03 ms |

Dos cosas para leer con cuidado:

- **El DFS "normal" tarda bastante más que el BFS, pero no por el
  algoritmo.** El DFS mantiene miles de objetos vivos en la pila y el
  recolector de basura de Python se pasa revisándolos. Al apagarlo
  (columnas "sin GC"), a 20.000 obras el DFS baja de 96 ms a 38 ms y queda
  del orden del BFS (30 ms), que es lo que predice la teoría (misma
  complejidad). Esa explicación la comprobé midiendo con y sin recolector.
- **El tiempo crece algo más rápido que la cantidad de datos** (de 1.000
  a 20.000 obras hay unas 20 veces más datos y el tiempo se multiplica por
  unas 50). El O(V + E) cuenta operaciones, no segundos: a ese tamaño el
  grafo seguramente ya no entra en la memoria caché del procesador y cada
  acceso cuesta más. Es una hipótesis que no medí, así que no la presento
  como un hecho.

### Experimento 2 — qué tan largo es el camino que encuentra cada uno

300 pares de obras al azar dentro de un catálogo de 2.000:

| | Promedio de pasos | Máximo |
|---|---|---|
| Camino del BFS | 4,1 | 6 |
| Camino del DFS | 933,9 | 1.709 |

El camino del DFS fue más largo que el mínimo en **297 de 300 pares**.
Con el DFS, para llegar de una obra a otra habría que "ver" en promedio
casi la mitad del catálogo; con el BFS, unas 4 obras. Por eso el DFS no
sirve para armar una guía de qué mirar: encuentra un camino, pero no uno
razonable.

## Límites a tener en cuenta

- **BFS minimiza la cantidad de obras, no los minutos.** El camino más
  corto en obras puede no ser el que menos horas lleva. El sistema lo
  aclara en pantalla y muestra el tiempo total del camino encontrado,
  pero no lo minimiza (para eso haría falta un algoritmo que use los pesos
  del grafo, como Dijkstra, que quedó fuera de este trabajo).
- **El catálogo de prueba es chico** (8 obras, 3 grupos). Los recorridos
  funcionan igual con cualquier tamaño (los experimentos usan hasta 20.000
  obras), pero con más obras y más personajes en común las consultas
  serían más ricas.

## Pruebas (`tests/test_recorridos.py`)

8 pruebas: BFS visita por niveles; DFS se mete hasta el fondo y vuelve;
BFS da la distancia mínima mientras que la profundidad del DFS puede ser
mayor; ambos alcanzan las mismas obras (y manejan obra aislada o
inexistente); camino más corto (con y sin camino); grupos conectados; DFS
y BFS sobre una cadena de 3.000 obras sin recursión; y los recorridos con
los datos reales.

```bash
python3 tests/test_recorridos.py
python3 experimentos/tp8_benchmark.py
```

## Versión 6 de la app

El submenú **[9] Explorar conexiones** suma cuatro opciones:

```
[e] Camino más corto entre dos obras (BFS)
[f] Obras relacionadas por cercanía (BFS)
[g] Explorar en profundidad desde una obra (DFS)
[h] Ver grupos de obras conectadas (DFS)
```
