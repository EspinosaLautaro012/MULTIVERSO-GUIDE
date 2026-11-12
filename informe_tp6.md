# TP6 — Que el sistema elija primero

## Qué problema resuelve

La funcionalidad estrella de MultiversoGuide es el **Top-N de
imprescindibles**: "¿qué tengo que ver antes del estreno?". Hace falta
un ranking que (1) se pueda pedir de cualquier tamaño N, (2) cambie según
el usuario y (3) se mantenga actualizado cuando el catálogo o el usuario
cambian. Eso es una **cola de prioridad**, y se implementó con una heap
binaria.

## Función de prioridad (`busqueda/prioridad.py`)

Combina tres factores, todos llevados a una escala de 0 a 10:

| Factor | Qué mide | Cómo se calcula |
|---|---|---|
| Rating | calidad de la obra | el rating tal cual (0 a 10) |
| Recencia | qué tan nueva es | 2008 (Iron Man) = 0, 2026 = 10 |
| Brevedad | cuánto tiempo cuesta verla | 0 min = 10, 360 min o más = 0 |

Los pesos dependen del **perfil del usuario** (la idea de los dos
recorridos que se planteó desde el TP0):

| Perfil | Rating | Recencia | Brevedad |
|---|---|---|---|
| casual | 0,55 | 0,30 | 0,15 |
| fan | 0,60 | 0,40 | 0,00 |

Se eligió así porque el usuario objetivo se quiere poner al día antes de
un estreno: lo reciente importa más que lo viejo, y a quien tiene poco
tiempo una serie de 330 minutos le sale más cara que una película. El
fan, en cambio, no descuenta por duración.

Resultado con el catálogo actual (Top 5, perfil casual):

```
1. Deadpool & Wolverine                           7.87
2. Spider-Man: No Way Home                        7.56
3. Avengers: Endgame                              7.20
4. Avengers: Infinity War                         7.17
5. Doctor Strange en el Multiverso de la Locura   7.10
```

*Loki* queda sexta para el perfil casual (330 min), pero sube al segundo
puesto para el perfil fan: el mismo catálogo da rankings distintos según
quién pregunta.

## Heap binaria (`busqueda/heap.py`)

Implementada a mano sobre una lista, **sin `heapq`**, como indica la
cátedra. La lista representa un árbol binario completo (hijos de `i` en
`2i+1` y `2i+2`, padre en `(i-1)//2`) y la obra de mayor puntaje queda
siempre en la raíz. Ante un empate de puntaje sale primero el título
alfabéticamente menor, para que el ranking sea siempre el mismo.

| Operación | Complejidad |
|---|---|
| `insertar` (sube el elemento) | O(log n) |
| `ver_max` | O(1) |
| `extraer_max` (hunde el último) | O(log n) |
| `desde_lista` (heapify) | O(n) |
| `top_n(k)` | O(k log n) |

`desde_lista` arma la heap en O(n) hundiendo los nodos internos de
abajo hacia arriba, que es más barato que insertar de a uno (O(n log n)).

## Integración al sistema (versión 4)

- `GestorDatos.top_n(n, perfil, excluir)` arma la heap con las obras
  puntuadas y devuelve las N primeras. `excluir` permite sacar las obras
  que el usuario ya vio.
- El menú suma **[7] Top imprescindibles** (elige perfil y cantidad) y
  **[8] Marcar una obra como vista**, que usa la clase `Usuario` (que
  hasta ahora no se usaba) y el AVL/BST para encontrar la obra por título.
- Resultado: el ranking es dinámico. Si el usuario marca *Deadpool &
  Wolverine* como vista, desaparece del Top y entra la siguiente.

## Consulta Top-N: ejemplo

```
> Elegí una opción: 7
Perfil (casual/fan) [Enter = casual]: casual
¿Cuántas obras querés en el ranking? [Enter = 5]: 3

TOP 3 imprescindibles - perfil casual
----------------------------------------------------
1. Deadpool & Wolverine                           7.87
2. Spider-Man: No Way Home                        7.56
3. Avengers: Endgame                              7.20
```

## Por qué una heap y no ordenar todo el dataset cada vez

Ordenar todo cuesta O(n log n) y entrega mucho más de lo que se pide:
ordena las n obras cuando solo interesan las primeras N. La heap deja
la mejor en la raíz y saca solo las que hacen falta.

Script: `experimentos/tp6_benchmark.py`. Se mide en **comparaciones**
(no depende de la máquina) y en **tiempo**.

### Experimento 1 — una sola consulta Top-10

| N obras | Comparaciones (ordenar todo) | Comparaciones (heap) | Tiempo ordenar | Tiempo heap |
|---|---|---|---|---|
| 1.000 | 8.649 | 2.109 | 0,94 ms | 0,35 ms |
| 10.000 | 119.834 | 19.124 | 14,09 ms | 3,15 ms |
| 100.000 | 1.529.053 | 188.420 | 346,40 ms | 78,79 ms |

Las comparaciones de la heap crecen casi linealmente con n (≈ n + k log n)
y las del ordenamiento crecen como n log n: a 100.000 obras la heap hace
unas 8 veces menos.

**Aclaración importante sobre los tiempos:** para poder contar las
comparaciones, el ordenamiento de esta tabla usa una función comparadora
escrita en Python, que es más lenta que el `sorted()` normal. Contra el
`sorted()` nativo de Python (escrito en C, ordenando con una `key`) la
ventaja en tiempo es bastante menor:

| N obras | `sorted()` nativo | heap propia |
|---|---|---|
| 1.000 | 0,24 ms | 0,32 ms |
| 10.000 | 4,35 ms | 3,20 ms |
| 100.000 | 75,16 ms | 36,53 ms |

Es decir: con un catálogo chico (1.000 obras) el `sorted()` nativo
gana, porque está implementado en C y nuestra heap en Python puro. La
heap empieza a convenir recién con catálogos grandes. La ventaja
asintótica es real, pero no hay que presentarla como "10 veces más
rápida" en cualquier situación.

### Experimento 2 — ranking dinámico

El caso donde la heap realmente se justifica: 10.000 obras, y 200
rondas de "llega una obra nueva y se pide el Top-10".

| Estrategia | Comparaciones | Tiempo total |
|---|---|---|
| Ordenar todo en cada ronda | 24.234.138 | 3.203 ms |
| Heap persistente | 70.057 | 10 ms |

Acá la diferencia es enorme (unas 350 veces menos comparaciones y unas
300 veces menos tiempo) porque la heap persistente solo hace una
inserción O(log n) y una extracción de K elementos, mientras que ordenar
todo repite el trabajo completo en cada ronda.

## Conclusión técnica

- Para un ranking que **se consulta una sola vez** sobre un catálogo
  chico, ordenar y cortar es perfectamente válido (y con `sorted()` hasta
  es más rápido). La ventaja de la heap crece con el tamaño del catálogo.
- Para un ranking **dinámico**, que se recalcula a medida que llegan
  obras nuevas o el usuario marca obras como vistas, la heap es la
  estructura correcta: cada cambio cuesta O(log n) en lugar de rehacer
  un ordenamiento de O(n log n).
- Con el catálogo actual (8 obras) la diferencia práctica es
  inexistente; la heap está pensada para que el sistema siga respondiendo
  bien cuando el catálogo crezca a cientos o miles de obras (series,
  cómics, spin-offs).

## Pruebas (`tests/test_heap.py`)

7 pruebas: heap vacía, extracción de mayor a menor, desempate por título,
heapify contra un ordenamiento de referencia (500 elementos), que
`top_n` no modifique la heap, la función de prioridad (rango y diferencia
entre perfiles) y el Top-N del sistema con datos reales (orden,
exclusión de obras vistas y N mayor al total).

```bash
python3 tests/test_heap.py
```

## Nota para los próximos TP

Para el grafo del TP7 las obras van a necesitar **conexiones entre sí**
(personajes o eventos compartidos). Esas conexiones también pueden
alimentar la función de prioridad: por ejemplo, subirle el puntaje a una
obra que conecta con muchas otras.
