# MultiversoGuide

Sistema de recomendaciones para saber qué películas, series y cómics del
universo Marvel conviene ver antes del estreno de la nueva Avengers en
diciembre.

TP Integrador de Algoritmos y Estructuras de Datos — UNaB, 2026.
**Versión actual: 5** (entregas TP1 a TP7).

## Cómo ejecutarlo

Requiere Python 3.8 o superior. No usa librerías externas.

```bash
cd multiversoguide
python3 main.py        # en Windows: python main.py
```

Hay que correrlo siempre desde la carpeta `multiversoguide` (la que
contiene `main.py`), porque los imports dependen de eso.

## Menú (versión 5)

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
├── busqueda/                # Estructuras de datos
│   ├── secuencial.py        # Búsqueda secuencial (TP2)
│   ├── arbol.py             # Árbol binario de búsqueda (TP3)
│   ├── avl.py               # Árbol AVL con rotaciones (TP4)
│   ├── arbol_general.py     # Árbol general: Marvel > Saga > Tipo > Obra (TP5)
│   ├── heap.py              # Heap binaria de máximos, hecha a mano (TP6)
│   ├── prioridad.py         # Función de prioridad del ranking (TP6)
│   └── grafo.py             # Grafo de conexiones entre obras, lista de adyacencia (TP7)
├── experimentos/            # Scripts de medición (TP2, TP4, TP6, TP7)
├── tests/                   # Pruebas de cada estructura
├── data/obras.json          # Datos de prueba
└── informe_tp2.md ... informe_tp7.md
```

## Pruebas y experimentos

```bash
python3 tests/test_arbol.py
python3 tests/test_avl.py
python3 tests/test_arbol_general.py
python3 tests/test_heap.py
python3 tests/test_grafo.py

python3 experimentos/tp2_benchmark.py
python3 experimentos/tp4_benchmark.py
python3 experimentos/tp6_benchmark.py
python3 experimentos/tp7_representacion.py
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

## Próximos pasos

- TP8-TP9: recorridos BFS/DFS y camino mínimo sobre el grafo.
- TP10: integración final y defensa.
