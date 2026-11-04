import json
import os

class GestorPuntuaciones:
    def __init__(self, nombre_archivo="ranking.json"):
        self._nombre_archivo = nombre_archivo

    @property
    def nombre_archivo(self):
        return self._nombre_archivo

    def guardar_puntuacion(self, nombre_jugador, puntaje):
        puntuaciones = []
        if os.path.exists(self._nombre_archivo):
            try:
                with open(self._nombre_archivo, "r") as archivo:
                    puntuaciones = json.load(archivo)
            except json.JSONDecodeError:
                puntuaciones = []

        puntuaciones.append({"nombre": nombre_jugador, "puntaje": puntaje})
        puntuaciones = sorted(puntuaciones, key=lambda x: x["puntaje"], reverse=True)

        with open(self._nombre_archivo, "w") as archivo:
            json.dump(puntuaciones, archivo, indent=4)

    def obtener_mejores_puntuaciones(self, limite=5):
        if not os.path.exists(self._nombre_archivo):
            return []
        try:
            with open(self._nombre_archivo, "r") as archivo:
                puntuaciones = json.load(archivo)
                return puntuaciones[:limite]
        except json.JSONDecodeError:
            return []