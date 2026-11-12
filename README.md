# MultiversoGuide

Sistema de recomendaciones para saber qué películas, series y cómics del
universo Marvel conviene ver antes del estreno de la nueva Avengers en
diciembre.

TP Integrador de Algoritmos y Estructuras de Datos — UNaB, 2026.
**Versión final: 6** (entregas TP1 a TP8).

## Cómo ejecutarlo

Requiere Python 3.8 o superior. No usa librerías externas.

```bash
cd multiversoguide
python3 main.py        # en Windows: python main.py
```

Hay que correrlo siempre desde la carpeta `multiversoguide` (la que
contiene `main.py`), porque los imports dependen de eso.

## Menú (versión 6)

```
[1] Buscar obra por título (parcial)
[2] Listar todas las obras (por año)
[3] Filtrar obras
[4] Buscar obra por título exacto (árbol)
[5] Listar ordenado alfabéticamente (árbol)
[6] Explorar categorías (árbol general)
[7] Top imprescindibles (ranking)
[8] Marcar una obra como vista
[9] Explorar conexiones (grafo)
[10] Salir
```

La opción **[9]** abre un submenú:

```
[a] Ver obras conectadas con una obra
[b] Ver qué comparten dos obras
[c] Ver el grafo completo
[d] Ver estadísticas del grafo
[e] Camino más corto entre dos obras (BFS)
[f] Obras relacionadas por cercanía (BFS)
[g] Explorar en profundidad desde una obra (DFS)
[h] Ver grupos de obras conectadas (DFS)
[i] Volver
```

## Funcionalidades de la propuesta (TP0) y dónde están

| Funcionalidad prometida | Dónde está |
|---|---|
| Buscar una obra por título y ver su información | **[1]** (búsqueda parcial) y **[4]** (exacta, con árbol) |
| Watch order recomendado, cronológico o por fase | **[2]** (por año), **[3]** (filtrar por fase) y **[6]** (por saga y tipo) |
| Top-N de contenido imprescindible | **[7]**, con perfil casual o fan |
| Explorar obras relacionadas a un personaje o evento | **[3]** (filtrar por personaje) y **[9]** (conexiones por personajes en común) |
| Camino mínimo entre dos obras | **[9] → [e]** (el que tiene menos obras) |

## Estructura del proyecto

```
multiversoguide/
├── main.py                  # Interfaz de terminal
├── gestor_datos.py          # Carga el JSON y conecta todas las estructuras
├── models/                  # Clases del dominio (TP1)
│   ├── obra.py
│   ├── personaje.py
│   ├── fase_saga.py
│   └── usuario.py
├── busqueda/                # Estructuras de datos y algoritmos
│   ├── secuencial.py        # Búsqueda secuencial (TP2)
│   ├── arbol.py             # Árbol binario de búsqueda (TP3)
│   ├── avl.py               # Árbol AVL con rotaciones (TP4)
│   ├── arbol_general.py     # Árbol general: Marvel > Saga > Tipo > Obra (TP5)
│   ├── heap.py              # Heap binaria de máximos, hecha a mano (TP6)
│   ├── prioridad.py         # Función de prioridad del ranking (TP6)
│   ├── grafo.py             # Grafo de conexiones, lista de adyacencia (TP7)
│   └── recorridos.py        # BFS, DFS, camino más corto y grupos (TP8)
├── experimentos/            # Scripts de medición (TP2, TP4, TP6, TP7, TP8)
├── tests/                   # Pruebas de cada estructura
├── data/obras.json          # Datos de prueba
└── informe_tp2.md ... informe_tp8.md
```

## Pruebas y experimentos

```bash
python3 tests/test_arbol.py
python3 tests/test_avl.py
python3 tests/test_arbol_general.py
python3 tests/test_heap.py
python3 tests/test_grafo.py
python3 tests/test_recorridos.py

python3 experimentos/tp2_benchmark.py
python3 experimentos/tp4_benchmark.py
python3 experimentos/tp6_benchmark.py
python3 experimentos/tp7_representacion.py
python3 experimentos/tp8_benchmark.py
```

## Entregas

| TP | Tema | Informe |
|---|---|---|
| TP1 | Clases del dominio, carga de datos, buscar/listar/filtrar | este README |
| TP2 | Búsqueda secuencial vs. árbol, complejidad | `informe_tp2.md` |
| TP3 | Árbol binario de búsqueda integrado | `informe_tp3.md` |
| TP4 | AVL y comparación con el BST desbalanceado | `informe_tp4.md` |
| TP5 | Árbol general (jerarquía de categorías) | `informe_tp5.md` |
| TP6 | Heap y ranking Top-N | `informe_tp6.md` |
| TP7 | Grafo de conexiones entre obras | `informe_tp7.md` |
| TP8 | Recorridos BFS y DFS | `informe_tp8.md` |

## Limitaciones conocidas

- El catálogo de prueba es chico (8 obras) y su grafo tiene 3 grupos
  separados, así que no existe camino entre todas las obras.
- El camino más corto minimiza la cantidad de obras, no los minutos.
