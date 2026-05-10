import math
import inspect
import ast
import textwrap
import pytest

from dominio.modelos import Proyectil
from dominio.patrones.fabrica import (FabricaLigero, FabricaPesado, FabricaConArrastre)
from dominio.patrones.estrategia import Euler, Verlet
from dominio.modelos import ResultadoProyectil
from dominio.patrones.observador import MonitorEstadisticas
from dominio.explosion import Explosion
from dominio.modelos import ConfigExplosion
from dominio.puertos import PuertoObservador
#tests para el método de Fábrica

def test_fabrica_ligero_crea_proyectil_correcto():
    p = FabricaLigero().crear(45, 20)
    assert isinstance(p, Proyectil)
    assert p.masa == 0.5
    assert p.coef_arrastre == 0.0

def test_velocidad_inicial_correcta():
    p = FabricaLigero().crear(45, 20.0)
    v = math.sqrt(p.vx**2 + p.vy**2)
    assert abs(v - 20.0) < 1e-9

def test_sin_if_en_fabrica_ligero():
    src = textwrap.dedent(inspect.getsource(FabricaLigero.crear))
    ifs = [n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.If)]
    assert len(ifs) == 0

def test_fabrica_pesado_crea_proyectil_correcto():
    p = FabricaPesado().crear(30, 15)
    assert isinstance(p, Proyectil)
    assert p.masa == 5.0
    assert p.coef_arrastre == 0.0

def test_velocidad_inicial_pesado_correcta():
    p = FabricaPesado().crear(30, 15.0)
    velocidad = math.sqrt(p.vx**2 + p.vy**2)
    assert abs(velocidad - 15.0) < 1e-9

def test_sin_if_en_fabrica_pesado():
    src = textwrap.dedent(inspect.getsource(FabricaPesado.crear))
    ifs = [n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.If)]
    assert len(ifs) == 0

def test_fabrica_con_arrastre_crea_proyectil_correcto():
    p = FabricaConArrastre().crear(60, 10)
    assert isinstance(p, Proyectil)
    assert p.masa == 1.0
    assert p.coef_arrastre > 0.0

def test_velocidad_inicial_con_arrastre_correcta():
    p = FabricaConArrastre().crear(60, 10.0)
    velocidad = math.sqrt(p.vx**2 + p.vy**2)
    assert abs(velocidad - 10.0) < 1e-9

def test_sin_if_en_fabrica_con_arrastre():
    src = textwrap.dedent(inspect.getsource(FabricaConArrastre.crear))
    ifs = [n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.If)]
    assert len(ifs) == 0

#Tests para el método estrategia

@pytest.mark.parametrize("angulo_deg", [30, 45, 60, 75])
def test_alcance_vs_analitico(angulo_deg):
    v0 = 20.0
    g = 9.8
    dt = 0.002
    p = FabricaLigero().crear(angulo_deg, v0)
    euler = Euler()
    while True:
        x_prev = p.x
        y_prev = p.y
        euler.paso(p, dt, g)
        if p.y < 0 and p.x != 0:
            f = y_prev / (y_prev - p.y)
            x_impacto = x_prev + f * (p.x - x_prev)
            break
    alcance_teorico = v0**2 * math.sin(2 * math.radians(angulo_deg)) / g
    assert abs(x_impacto - alcance_teorico) / alcance_teorico < 0.01

def test_verlet_conserva_mejor_energia_que_euler():
    def error_energia(estrategia):
        p = FabricaLigero().crear(45, 20)
        energia_inicial = p.energia_total(9.8)
        for _ in range(500):
            estrategia.paso(p, 0.05, 9.8)
            if p.y < 0:
                break
        energia_final = p.energia_total(9.8)
        return abs(energia_final - energia_inicial) / abs(energia_inicial)
    assert error_energia(Verlet()) < error_energia(Euler())

# fixtures de pytest
@pytest.fixture
def config_minima():
    return ConfigExplosion(n_proyectiles=20, v_min=10, v_max=20, semilla=7)

@pytest.fixture
def motor_euler():
    monitor = MonitorEstadisticas()
    motor = Explosion(FabricaLigero(), Euler(), [monitor])
    return motor, monitor

# tests para el método observador
def test_monitor_recibe_todos_los_aterrizajes(config_minima, motor_euler):
    motor, monitor = motor_euler
    motor.ejecutar(config_minima)
    assert monitor.resumen()["n"] == config_minima.n_proyectiles

def test_resumen_tiene_claves_esperadas(config_minima, motor_euler):
    motor, monitor = motor_euler
    motor.ejecutar(config_minima)
    for clave in ("n", "alcance_max", "alcance_min", "promedio", "desv_std"):
        assert clave in monitor.resumen()

def test_nuevo_observador_sin_modificar_motor():
    eventos = []
    class ObsCustom(PuertoObservador):
        def al_aterrizar(self, r):
            eventos.append(r.alcance)

    config = ConfigExplosion(n_proyectiles=10, v_min=10, v_max=20, semilla=1)
    motor = Explosion(FabricaLigero(), Euler(), [ObsCustom()])
    motor.ejecutar(config)
    assert len(eventos) == 10

# tests para motor explosion
def test_trayectorias_empiezan_en_origen(config_minima):
    motor = Explosion(FabricaLigero(), Euler())
    trajs, _ = motor.ejecutar(config_minima)
    for tray in trajs:
        assert tray[0] == (0.0, 0.0)

def test_reproducibilidad_con_misma_semilla():
    config = ConfigExplosion(n_proyectiles=30, semilla=99)
    _, r1 = Explosion(FabricaLigero(), Euler()).ejecutar(config)
    _, r2 = Explosion(FabricaLigero(), Euler()).ejecutar(config)
    for a, b in zip(r1, r2):
        assert abs(a.alcance - b.alcance) < 1e-10