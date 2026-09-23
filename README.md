# MultiversoGuide

Sistema de recomendaciones para saber qué películas, series y cómics del
universo Marvel conviene ver antes del estreno de la nueva Avengers en
diciembre.

Este es el entregable de la **Parte 01 (TP1)** del TP Integrador de
Algoritmos y Estructuras de Datos — UNaB, 2026.

## Estructura del proyecto

```
multiversoguide/
├── main.py                # Interfaz de terminal
├── gestor_datos.py        # Carga el JSON y expone buscar/listar/filtrar
├── models/
│   ├── obra.py             # Clase Obra (película/serie/cómic)
│   ├── personaje.py        # Clase Personaje
│   ├── fase_saga.py        # Clase FaseSaga
│   └── usuario.py          # Clase Usuario
├── data/
│   └── obras.json          # Datos de prueba (8 obras)
└── README.md
```

## Clases principales

- **Obra**: título, tipo, año, duración, fase, rating y personajes. Todos
  los atributos son privados (encapsulamiento) y se acceden mediante
  `@property`.
- **Personaje**: nombre y lista de obras en las que aparece.
- **FaseSaga**: nombre y orden dentro de la cronología del MCU.
- **Usuario**: nombre y perfil (`fan` o `casual`), con lista de obras
  vistas.

## Operaciones implementadas

1. **Buscar** una obra por título (coincidencia parcial).
2. **Listar** todas las obras, ordenadas por año.
3. **Filtrar** por tipo, fase/saga y/o personaje (combinables).

## Requisitos

- Python 3.8 o superior (no usa librerías externas).

## Cómo ejecutarlo

```bash
cd multiversoguide
python3 main.py
```

Se abre un menú interactivo por consola con las opciones de buscar,
listar, filtrar y salir.

## Datos de prueba

`data/obras.json` incluye 8 obras de ejemplo (películas y series) con
título, tipo, año, duración, fase, rating y personajes.

## Próximos pasos (siguientes entregas del TP)

- TP2: comparación de estrategias de búsqueda y análisis de complejidad.
- TP3-TP4: árbol de búsqueda / AVL para ordenar obras.
- TP5: árbol general para la jerarquía de fases/sagas.
- TP6: heap para el ranking de "Top-N imprescindibles".
- TP7-TP9: grafo, BFS/DFS y camino mínimo entre obras.
