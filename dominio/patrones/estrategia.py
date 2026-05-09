from dominio.modelos import Proyectil
from dominio.puertos import PuertoEstrategia

class Euler(PuertoEstrategia):
    def paso(self, p: Proyectil,
            dt: float, g: float) -> None:
        ax = -p.coef_arrastre / p.masa * p.velocidad() * p.vx
        ay = -g - p.coef_arrastre / p.masa * p.velocidad() * p.vy
        p.x += p.vx * dt
        p.y += p.vy * dt
        p.vx += ax * dt
        p.vy += ay * dt
    @property
    def nombre(self) -> str:
        return "Euler (orden 1)"

class Verlet(PuertoEstrategia):
    def paso(self, p: Proyectil,
            dt: float, g: float) -> None:
        ax = -p.coef_arrastre / p.masa * p.velocidad() * p.vx
        ay = -g - p.coef_arrastre / p.masa * p.velocidad() * p.vy
        x_nuevo = p.x + p.vx * dt + 0.5 * ax * dt**2
        y_nuevo = p.y + p.vy * dt + 0.5 * ay * dt**2
        vx_temp = p.vx + ax * dt
        vy_temp = p.vy + ay * dt
        
        p_temp = Proyectil(x=x_nuevo, y=y_nuevo, vx=vx_temp,
                        vy=vy_temp, masa=p.masa, coef_arrastre=p.coef_arrastre)
        ax_nuevo = -p_temp.coef_arrastre / p_temp.masa * p_temp.velocidad() * p_temp.vx
        ay_nuevo = -g - p_temp.coef_arrastre / p_temp.masa * p_temp.velocidad() * p_temp.vy
        p.x = x_nuevo
        p.y = y_nuevo
        p.vx += 0.5 * (ax + ax_nuevo) * dt
        p.vy += 0.5 * (ay + ay_nuevo) * dt
    @property
    def nombre(self) -> str:
        return "Verlet (orden 2)"