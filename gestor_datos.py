import json
import os
from models.obra import Obra


class GestorDatos:
    """Carga las obras desde un archivo JSON y ofrece las operaciones
    principales sobre esos datos: buscar, listar y filtrar."""

    def __init__(self, ruta_json):
        self._ruta_json = ruta_json
        self._obras = []
        self._cargar_datos()

    def _cargar_datos(self):
        if not os.path.exists(self._ruta_json):
            raise FileNotFoundError(f"No se encontró el archivo de datos: {self._ruta_json}")

        with open(self._ruta_json, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        self._obras = [
            Obra(
                titulo=item["titulo"],
                tipo=item["tipo"],
                anio=item["anio"],
                duracion_min=item["duracion_min"],
                fase=item["fase"],
                rating=item["rating"],
                personajes=item.get("personajes", []),
            )
            for item in datos
        ]

    @property
    def obras(self):
        return list(self._obras)

    # --- Operación 1: Buscar ---
    def buscar_por_titulo(self, texto):
        texto = texto.lower().strip()
        return [obra for obra in self._obras if texto in obra.titulo.lower()]

    # --- Operación 2: Listar ---
    def listar_todas(self, orden_por_anio=True):
        if orden_por_anio:
            return sorted(self._obras, key=lambda obra: obra.anio)
        return list(self._obras)

    # --- Operación 3: Filtrar ---
    def filtrar(self, tipo=None, fase=None, personaje=None):
        resultado = self._obras

        if tipo:
            resultado = [o for o in resultado if o.tipo.lower() == tipo.lower()]
        if fase:
            resultado = [o for o in resultado if fase.lower() in o.fase.lower()]
        if personaje:
            resultado = [
                o for o in resultado
                if any(personaje.lower() in p.lower() for p in o.personajes)
            ]

        return resultado
