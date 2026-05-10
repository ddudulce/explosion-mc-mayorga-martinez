import random
import math

from dominio.modelos import ConfigExplosion, ResultadoProyectil
from dominio.puertos import PuertoFabrica, PuertoEstrategia, PuertoObservador

class Explosion:
    def __init__(self, fabrica: PuertoFabrica, estrategia: PuertoEstrategia,
                observadores: list[PuertoObservador] | None = None):
        self._fabrica = fabrica
        self._estrategia = estrategia
        self._observadores = list(observadores or [])

    def ejecutar(self, config: ConfigExplosion) -> tuple[list, list]:
        rng = random.Random(config.semilla)
        condiciones_iniciales = []
        for _ in range(config.n_proyectiles):
            angulo = self._generar_angulo(rng, config)
            v0 = self._generar_velocidad(rng, config)
            condiciones_iniciales.append((angulo, v0))
        trayectorias = []
        resultados = []

        for observador in self._observadores:
            observador._al_iniciar(config)
            
        for angulo_deg, v0 in condiciones_iniciales:
            trayectoria, resultado = self._simular_proyectil(angulo_deg, v0, config)
            trayectorias.append(trayectoria)
            resultados.append(resultado)
            for observador in self._observadores:
                    observador.al_aterrizar(resultado)

        for observador in self._observadores:
            observador._al_finalizar(resultados)
        return trayectorias, resultados

    def _generar_angulo(self, rng, config: ConfigExplosion) -> float:
        if config.dist_angulo == "normal":
            return rng.gauss(config.angulo_media, config.angulo_sigma)
        if config.dist_angulo == "vonmises":
            media_rad = math.radians(config.angulo_media)
            return math.degrees(rng.vonmisesvariate(media_rad, config.angulo_kappa))
        return rng.uniform(0.0, 360.0)

    def _generar_velocidad(self, rng, config: ConfigExplosion) -> float:
        if config.dist_velocidad == "normal":
            return max(0.0, rng.gauss(config.vel_media, config.vel_sigma))
        if config.dist_velocidad == "exponencial":
            return rng.expovariate(1.0 / config.vel_media)
        return rng.uniform(config.v_min, config.v_max)

    def _simular_proyectil(self, angulo_deg: float, v0: float, config: ConfigExplosion) -> tuple[list, ResultadoProyectil]:
        p = self._fabrica.crear(angulo_deg, v0)
        trayectoria = [(p.x, p.y)]
        altura_max = p.y
        tiempo = 0.0
        energia_inicial = p.energia_total(config.g)
        x_impacto  = p.x
        tiempo_vuelo = tiempo
        for _ in range(100000):
            x_prev = p.x
            y_prev = p.y
            tiempo_prev = tiempo
            self._estrategia.paso(p, config.dt, config.g)
            tiempo += config.dt
            trayectoria.append((p.x, p.y))
            if p.y > altura_max:
                altura_max = p.y
            if p.y < 0:
                if y_prev != p.y:
                    f = y_prev / (y_prev - p.y)
                else: f = 0.0
                x_impacto = x_prev + f * (p.x - x_prev)
                tiempo_vuelo = tiempo_prev + f * config.dt
                p.x = x_impacto
                p.y = 0.0
                trayectoria[-1] = (x_impacto, 0.0)
                break
        energia_final = p.energia_total(config.g)

        resultado = ResultadoProyectil(angulo_deg=angulo_deg, v0=v0, masa=p.masa, alcance=x_impacto,
                                    altura_max=altura_max, tiempo_vuelo=tiempo_vuelo, energia_inicial=energia_inicial,
                                    energia_final=energia_final, trayectoria=trayectoria)
        return trayectoria, resultado