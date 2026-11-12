"""Función de prioridad para el ranking de "imprescindibles".

El puntaje de una obra combina tres factores, todos llevados a una
escala de 0 a 10 para poder sumarlos:

    rating    -> el rating de la obra (ya viene de 0 a 10).
    recencia  -> qué tan reciente es. Como el usuario quiere ponerse al
                 día antes del estreno, lo más nuevo pesa más.
                 2008 (Iron Man) = 0, el año actual = 10.
    brevedad  -> qué tan corta es. Una serie de 330 minutos "cuesta"
                 más que una película de 120. 0 min = 10, 360 min o más = 0.

Los pesos dependen del perfil del usuario:
    casual -> le importa el tiempo: la brevedad suma.
    fan    -> no le importa la duración: solo rating y recencia.
"""

ANIO_INICIO_MCU = 2008
ANIO_ACTUAL = 2026
DURACION_MAXIMA_MIN = 360

PESOS_POR_PERFIL = {
    "casual": {"rating": 0.55, "recencia": 0.30, "brevedad": 0.15},
    "fan":    {"rating": 0.60, "recencia": 0.40, "brevedad": 0.00},
}


def _recencia(anio):
    avance = (anio - ANIO_INICIO_MCU) / (ANIO_ACTUAL - ANIO_INICIO_MCU)
    return 10 * max(0.0, min(1.0, avance))


def _brevedad(duracion_min):
    proporcion = min(duracion_min, DURACION_MAXIMA_MIN) / DURACION_MAXIMA_MIN
    return 10 * (1 - proporcion)


def calcular_prioridad(obra, perfil="casual"):
    """Devuelve el puntaje (0 a 10) de una obra para un perfil dado."""
    pesos = PESOS_POR_PERFIL.get(perfil, PESOS_POR_PERFIL["casual"])
    puntaje = (
        pesos["rating"] * obra.rating
        + pesos["recencia"] * _recencia(obra.anio)
        + pesos["brevedad"] * _brevedad(obra.duracion_min)
    )
    return round(puntaje, 2)
