#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DH Inspector — Visualiza FK por DH, grafica juntas y eslabones en 3D,
y permite mover articulaciones con sliders o inputs numéricos.

Requisitos: numpy, matplotlib
    sudo apt-get install python3-matplotlib
o  pip install matplotlib
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, TextBox, CheckButtons

# -------------------- DH DEL ROBOT (EDITABLE) --------------------
# Formato por fila i (1..N): a_i [m], alpha_i [rad], d_i [m], theta_i [rad]
# Incluye tu "fila auxiliar" si la usas (no GDL).
# OJO: usa metros; si tienes mm conviértelo a m.
DH = [
    # i=0  (ascensor "base extra" para d0 + d_fix: se suma en runtime)
    # En muchas implementaciones, el ascensor se pone como Tz(d0 + d_fix).
    # Aquí dejamos d_i=0 y sumamos d0 + d_fix en runtime antes de la cadena.
    # Esta fila se puede dejar en identidad (a=0,alpha=0,d=0,theta=0).
    [0.0,            0.0,            0.0,         0.0],            # fila 0 (placeholder)

    # i=1
    [0.025,         -np.pi/2,        0.065,       0.0],            # theta1_offset + pi se aplica en runtime
    # i=2 (auxiliar, NO GDL)
    [0.0,            0.0,            0.10,        0.0],            # theta2_aux=0
    # i=3
    [0.215,          0.0,            0.0,         0.0],            # theta2_offset + pi en runtime
    # i=4
    [0.250,          np.pi,          0.0,         0.0],            # theta3_offset en runtime
    # i=5 (muñeca)
    [0.125,          0.0,            0.0,         0.0],            # -theta4 (o +theta4) en runtime
]

# Offsets de "cero" mecánico respecto al DH (ajústalos con medidas reales)
OFFSETS = {
    "d_fix": 0.80,       # m que se suman a d0
    "theta1_off": np.pi, # +π
    "theta2_off": np.pi, # +π
    "theta3_off": 0.0,   # 0
    "theta4_inv": True,  # True -> usa -theta4
}

# Límites razonables (para dibujar guías y validar rango)
LIMITS = {
    "d0":  (0.0, 0.45),              # m (0..450 mm)
    "th1": (-np.pi, np.pi),
    "th2": (-np.pi, np.pi),
    "th3": (-np.pi, np.pi),
    "th4": (-np.pi, np.pi),
}

# -------------------- FK por DH --------------------
def dh_matrix(theta, d, a, alpha):
    ct, st = np.cos(theta), np.sin(theta)
    ca, sa = np.cos(alpha), np.sin(alpha)
    return np.array([
        [ ct, -st*ca,  st*sa, a*ct],
        [ st,  ct*ca, -ct*sa, a*st],
        [  0,     sa,     ca,    d ],
        [  0,      0,      0,    1 ],
    ], dtype=float)

def fk_all_points(d0, th1, th2, th3, th4, dh=DH, offs=OFFSETS):
    """Devuelve lista de puntos 4x1 (homogéneos) de cada ‘junta’ y efector."""
    # Armamos la cadena:
    # T = Tz(d0 + d_fix) * (i=1..5)
    T = np.eye(4)
    T = T @ dh_matrix(0.0, d0 + offs["d_fix"], 0.0, 0.0)

    # i=1: theta1 + offset
    a1, al1, d1, _ = dh[1]
    T = T @ dh_matrix(th1 + offs["theta1_off"], d1, a1, al1)

    # i=2: auxiliar (sin GDL)
    a2, al2, d2, th2_aux = dh[2]
    T = T @ dh_matrix(th2_aux, d2, a2, al2)

    # i=3: theta2 + offset
    a3, al3, d3, _ = dh[3]
    T = T @ dh_matrix(th2 + offs["theta2_off"], d3, a3, al3)

    # i=4: theta3 + offset
    a4, al4, d4, _ = dh[4]
    T = T @ dh_matrix(th3 + OFFSETS["theta3_off"], d4, a4, al4)

    # i=5: theta4 (posible inversión de signo)
    a5, al5, d5, _ = dh[5]
    th4_eff = -th4 if offs["theta4_inv"] else th4
    T = T @ dh_matrix(th4_eff, d5, a5, al5)

    # Para mostrar todos los puntos intermedios, volvemos a multiplicar paso a paso
    points = []
    Tlist = []
    T = np.eye(4)
    T = T @ dh_matrix(0.0, d0 + offs["d_fix"], 0.0, 0.0); points.append(T @ np.array([0,0,0,1])); Tlist.append(T.copy())
    T = T @ dh_matrix(th1 + offs["theta1_off"], d1, a1, al1); points.append(T @ np.array([0,0,0,1])); Tlist.append(T.copy())
    T = T @ dh_matrix(th2_aux, d2, a2, al2);               points.append(T @ np.array([0,0,0,1])); Tlist.append(T.copy())
    T = T @ dh_matrix(th2 + offs["theta2_off"], d3, a3, al3); points.append(T @ np.array([0,0,0,1])); Tlist.append(T.copy())
    T = T @ dh_matrix(th3 + offs["theta3_off"], d4, a4, al4); points.append(T @ np.array([0,0,0,1])); Tlist.append(T.copy())
    T = T @ dh_matrix(th4_eff, d5, a5, al5);                points.append(T @ np.array([0,0,0,1])); Tlist.append(T.copy())
    # último punto (efector)
    ee = T @ np.array([0,0,0,1]); points.append(ee); Tlist.append(T.copy())
    return points, Tlist

# -------------------- GUI (matplotlib sliders) --------------------
class DHInspector:
    def __init__(self):
        self.mode_deg = False  # RAD por defecto

        # valores de articulaciones (radianes / metros)
        self.d0  = 0.10
        self.th1 = 0.0
        self.th2 = 0.0
        self.th3 = 0.0
        self.th4 = 0.0

        self.fig = plt.figure("DH Inspector")
        gs = self.fig.add_gridspec(6, 3, height_ratios=[12,1,1,1,1,1], width_ratios=[1,1,1], hspace=0.4)

        # 3D
        from mpl_toolkits.mplot3d import Axes3D  # noqa
        self.ax = self.fig.add_subplot(gs[0,:], projection='3d')
        self.ax.set_box_aspect([1,1,1])
        self.ax.set_xlabel('X [m]'); self.ax.set_ylabel('Y [m]'); self.ax.set_zlabel('Z [m]')
        self.ax.grid(True)

        # Sliders + texto (d0, th1..th4)
        self.sl_axes = []
        self.txt_boxes = []

        # Helper para crear slider + textbox
        def add_slider(row, label, vmin, vmax, v0, is_angle):
            ax_s = self.fig.add_subplot(gs[row, :2])
            ax_s.set_title(label)
            s = Slider(ax=ax_s, label="", valmin=vmin, valmax=vmax, valinit=v0)
            self.sl_axes.append((s, is_angle))
            ax_t = self.fig.add_subplot(gs[row, 2])
            tb = TextBox(ax_t, "Set", initial=f"{v0:.3f}")
            self.txt_boxes.append((tb, s, is_angle))
            return s, tb

        s_d0,_   = add_slider(1, "d0 [m]", *LIMITS["d0"], self.d0, False)
        s_t1,_   = add_slider(2, "θ1 [rad]", *LIMITS["th1"], self.th1, True)
        s_t2,_   = add_slider(3, "θ2 [rad]", *LIMITS["th2"], self.th2, True)
        s_t3,_   = add_slider(4, "θ3 [rad]", *LIMITS["th3"], self.th3, True)
        s_t4,_   = add_slider(5, "θ4 [rad]", *LIMITS["th4"], self.th4, True)

        self.sliders = [s_d0, s_t1, s_t2, s_t3, s_t4]

        # Botón RAD/DEG
        ax_btn = self.fig.add_axes([0.82, 0.93, 0.15, 0.05])
        self.btn_units = Button(ax_btn, "Modo: RAD")
        self.btn_units.on_clicked(self.toggle_units)

        # Conectar eventos
        for (s, is_ang) in self.sl_axes:
            s.on_changed(lambda _val: self.on_change())

        for (tb, s, is_ang) in self.txt_boxes:
            def submit(val, tb=tb, s=s, ang=is_ang):
                try:
                    v = float(val)
                    if self.mode_deg and ang:
                        v = np.deg2rad(v)
                    s.set_val(v)
                except ValueError:
                    pass
            tb.on_submit(submit)

        self.update_plot()
        plt.show()

    def get_values(self):
        vals = [s.val for (s, is_ang) in self.sl_axes]
        d0, th1, th2, th3, th4 = vals
        return float(d0), float(th1), float(th2), float(th3), float(th4)

    def on_change(self):
        # Actualiza cajas de texto con la unidad actual
        for (tb, s, is_ang) in self.txt_boxes:
            v = s.val
            if self.mode_deg and is_ang:
                tb.set_val(f"{np.rad2deg(v):.3f}")
            else:
                tb.set_val(f"{v:.3f}")
        self.update_plot()

    def toggle_units(self, _evt):
        self.mode_deg = not self.mode_deg
        self.btn_units.label.set_text("Modo: DEG" if self.mode_deg else "Modo: RAD")

        # Re-escala sliders de ángulos para mostrar límites en deg si procede
        for (s, is_ang), (tb, _, _) in zip(self.sl_axes, self.txt_boxes):
            if is_ang:
                if self.mode_deg:
                    s.valmin, s.valmax = np.rad2deg([LIMITS["th1"][0], LIMITS["th1"][1]])
                    # mostramos la caja en deg, pero mantenemos el valor interno en rad
                    tb.set_val(f"{np.rad2deg(s.val):.3f}")
                else:
                    s.valmin, s.valmax = LIMITS["th1"]
                    tb.set_val(f"{s.val:.3f}")
        self.fig.canvas.draw_idle()

    def update_plot(self):
        self.ax.cla()
        self.ax.set_xlabel('X [m]'); self.ax.set_ylabel('Y [m]'); self.ax.set_zlabel('Z [m]')
        self.ax.grid(True)

        d0, th1, th2, th3, th4 = self.get_values()
        pts, Ts = fk_all_points(d0, th1, th2, th3, th4)

        # Extrae xyz
        xyz = np.array([p[:3] for p in pts])  # shape (k,3)
        # Dibuja eslabones
        self.ax.plot(xyz[:,0], xyz[:,1], xyz[:,2], '-o', lw=2, ms=6, color='C0')

        # Dibuja frames locales (pequeñas triadas)
        L = 0.06
        for T in Ts:
            o = T[:3,3]
            x = o + L*T[:3,0]
            y = o + L*T[:3,1]
            z = o + L*T[:3,2]
            self.ax.plot([o[0],x[0]],[o[1],x[1]],[o[2],x[2]], color='r')
            self.ax.plot([o[0],y[0]],[o[1],y[1]],[o[2],y[2]], color='g')
            self.ax.plot([o[0],z[0]],[o[1],z[1]],[o[2],z[2]], color='b')

        # Texto con posiciones
        labels = ["base+d0", "J1", "aux", "J2", "J3", "J4", "EE"]
        for lab, p in zip(labels, xyz):
            self.ax.text(p[0], p[1], p[2], lab)

        # Autoscale caja
        allpts = xyz
        mins = allpts.min(axis=0); maxs = allpts.max(axis=0)
        span = np.maximum(maxs - mins, 0.2)
        ctr = 0.5*(maxs + mins)
        lim = np.max(span)*0.6
        self.ax.set_xlim(ctr[0]-lim, ctr[0]+lim)
        self.ax.set_ylim(ctr[1]-lim, ctr[1]+lim)
        self.ax.set_zlim(ctr[2]-lim, ctr[2]+lim)

        # Muestra EE
        ee = xyz[-1]
        self.ax.set_title(f"EE: x={ee[0]:.3f} m, y={ee[1]:.3f} m, z={ee[2]:.3f} m", fontsize=11)

        self.fig.canvas.draw_idle()


if __name__ == "__main__":
    DHInspector()
