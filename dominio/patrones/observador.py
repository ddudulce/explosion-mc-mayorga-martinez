import math
from dominio.puertos import PuertoObservador

class MonitorEstadisticas(PuertoObservador):
    def __init__(self):
        self.alcances = []
        self._altura_max = 0.0
    
    def al_aterrizar(self, resultado) -> None:
        self._alcances.append(resultado.alcance)
        if resultado.altura_max > self._altura_max:
            self._altura_max = resultado.altura_max
    
    def resumen(self) -> dict:
        if not self.alcances:
            return {}
        n = len(self._alcances)
        promedio = sum(self._alcances) / n
        desv_std = math.sqrt(sum((x - promedio) ** 2 for x in self._alcances) / n)

        return {"n": n, "alcance_max": max(self._alcances),"alcance_min": min(self._alcances),
                "promedio": promedio, "desv_std": desv_std, "altura_max": self._altura_max,}