import argparse

from dominio.modelos import ConfigExplosion
from dominio.puertos import PuertoEntrada
from adaptadores.entrada.yaml_config import cargar_config_yaml


class EntradaCLI(PuertoEntrada):
    def __init__(self, ruta_config: str = "config.yaml"):
        self._ruta_config = ruta_config

    def obtener_config(self) -> ConfigExplosion:
        config_base = cargar_config_yaml(self._ruta_config)

        parser = argparse.ArgumentParser(
            description="Simulacion Monte Carlo de una explosion"
        )

        parser.add_argument("--n", type=int, default=config_base.n_proyectiles)
        parser.add_argument("--v-min", type=float, default=config_base.v_min)
        parser.add_argument("--v-max", type=float, default=config_base.v_max)
        parser.add_argument("--g", type=float, default=config_base.g)
        parser.add_argument("--dt", type=float, default=config_base.dt)
        parser.add_argument("--semilla", type=int, default=config_base.semilla)

        parser.add_argument(
            "--tipo",
            choices=["ligero", "pesado", "arrastre"],
            default=config_base.tipo
        )

        parser.add_argument(
            "--metodo",
            choices=["euler", "verlet"],
            default=config_base.metodo
        )

        parser.add_argument(
            "--salida",
            choices=["animacion", "csv", "ambos"],
            default=config_base.salida
        )

        parser.add_argument(
            "--dist-angulo",
            choices=["uniforme", "normal", "vonmises"],
            default=config_base.dist_angulo
        )

        parser.add_argument(
            "--dist-vel",
            choices=["uniforme", "normal", "exponencial"],
            default=config_base.dist_velocidad
        )

        args = parser.parse_args()

        config_base.n_proyectiles = args.n
        config_base.v_min = args.v_min
        config_base.v_max = args.v_max
        config_base.g = args.g
        config_base.dt = args.dt
        config_base.semilla = args.semilla
        config_base.tipo = args.tipo
        config_base.metodo = args.metodo
        config_base.salida = args.salida
        config_base.dist_angulo = args.dist_angulo
        config_base.dist_velocidad = args.dist_vel

        return config_base