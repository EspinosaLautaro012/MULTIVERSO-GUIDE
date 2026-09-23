class FaseSaga:
    """Representa una fase o saga del MCU (ej. Fase 1, Saga del Infinito)."""

    def __init__(self, nombre, orden):
        self._nombre = nombre
        self._orden = orden

    @property
    def nombre(self):
        return self._nombre

    @property
    def orden(self):
        return self._orden

    def __repr__(self):
        return f"FaseSaga({self._nombre}, orden {self._orden})"

    def __lt__(self, otra):
        return self._orden < otra._orden
