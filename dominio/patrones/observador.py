import math
from dominio.puertos import PuertoObservador

class MonitorEstadisticas(PuertoObservador):
    def __init__(self):
        self.alcances = []
        self._altura_max = 0.0
    
    def al_aterrizar(self, resultado) -> None:
        self.alcances.append(resultado.alcance)
        if resultado.altura_max > self._altura_max:
            self._altura_max = resultado.altura_max
    
    def resumen(self) -> dict:
        if not self.alcances:
            return {}
        n = len(self.alcances)
        promedio = sum(self.alcances) / n
        desv_std = math.sqrt(sum((x - promedio) ** 2 for x in self.alcances) / n)

        return {"n": n, "alcance_max": max(self.alcances),"alcance_min": min(self.alcances),
                "promedio": promedio, "desv_std": desv_std, "altura_max": self._altura_max,}