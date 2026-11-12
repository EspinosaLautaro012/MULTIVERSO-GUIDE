# TP7 — Conectá las cosas

## Modelo del grafo

| Elemento | Decisión |
|---|---|
| **Vértices** | Una obra (película, serie o cómic), identificada por su título. |
| **Aristas** | Dos obras están conectadas si **comparten al menos un personaje**. |
| **Tipo** | **Dirigido y pesado** |
| **Peso** | El costo de "ir" a una obra = **los minutos que dura esa obra**. |
| **Representación** | **Lista de adyacencia** |

### Por qué los vértices son obras

Todo lo que el sistema recomienda, filtra y ordena son obras, y las
funcionalidades que siguen (recorridos y camino mínimo entre obras, TP8
y TP9) son preguntas sobre obras: "¿qué tengo que ver para llegar de
esta a esta otra?". Si los vértices fueran personajes, habría que
traducir cada respuesta de vuelta a obras.

### Por qué la arista es "comparten un personaje"

Es la relación que realmente importa para ver una película con contexto:
si dos obras comparten un personaje, ver una ayuda a entender la otra.
Además es un dato que **ya existía** en el catálogo (`personajes` de cada
obra), así que las conexiones se calculan solas: al agregar una obra
nueva al JSON, el grafo la conecta sin tocar código. Cada arista guarda
también *cuáles* personajes comparten, para poder explicar la conexión
al usuario.

### Por qué dirigido y pesado

- **La conexión en sí es simétrica**: si A comparte un personaje con B,
  B lo comparte con A. Por eso cada conexión se guarda como **dos
  arcos** (A→B y B→A).
- **El costo no es simétrico**: lo que le cuesta al usuario "llegar" a
  una obra es lo que dura verla. Ir hacia *Endgame* cuesta 181 minutos;
  ir hacia *Iron Man* cuesta 126. Por eso los dos arcos tienen pesos
  distintos y el grafo es dirigido.
- La ventaja de elegirlo así: el costo de un camino es simplemente la
  suma de sus pesos, y equivale a **todo lo que el usuario tiene que ver
  después de la obra de origen** (que ya vio). Ejemplo con los datos
  reales: de *Iron Man* a *Endgame* directo cuesta 181 minutos; pasando
  por *Infinity War* cuesta 149 + 181 = 330. Esto es lo que va a usar el
  camino mínimo del TP9.
- En el TP8 (recorridos BFS/DFS) los pesos se ignoran.

### Por qué lista de adyacencia

Se compararon las dos representaciones con catálogos sintéticos de
distinto tamaño (`experimentos/tp7_representacion.py`). Cada obra recibe
3 personajes al azar y cada personaje aparece en promedio en 3 obras:

| Obras | Arcos | Densidad | Memoria lista | Memoria matriz | Pedir vecinos (lista) | Pedir vecinos (matriz) |
|---|---|---|---|---|---|---|
| 200 | 1.800 | 4,52 % | 455 KB | 332 KB | 0,4 µs | 8,3 µs |
| 1.000 | 8.878 | 0,89 % | 2.141 KB | 7.922 KB | 0,4 µs | 23,0 µs |
| 2.000 | 17.860 | 0,45 % | 4.293 KB | 31.474 KB | 0,6 µs | 48,5 µs |

Lo que muestra:

- **La densidad cae a medida que crece el catálogo.** Cada obra se
  conecta con unas pocas (las que comparten sus personajes), no con todas,
  así que los arcos crecen en proporción a V pero las celdas de la matriz
  crecen como V². Un grafo así se llama *ralo*.
- La matriz necesita V² celdas aunque casi todas valgan 0. La lista solo
  guarda las conexiones que existen: espacio O(V + E).
- Pedir los vecinos de una obra con la matriz obliga a recorrer una fila
  entera (O(V)); con la lista alcanza con recorrer sus conexiones
  (O(grado)), por eso queda casi constante.
- La lista guarda además información que la matriz no tiene lugar para
  guardar (los personajes que explican cada conexión).

**Cuándo la matriz sería mejor:** la única consulta donde la matriz gana
es "¿existe la arista u→v?", que es O(1) contra O(grado) de la lista.
Y como se ve en la primera fila, con un catálogo chico (200 obras) la
matriz incluso usa menos memoria que la lista, porque cada objeto
`Arista` pesa más que una celda. La lista se justifica por hacia dónde
va el sistema: un catálogo que crece, donde el grafo es cada vez más ralo.
(Las cifras de memoria de la lista incluyen los índices temporales que se
usan al construirla, así que la comparan de forma conservadora.)

Con el catálogo real actual (8 obras) la densidad es 25 %, un número
alto simplemente porque hay muy pocas obras; la decisión se toma pensando
en el catálogo completo, no en el de prueba.

## Implementación (`busqueda/grafo.py`)

- `Arista`: destino, peso y personajes en común.
- `Grafo`: diccionario `{título: [Arista, ...]}` con `agregar_vertice`,
  `agregar_arista`, `existe_arista`, `obtener_arista`, `vecinos`, `grado`,
  `aislados`, `cantidad_vertices`, `cantidad_aristas` y `densidad`.
- `construir_grafo_por_personajes(obras)`: arma el grafo. Para no comparar
  todas las obras contra todas (O(n²)) arma primero un índice
  personaje → obras donde aparece y conecta solo las que figuran juntas.

## El grafo con los datos reales

| Obra A | Obra B | Personajes en común |
|---|---|---|
| Iron Man | Avengers: Infinity War | Tony Stark |
| Iron Man | Avengers: Endgame | Tony Stark |
| Avengers: Infinity War | Avengers: Endgame | Thanos, Tony Stark |
| Avengers: Infinity War | Doctor Strange en el Multiverso de la Locura | Doctor Strange |
| Avengers: Infinity War | Spider-Man: No Way Home | Doctor Strange |
| Doctor Strange en el Multiverso de la Locura | Spider-Man: No Way Home | Doctor Strange |
| Loki | Deadpool & Wolverine | Kang |

8 vértices, 7 conexiones (14 arcos) y una obra aislada: *Secret Invasion*
(su único personaje, Nick Fury, no aparece en ninguna otra obra cargada).

## Ejemplos de consultas

```
Obras conectadas con 'Avengers: Endgame':
  - Avengers: Infinity War  (comparten: Thanos, Tony Stark)
  - Iron Man  (comparten: Tony Stark)

'Iron Man' y 'Avengers: Endgame' están conectadas.
Personajes en común: Tony Stark

'Iron Man' y 'Loki' NO están conectadas directamente.

Estadísticas del grafo:
  Obras (vértices):          8
  Conexiones entre obras:    7
  Densidad:                  25.0%
  Obra más conectada:        Avengers: Infinity War (4 conexiones)
  Obras sin conexiones:      Secret Invasion
```

## Funcionalidad integrada (versión 5)

El menú suma **[9] Explorar conexiones**, con un submenú:

```
[a] Ver obras conectadas con una obra
[b] Ver qué comparten dos obras
[c] Ver el grafo completo          (lista de adyacencia)
[d] Ver estadísticas del grafo
[e] Volver
```

Las obras se pueden escribir parcialmente ("endgame"); si el texto
coincide con varias, el sistema muestra las coincidencias y pide más
precisión. Salir pasó a ser la opción **[10]**.

## Limitación importante de los datos actuales

Con el catálogo de prueba el grafo tiene **3 componentes separados**:

1. *Iron Man*, *Infinity War*, *Endgame*, *Doctor Strange en el
   Multiverso de la Locura* y *Spider-Man: No Way Home*.
2. *Loki* y *Deadpool & Wolverine* (unidas solo por Kang).
3. *Secret Invasion*, sola.

Es decir que, por ejemplo, **no existe ningún camino entre *Iron Man* y
*Loki***. Para que el camino mínimo del TP9 tenga sentido hay que ampliar
el catálogo con más obras y personajes en común (por ejemplo, obras que
unan la Saga del Infinito con la del Multiverso). No hace falta cambiar
código: alcanza con agregar obras al JSON.

## Pruebas (`tests/test_grafo.py`)

7 pruebas: grafo vacío; vértices, aristas, grado y obras aisladas; que
el peso dependa del sentido; que no se dupliquen aristas y se rechacen
extremos inexistentes; densidad; el grafo armado con los datos reales
(conexiones, pesos, simetría de los arcos, obra aislada); y las consultas
de obras conectadas.

```bash
python3 tests/test_grafo.py
python3 experimentos/tp7_representacion.py
```

## Nota para los próximos TP

- **TP8:** BFS y DFS sobre este mismo grafo (usan `vecinos()`).
- **TP9:** camino mínimo sobre los pesos (minutos de contenido), que ya
  quedan cargados en cada arco.
