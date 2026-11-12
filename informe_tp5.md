# TP5 — Organizá tu universo

## Jerarquía elegida

El catálogo de MultiversoGuide tiene una organización natural de tipo
"pertenece a": cada obra pertenece a un tipo (película, serie, cómic),
y cada tipo pertenece a una saga del MCU. Eso es una jerarquía, y se
representa con un **árbol general (n-ario)**, donde cada nodo puede
tener cualquier cantidad de hijos:

```
Marvel
├── Saga del Infinito
│   └── Películas
│       ├── Iron Man
│       ├── Avengers: Infinity War
│       └── Avengers: Endgame
└── Saga del Multiverso
    ├── Series
    │   ├── Loki
    │   └── Secret Invasion
    └── Películas
        ├── Doctor Strange en el Multiverso de la Locura
        ├── Spider-Man: No Way Home
        └── Deadpool & Wolverine
```

Las categorías (Marvel, Saga, Tipo) son nodos internos; las obras son
las hojas y guardan el objeto `Obra` completo.

**Cómo se arma:** `GestorDatos` construye el árbol al cargar el JSON.
La saga se deduce de la fase de cada obra (fases 1-3 → Saga del
Infinito, fases 4-6 → Saga del Multiverso; si el dato ya trae el nombre
de la saga, se respeta). Si mañana se agrega un cómic o una saga nueva
al JSON, el árbol crea las ramas que falten solo, sin tocar código.

## Por qué un árbol general y no un BST

| | BST / AVL (TP3-TP4) | Árbol general (TP5) |
|---|---|---|
| Hijos por nodo | máximo 2 | cualquier cantidad |
| Qué representa | un **orden** (alfabético) | una **pertenencia** (jerarquía) |
| Búsqueda | O(log n), descarta ramas por comparación | O(n), no hay orden para descartar |

No compiten: se complementan. El AVL sirve para encontrar rápido una
obra por título; el árbol general sirve para explorar el catálogo por
categorías.

## Implementación (`busqueda/arbol_general.py`)

- `NodoGeneral`: nombre, lista de hijos, referencia al padre y (en las
  hojas) la obra.
- `ArbolGeneral`: `agregar_hijo`, `obtener_o_crear_hijo`, `buscar`,
  `camino_a`, `obras_de`, `contar_obras`, `altura` y los tres recorridos.

## Búsquedas

- **`buscar(nombre)`**: recorrido en profundidad, devuelve el nodo
  (categoría u obra). Es O(n) en el peor caso.
- **`camino_a(nombre)`**: sube por las referencias al padre y devuelve
  la ruta desde la raíz. Ej: `Marvel > Saga del Multiverso > Series > Loki`.
- **`obras_de(nodo)`**: todas las obras que cuelgan de una categoría.

## Ejemplos de recorridos

Sobre el árbol de ejemplo de las pruebas (`Raiz → A (A1, A2), B`):

| Recorrido | Orden de visita | Para qué sirve |
|---|---|---|
| **Preorden** | Raiz, A, A1, A2, B | Mostrar el árbol como índice con sangría |
| **Postorden** | A1, A2, A, B, Raiz | Calcular algo de una categoría a partir de sus hijos (contar, sumar) |
| **Por niveles** (BFS, con cola) | Raiz, A, B, A1, A2 | Ver el árbol capa por capa |

Sobre el catálogo real, el recorrido por niveles da:

```
Nivel 0: Marvel
Nivel 1: Saga del Infinito, Saga del Multiverso
Nivel 2: Películas, Series, Películas
Nivel 3: (las 8 obras)
```

## Funcionalidad en terminal (versión 3)

El menú principal suma la opción **[6] Explorar categorías**, que abre
un submenú:

```
[a] Ver el árbol completo          (preorden con cantidad de obras por categoría)
[b] Ver por niveles                (recorrido por niveles)
[c] Buscar una categoría u obra    (muestra la ruta y las obras que contiene)
[d] Volver
```

Ejemplo: buscar "Saga del Multiverso" muestra la ruta
`Marvel > Saga del Multiverso` y lista las 5 obras que contiene.

## Pruebas (`tests/test_arbol_general.py`)

8 pruebas: los tres recorridos, búsqueda y camino, altura, conteo de
obras, mapeo fase → saga, y la jerarquía armada con los datos reales
(todas las obras quedan en el árbol y las rutas son las esperadas).

```bash
python3 tests/test_arbol_general.py
```

## Nota para los próximos TP

El árbol general es la base para el grafo del TP7: las categorías
describen a qué grupo pertenece cada obra, pero todavía falta modelar
las **conexiones entre obras** (comparten personaje o evento), que es lo
que permite el camino mínimo.
