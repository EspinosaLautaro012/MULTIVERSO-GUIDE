class Personaje:
    """Representa un personaje que puede aparecer en varias obras."""

    def __init__(self, nombre, obras=None):
        self._nombre = nombre
        self._obras = obras if obras is not None else []

    @property
    def nombre(self):
        return self._nombre

    @property
    def obras(self):
        return list(self._obras)

    def agregar_obra(self, titulo_obra):
        if titulo_obra not in self._obras:
            self._obras.append(titulo_obra)

    def __repr__(self):
        return f"Personaje({self._nombre}, {len(self._obras)} obra/s)"
