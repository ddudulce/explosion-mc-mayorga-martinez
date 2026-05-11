from pathlib import Path

import yaml

from dominio.modelos import ConfigExplosion


def cargar_config_yaml(ruta: str = "config.yaml") -> ConfigExplosion:
    archivo = Path(ruta)

    if not archivo.exists():
        return ConfigExplosion()

    with open(archivo, "r", encoding="utf-8") as f:
        datos = yaml.safe_load(f) or {}

    simulacion = datos.get("simulacion", {})
    visualizacion = datos.get("visualizacion", {})
    distribucion = datos.get("distribucion", {})
    ejecucion = datos.get("ejecucion", {})

    dist_angulo = distribucion.get("angulo", {})
    dist_velocidad = distribucion.get("velocidad", {})

    return ConfigExplosion(
        n_proyectiles=simulacion.get("n_proyectiles", 300),
        v_min=simulacion.get("v_min", 5.0),
        v_max=simulacion.get("v_max", 30.0),
        g=simulacion.get("g", 9.8),
        dt=simulacion.get("dt", 0.04),
        semilla=simulacion.get("semilla", 42),
        trail_length=visualizacion.get("trail", 18),
        tipo=simulacion.get("tipo", "ligero"),
        metodo=simulacion.get("metodo", "euler"),
        salida=simulacion.get("salida", "animacion"),   
        modo_ejecucion=ejecucion.get("modo", "secuencial"),
        workers=ejecucion.get("workers", None),
        dist_angulo=dist_angulo.get("tipo", "uniforme"),
        angulo_media=dist_angulo.get("media", 90.0),
        angulo_sigma=dist_angulo.get("sigma", 20.0),
        angulo_kappa=dist_angulo.get("kappa", 6.0),
        dist_velocidad=dist_velocidad.get("tipo", "uniforme"),
        vel_media=dist_velocidad.get("media", 12.0),
        vel_sigma=dist_velocidad.get("sigma", 4.0),
        
    )