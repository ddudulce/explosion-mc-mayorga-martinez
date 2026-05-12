import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.collections import LineCollection
from dominio.puertos import PuertoSalida

class SalidaAnimacion(PuertoSalida):
    def titulo(self, config) -> str:
        if config.dist_angulo == "uniforme" and config.dist_velocidad == "uniforme":
            return "EXPLOSION CLASICA - angulo uniforme - vel uniforme"

        if config.dist_angulo == "vonmises":
            return (f"EXPLOSION DIRIGIDA - angulo vonMises "
                    f"($\\kappa$={config.angulo_kappa}, $\\mu$={config.angulo_media:.0f}$^\\circ$)")

        if config.dist_angulo == "uniforme" and config.dist_velocidad == "exponencial":
            return (f"METRALLA - angulo uniforme - vel exponencial "
                    f"($\\mu$={config.vel_media:.0f} m/s)")

        if config.dist_angulo == "normal" and config.dist_velocidad == "normal":
            return (f"COHETE DISPERSO - angulo normal " f"($\\sigma$={config.angulo_sigma:.0f}$^\\circ$) - vel normal "
                    f"($\\mu$={config.vel_media:.0f}, $\\sigma$={config.vel_sigma:.0f})")

        return f"EXPLOSION - angulo {config.dist_angulo} - vel {config.dist_velocidad}"

    def mostrar(self, config, trayectorias, resultados) -> None:
        if not trayectorias:
            print("No hay trayectorias para mostrar.")
            return

        fig = plt.figure(figsize=(14, 7), facecolor="#0a0f0a")
        gs = fig.add_gridspec(2, 2, width_ratios=[2.3, 1.0], height_ratios=[1, 1])

        ax_tray = fig.add_subplot(gs[:, 0])
        ax_hist = fig.add_subplot(gs[0, 1])
        ax_stats = fig.add_subplot(gs[1, 1])
        
        for ax in (ax_tray, ax_hist, ax_stats):
            ax.set_facecolor("#0a0f0a")
            ax.tick_params(colors="#00ff41")
            for borde in ax.spines.values():
                borde.set_color("#00ff41")
        ax_tray.set_title(self.titulo(config), color="#00ff41", fontsize=10)
        ax_tray.set_xlabel("x (m)", color="#00ff41")
        ax_tray.set_ylabel("y (m)", color="#00ff41")

        xs = [x for tray in trayectorias for x, y in tray]
        ys = [y for tray in trayectorias for x, y in tray]

        ax_tray.set_xlim(min(xs) - 1, max(xs) + 1)
        ax_tray.set_ylim(min(0, min(ys)) - 1, max(ys) + 1)
        
        lineas = LineCollection([], colors="#00ff41", linewidths=0.6, alpha=0.35)
        ax_tray.add_collection(lineas)
        
        impactos = ax_tray.scatter([], [], color = "orange", marker = "x")
        texto = ax_tray.text(0.02, 0.95, "", transform=ax_tray.transAxes, color="#00ff41", va="top")
        max_frames = max(len(tray) for tray in trayectorias)

        def actualizar(frame):
            segmentos = []
            impactos_x = []
            impactos_y = []
            alcances = []
            for tray, resultado in zip(trayectorias, resultados):
                limite = min(frame + 1, len(tray))
                inicio = max(0, limite - config.trail_length)
                tramo = tray[:limite]

                if len(tramo) > 1:
                    segmentos.append(np.array(tramo))

                if frame >= len(tray) - 1:
                    impactos_x.append(resultado.alcance)
                    impactos_y.append(0.0)
                    alcances.append(resultado.alcance)
            lineas.set_segments(segmentos)

            if impactos_x:
                impactos.set_offsets(np.column_stack((impactos_x, impactos_y)))
            else:
                impactos.set_offsets(np.empty((0, 2)))

            ax_hist.clear()
            ax_hist.set_facecolor("#0a0f0a")
            ax_hist.tick_params(colors="#00ff41")

            for borde in ax_hist.spines.values():
                borde.set_color("#00ff41")

            ax_hist.set_title("Histograma de alcances", color="#00ff41")
            ax_hist.set_xlabel("alcance (m)", color="#00ff41", labelpad=8)
            ax_hist.set_ylabel("frecuencia", color="#00ff41", labelpad=14)
            if alcances:
                ax_hist.hist(alcances, bins=20, color="#00ff41")

            ax_stats.clear()
            ax_stats.set_facecolor("#0a0f0a")
            ax_stats.axis("off")
            aterrizados = len(alcances)
            total = len(resultados)
            en_vuelo = total - aterrizados

            if alcances:
                promedio = sum(alcances) / len(alcances)
                alcance_max = max(alcances)
            else:
                promedio = 0.0
                alcance_max = 0.0

            ax_stats.text(0.05, 0.90, f"Proyectiles: {total}\n" f"En vuelo: {en_vuelo}\n" f"Aterrizados: {aterrizados}\n\n"
                        f"Promedio: {promedio:.2f} m\n" f"Máximo: {alcance_max:.2f} m", color="#00ff41", va="top")
            tiempo = frame * config.dt
            texto.set_text(f"t = {tiempo:.2f} s\n" f"vuelo: {en_vuelo} | tierra: {aterrizados}")
            return lineas, impactos, texto

        animacion = FuncAnimation(fig, actualizar, frames=max_frames, interval=30, blit=False, repeat=False)
        fig.subplots_adjust(left=0.06, right=0.99, bottom=0.10, top=0.90, wspace=0.238, hspace=0.13)
        plt.show()
