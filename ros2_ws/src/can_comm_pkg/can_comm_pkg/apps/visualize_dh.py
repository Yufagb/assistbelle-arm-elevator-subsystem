#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import Axes3D

# ------------------ Forward Kinematics Logic ------------------

from can_comm_pkg.apps.cinematica_directa import DH_PARAMS, dh_matrix

# ------------------ Forward Kinematics Logic ------------------

# dh_matrix y DH_PARAMS importados de cinematica_directa.py para mantener consistencia

def calculate_chain(d0, th1, th2, th3, th4):
    """
    Calcula las posiciones de todos los orígenes de los sistemas de coordenadas.
    Retorna una lista de puntos (x,y,z).
    """
    # Mapeo de variables a los eslabones
    # Link Fijo (idx 2) es constante 0
    vars_list = [d0, th1, 0.0, th2, th3, th4]
    
    T = np.eye(4)
    points = [T[:3, 3]] # Origen base (0,0,0)
    
    for i, p in enumerate(DH_PARAMS):
        val = vars_list[i]
        
        # Lógica de inversión y offset
        if p["type"] == "P":
            d_val = val + p["d"]
            theta_val = p["offset"]
        else:
            d_val = p["d"]
            if p.get("invert", False):
                val = -val
            theta_val = val + p["offset"]
            
        T = T @ dh_matrix(theta_val, d_val, p["a"], p["alpha"])
        points.append(T[:3, 3])
        
    return points, T[:3, 3] # Lista de puntos, Posición final

# ------------------ Visualization ------------------

# ------------------ Visualization ------------------

class RobotVisualizer:
    def __init__(self):
        self.fig = plt.figure(figsize=(10, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        plt.subplots_adjust(left=0.1, bottom=0.35)

        # Límites del gráfico
        limit = 0.8
        self.ax.set_xlim(-limit, limit)
        self.ax.set_ylim(-limit, limit)
        self.ax.set_zlim(0, 1.2)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_title('Visualización Cinemática Directa (DH)')

        # Elementos gráficos iniciales
        self.line, = self.ax.plot([], [], [], 'o-', lw=2, markersize=6, label='Robot Links')
        self.scat_ee = self.ax.scatter([], [], [], c='r', s=100, marker='*', label='End Effector')
        
        # Texto para mostrar posición
        self.text_pos = self.fig.text(0.05, 0.9, '', transform=self.fig.transFigure, fontsize=12, 
                            bbox=dict(facecolor='white', alpha=0.8))

        # Textos 3D para etiquetas en el gráfico
        self.labels_3d = []
        self.joint_names = ["Base", "J5 (Elev)", "J1 (Base)", "Link Fijo", "J2 (Homb)", "J3 (Codo)", "J4 (Muñe/EE)"]
        
        for _ in range(len(self.joint_names)):
            self.labels_3d.append(self.ax.text(0, 0, 0, "", fontsize=9))
            
        self.ax.legend()

    def update_plot(self, d0, th1, th2, th3, th4):
        points, ee_pos = calculate_chain(d0, th1, th2, th3, th4)
        
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        zs = [p[2] for p in points]

        self.line.set_data(xs, ys)
        self.line.set_3d_properties(zs)
        
        self.scat_ee._offsets3d = ([ee_pos[0]], [ee_pos[1]], [ee_pos[2]])
        
        # Actualizar etiquetas 3D
        for i, (lbl, p) in enumerate(zip(self.labels_3d, points)):
            lbl.set_position((p[0], p[1]))
            lbl.set_3d_properties(p[2])
            lbl.set_text(f"{self.joint_names[i]}")
        
        # Construir texto informativo
        info_str = "COORDENADAS (Metros):\n"
        info_str += f"EE (J4): [{ee_pos[0]:.3f}, {ee_pos[1]:.3f}, {ee_pos[2]:.3f}]\n"
        info_str += f"J5 (Elev): [{points[1][0]:.3f}, {points[1][1]:.3f}, {points[1][2]:.3f}]\n"
        info_str += f"J1 (Base): [{points[2][0]:.3f}, {points[2][1]:.3f}, {points[2][2]:.3f}]\n"
        info_str += f"J2 (Homb): [{points[4][0]:.3f}, {points[4][1]:.3f}, {points[4][2]:.3f}]\n"
        info_str += f"J3 (Codo): [{points[5][0]:.3f}, {points[5][1]:.3f}, {points[5][2]:.3f}]"

        self.text_pos.set_text(info_str)
        self.fig.canvas.draw_idle()
        plt.pause(0.001) # Necesario para actualizar en tiempo real

def main():
    viz = RobotVisualizer()
    
    # Sliders (Solo para modo interactivo manual)
    ax_d0 = plt.axes([0.15, 0.25, 0.7, 0.03])
    ax_th1 = plt.axes([0.15, 0.20, 0.7, 0.03])
    ax_th2 = plt.axes([0.15, 0.15, 0.7, 0.03])
    ax_th3 = plt.axes([0.15, 0.10, 0.7, 0.03])
    ax_th4 = plt.axes([0.15, 0.05, 0.7, 0.03])

    s_d0 = Slider(ax_d0, 'Ascensor (m)', 0.0, 0.5, valinit=0.0)
    s_th1 = Slider(ax_th1, 'Base (deg)', -180, 180, valinit=0.0)
    s_th2 = Slider(ax_th2, 'Hombro (deg)', -180, 180, valinit=0.0)
    s_th3 = Slider(ax_th3, 'Codo (deg)', -180, 180, valinit=0.0)
    s_th4 = Slider(ax_th4, 'Muñeca (deg)', -180, 180, valinit=0.0)

    def update_slider(val):
        d0 = s_d0.val
        th1 = np.deg2rad(s_th1.val)
        th2 = np.deg2rad(s_th2.val)
        th3 = np.deg2rad(s_th3.val)
        th4 = np.deg2rad(s_th4.val)
        viz.update_plot(d0, th1, th2, th3, th4)

    s_d0.on_changed(update_slider)
    s_th1.on_changed(update_slider)
    s_th2.on_changed(update_slider)
    s_th3.on_changed(update_slider)
    s_th4.on_changed(update_slider)

    # Inicializar
    update_slider(0)
    plt.show()

if __name__ == "__main__":
    main()
