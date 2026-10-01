# TP3 — Poné un árbol en tu sistema

## Clave de ordenamiento elegida

**Título de la obra**, en orden alfabético. Es el criterio más natural
para esta funcionalidad: permite buscar una obra exacta rápido y listar
el catálogo de forma ordenada y predecible para el usuario.

## Implementación

El árbol ya existía desde el TP2 (`busqueda/arbol.py`), pero era un
"árbol de juguete" usado solo para medir tiempos. En este TP se completó
con lo que pedía la consigna y se lo integró de verdad al sistema:

- **Inserción**: ya estaba (TP2).
- **Búsqueda**: ya estaba (TP2).
- **Recorridos** (nuevo): `recorrido_inorder()`, `recorrido_preorder()`
  y `recorrido_postorder()`, agregados a `ArbolBusquedaObras`.
- **Integración real** (nuevo): `GestorDatos` ahora arma el árbol al
  cargar los datos (`gestor_datos.py`), y expone dos operaciones nuevas:
  - `buscar_exacto_arbol(titulo)` → usa `arbol.buscar()`.
  - `listar_ordenado_por_titulo()` → usa `arbol.recorrido_inorder()`.
- **Interfaz** (nuevo): el menú de `main.py` (ahora "v2") agrega las
  opciones [4] y [5] para usar estas dos funcionalidades desde la
  consola.

## Por qué el inorder es la base de "listar ordenado"

El recorrido inorder visita primero el subárbol izquierdo, después la
raíz, y por último el subárbol derecho. Como el árbol se arma de forma
que todo nodo a la izquierda tiene un título "menor" y todo nodo a la
derecha tiene un título "mayor", visitar en ese orden entrega las obras
siempre alfabéticamente ordenadas — sin tener que ordenar la lista cada
vez que se pide (como sí hace `listar_todas()` con `sorted()`).

## Pruebas (`tests/test_arbol.py`)

Se probaron los cinco casos clave:
1. Árbol vacío no rompe nada y no "encuentra" nada.
2. Insertar varias obras y poder buscarlas todas por título exacto.
3. El recorrido inorder devuelve los títulos en orden alfabético exacto
   (comparado contra `sorted()` de Python).
4. El recorrido preorder arranca en la raíz.
5. El recorrido postorder termina en la raíz.

Se ejecutan con:
```bash
python3 tests/test_arbol.py
```
Las cinco pasan correctamente (ver salida de consola al correrlo).

## Comparación contra la búsqueda secuencial del TP2

La comparación de tiempos ya se hizo en el TP2 (`informe_tp2.md`), con
el mismo árbol que ahora se integró de verdad. Resultados (sin cambios,
porque la lógica de búsqueda no se modificó, solo se la conectó al resto
del sistema):

| N elementos | Búsqueda secuencial | Búsqueda en árbol |
|-------------|----------------------|---------------------|
| 100         | 0.0031 ms            | 0.0008 ms           |
| 1.000       | 0.0254 ms            | 0.0011 ms           |
| 10.000      | 0.3204 ms            | 0.0014 ms           |

La conclusión del TP2 se mantiene: para búsquedas exactas sobre un
catálogo que puede crecer, conviene el árbol. La búsqueda secuencial
(opción [1] del menú) se mantiene aparte porque cumple un propósito
distinto: permite coincidencias **parciales** ("escribí parte del
título"), algo que un BST ordenado por título exacto no resuelve
directamente.

## Versión 2 de la app

El menú de `main.py` ahora tiene 5 operaciones (antes 3):

```
[1] Buscar obra por título (parcial)
[2] Listar todas las obras (por año)
[3] Filtrar obras
[4] Buscar obra por título exacto (árbol)
[5] Listar ordenado alfabéticamente (árbol)
[6] Salir
```

## Nota para TP4

Este árbol todavía **no está balanceado**: si las obras se insertaran ya
ordenadas alfabéticamente, degeneraría en una lista. Por ahora no es un
problema porque el dataset se inserta en el orden del JSON (no
alfabético), pero en el TP4 se va a convertir esta misma estructura en
un AVL con rotaciones, para garantizar O(log n) siempre, sin depender
del orden de inserción.
