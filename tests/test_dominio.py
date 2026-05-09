from dominio.modelos import Proyectil
from dominio.patrones.fabrica import (FabricaLigero, FabricaPesado, FabricaConArrastre)

def test_fabrica_ligero_crea_proyectil_correcto():
    p = FabricaLigero().crear(45, 20)
    assert isinstance(p, Proyectil)
    assert p.masa == 0.5
    assert p.coef_arrastre == 0.0

def test_velocidad_inicial_correcta():
    import math
    p = FabricaLigero().crear(45, 20.0)
    v = math.sqrt(p.vx**2 + p.vy**2)
    assert abs(v - 20.0) < 1e-9

def test_sin_if_en_fabrica_ligero():
    import inspect, ast, textwrap
    src = textwrap.dedent(inspect.getsource(FabricaLigero.crear))
    ifs = [n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.If)]
    assert len(ifs) == 0

def test_fabrica_pesado_crea_proyectil_correcto():
    p = FabricaPesado().crear(30, 15)
    assert isinstance(p, Proyectil)
    assert p.masa == 5.0
    assert p.coef_arrastre == 0.0

def test_velocidad_inicial_pesado_correcta():
    import math
    p = FabricaPesado().crear(30, 15.0)
    velocidad = math.sqrt(p.vx**2 + p.vy**2)
    assert abs(velocidad - 15.0) < 1e-9

def test_sin_if_en_fabrica_pesado():
    import inspect, ast, textwrap
    src = textwrap.dedent(inspect.getsource(FabricaPesado.crear))
    ifs = [n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.If)]
    assert len(ifs) == 0

def test_fabrica_con_arrastre_crea_proyectil_correcto():
    p = FabricaConArrastre().crear(60, 10)
    assert isinstance(p, Proyectil)
    assert p.masa == 1.0
    assert p.coef_arrastre > 0.0

def test_velocidad_inicial_con_arrastre_correcta():
    import math
    p = FabricaConArrastre().crear(60, 10.0)
    velocidad = math.sqrt(p.vx**2 + p.vy**2)
    assert abs(velocidad - 10.0) < 1e-9

def test_sin_if_en_fabrica_con_arrastre():
    import inspect, ast, textwrap
    src = textwrap.dedent(inspect.getsource(FabricaConArrastre.crear))
    ifs = [n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.If)]
    assert len(ifs) == 0




