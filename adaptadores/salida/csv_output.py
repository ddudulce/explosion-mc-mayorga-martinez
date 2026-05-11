import csv
from pathlib import Path

from dominio.puertos import PuertoObservador


class SalidaCSV(PuertoObservador):
    def __init__(self, ruta: str = "resultados.csv"):
        self._ruta = Path(ruta)
        self._iniciado = False

        self._campos = [
            "angulo_deg",
            "v0",
            "masa",
            "alcance",
            "altura_max",
            "tiempo_vuelo",
            "error_energia",
        ]

    def al_iniciar(self, config) -> None:
        with open(self._ruta, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self._campos)
            writer.writeheader()

        self._iniciado = True

    def al_aterrizar(self, resultado) -> None:
        if not self._iniciado:
            self.al_iniciar(None)

        with open(self._ruta, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self._campos)

            writer.writerow({
                "angulo_deg": resultado.angulo_deg,
                "v0": resultado.v0,
                "masa": resultado.masa,
                "alcance": resultado.alcance,
                "altura_max": resultado.altura_max,
                "tiempo_vuelo": resultado.tiempo_vuelo,
                "error_energia": resultado.error_energia,
            })