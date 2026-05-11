from dominio.explosion import Explosion
from dominio.patrones.fabrica import (
    FabricaLigero,
    FabricaPesado,
    FabricaConArrastre,
)
from dominio.patrones.estrategia import Euler, Verlet
from dominio.patrones.observador import MonitorEstadisticas

from adaptadores.entrada.cli import EntradaCLI
from adaptadores.salida.csv_output import SalidaCSV


def seleccionar_fabrica(tipo: str):
    fabricas = {
        "ligero": FabricaLigero,
        "pesado": FabricaPesado,
        "arrastre": FabricaConArrastre,
    }

    if tipo not in fabricas:
        raise ValueError(f"Tipo de proyectil no reconocido: {tipo}")

    return fabricas[tipo]()


def seleccionar_estrategia(metodo: str):
    estrategias = {
        "euler": Euler,
        "verlet": Verlet,
    }

    if metodo not in estrategias:
        raise ValueError(f"Metodo numerico no reconocido: {metodo}")

    return estrategias[metodo]()


def main():
    entrada = EntradaCLI()
    config = entrada.obtener_config()

    fabrica = seleccionar_fabrica(config.tipo)
    estrategia = seleccionar_estrategia(config.metodo)

    monitor = MonitorEstadisticas()
    observadores = [monitor]

    if config.salida in ("csv", "ambos"):
        observadores.append(SalidaCSV())

    motor = Explosion(
        fabrica=fabrica,
        estrategia=estrategia,
        observadores=observadores
    )

    trayectorias, resultados = motor.ejecutar(config)

    print("Simulacion finalizada")
    print(f"Proyectiles simulados: {len(resultados)}")
    print(f"Fabrica: {fabrica.nombre}")
    print(f"Metodo: {estrategia.nombre}")

    resumen = monitor.resumen()
    if resumen:
        print(f"Alcance promedio: {resumen['promedio']:.3f} m")
        print(f"Alcance maximo: {resumen['alcance_max']:.3f} m")
        print(f"Altura maxima: {resumen['altura_max']:.3f} m")

    if config.salida == "animacion":
        print("La salida de animacion se agregara en el adaptador correspondiente.")

    return trayectorias, resultados


if __name__ == "__main__":
    main()