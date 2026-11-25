class Obra:
    """Representa una obra del universo Marvel: película, serie o cómic."""

    def __init__(self, titulo, tipo, anio, duracion_min, fase, rating, personajes, descripcion =None):
        self._titulo = titulo
        self._tipo = tipo                # "pelicula", "serie" o "comic"
        self._anio = anio
        self._duracion_min = duracion_min
        self._fase = fase                # nombre de la FaseSaga a la que pertenece
        self._rating = rating
        self._personajes = personajes if personajes is not None else []
        self._descripcion= descripcion

    # --- Getters (encapsulamiento) ---
    @property
    def titulo(self):
        return self._titulo

    @property
    def tipo(self):
        return self._tipo

    @property
    def anio(self):
        return self._anio

    @property
    def duracion_min(self):
        return self._duracion_min

    @property
    def fase(self):
        return self._fase

    @property
    def rating(self):
        return self._rating

    @property
    def personajes(self):
        return list(self._personajes)
    @property
    def descripcion(self):
        return self._descripcion
    
    def obtener_info(self):
        personajes_str = ", ".join(self._personajes) if self._personajes else "sin datos"
        info = (
            f"{self._titulo} ({self._anio}) - {self._tipo.capitalize()}\n"
            f"Fase: {self._fase} | Duración: {self._duracion_min} min | Rating: {self._rating}\n"
            f"Personajes: {personajes_str}"
        )
        if self._descripcion:
            info += f"\nDescripción: {self._descripcion}"
        return info

    def __repr__(self):
        return f"{self._titulo} ({self._tipo}, {self._anio}, rating {self._rating})"
