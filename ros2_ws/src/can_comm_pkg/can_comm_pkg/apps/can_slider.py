#!/usr/bin/env python3
import threading
import time
import math
import tkinter as tk
from tkinter import ttk

import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32MultiArray


class SliderNode(Node):
    def __init__(self):
        super().__init__('can_slider')
        self.pub = self.create_publisher(String, 'can_command', 10)
        self.sub = self.create_subscription(Float32MultiArray, 'motors_state', self.on_state, 10)

        # Estado actual (de can_node)
        self.positions = [0.0]*5      # rad, rad, rad, rad, mm
        self.vels      = [0.0]*5
        # Último setpoint enviado por slider (rad, rad, rad, rad, mm)
        self.setpoints = [0.0]*5

        # Constante de filtro de entrada
        self.alpha = 0.1

        # Ventana temporal para gráficas (s)
        self.window_secs = 30.0
        self.hist_t   = []
        self.hist_pos = [[] for _ in range(5)]
        self.hist_sp  = [[] for _ in range(5)]
        self.hist_err = [[] for _ in range(5)]

        # Polling A# (5 Hz)
        self.timer_poll = self.create_timer(0.2, self.poll_states)

        # Rate-limit, deadband y step (en rad/mm)
        self.last_pub_ts = [0.0]*5
        self.min_interval = 0.05
        self.deadband = [0.01, 0.01, 0.01, 0.01, 1.0]   # rad | mm
        self.step     = [0.01, 0.01, 0.01, 0.01, 1.0]   # rad | mm
        self.last_sent = [0.0]*5

        self.get_logger().info("can_slider listo (GUI en otra hebra).")

    # ----------------- ROS -----------------
    def on_state(self, msg: Float32MultiArray):
        if len(msg.data) < 10:
            return
        self.positions = list(msg.data[:5])
        self.vels      = list(msg.data[5:])

        now = time.time()
        self.hist_t.append(now)
        for i in range(5):
            p  = float(self.positions[i])
            sp = float(self.setpoints[i])
            er = float(sp - p)
            self.hist_pos[i].append(p)
            self.hist_sp[i].append(sp)
            self.hist_err[i].append(er)

        tmin = now - self.window_secs
        while self.hist_t and self.hist_t[0] < tmin:
            self.hist_t.pop(0)
            for arr in (self.hist_pos, self.hist_sp, self.hist_err):
                for j in range(5):
                    if arr[j]:
                        arr[j].pop(0)

    def poll_states(self):
        for i in range(1, 6):
            self.pub.publish(String(data=f"A{i}"))

    def set_joint(self, idx: int, value_rad_or_mm: float):
        """value siempre en unidades base (rad para J1..J4, mm para J5)."""
        st = self.step[idx]
        q = round(value_rad_or_mm / st) * st if st > 0 else value_rad_or_mm

        # Aplicar filtro a articulacion
        q = self.alpha*q + (1-self.alpha)*self.last_sent[idx]

        if abs(q - self.last_sent[idx]) < self.deadband[idx]:
            return

        now = time.time()
        if now - self.last_pub_ts[idx] < self.min_interval:
            return

        self.last_pub_ts[idx] = now
        self.last_sent[idx]   = q
        self.setpoints[idx]   = q

        j = idx + 1
        if j < 5:
            self.pub.publish(String(data=f"C{j}:{q},0.0"))
        else:
            self.pub.publish(String(data=f"C5:{q}"))


# ---------------- GUI (multi-joint, 2 paneles, eje X=tiempo, RAD/DEG) ----------------
class SliderGUI:
    BASE_COLORS = ["#44DDDD", "#99DD44", "#DD9944", "#BB77FF", "#FF7777"]  # J1..J5

    def __init__(self, node: SliderNode):
        self.node = node
        self.root = tk.Tk()
        self.root.title("CAN Sliders — multi-joint (líneas, tiempo)")

        # Modo de entrada para J1..J4: 'rad' o 'deg'
        self.angle_mode = tk.StringVar(value="rad")

        frame = ttk.Frame(self.root, padding=10)
        frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # ---------- Selección y controles superiores ----------
        top = ttk.Frame(frame)
        top.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0,8))
        ttk.Label(top, text="Mostrar joints:").pack(side="left", padx=(0,8))
        self.joint_enabled = [tk.BooleanVar(value=(i==0)) for i in range(5)]
        for i in range(5):
            ttk.Checkbutton(top, text=f"J{i+1}", variable=self.joint_enabled[i]).pack(side="left")

        ttk.Label(top, text="  Ventana (s):").pack(side="left", padx=(10,2))
        self.win_var = tk.DoubleVar(value=self.node.window_secs)
        ttk.Entry(top, textvariable=self.win_var, width=5).pack(side="left")
        ttk.Button(top, text="Aplicar", command=self.apply_window).pack(side="left", padx=(4,8))

        # Botón de unidades RAD/DEG (afecta J1..J4 en la UI; envío siempre en rad)
        self.btn_units = ttk.Button(top, text="Modo: RAD", command=self.toggle_units)
        self.btn_units.pack(side="left")

        # ---------- Sliders + marcas ----------
        labels_rad = ["J1 (rad)", "J2 (rad)", "J3 (rad)", "J4 (rad)", "J5 (mm)"]
        self.scales = []
        self.tick_frames = []
        self.step_vars, self.db_vars = [], []
        row = 1
        for i, lab in enumerate(labels_rad):
            ttk.Label(frame, text=lab).grid(row=row, column=0, sticky="w")

            # rango base en rad/mm; la UI re-mapea cuando esté en DEG
            (mn, mx) = ((-math.pi, math.pi) if i < 4 else (0.0, 450.0))
            var = tk.DoubleVar(value=0.0)
            scale = ttk.Scale(
                frame,
                from_=mn, to=mx, orient="horizontal", variable=var,
                command=lambda _v, idx=i, v=var: self.on_slider(idx, v)
            )
            scale.grid(row=row, column=1, sticky="ew", padx=8)
            frame.columnconfigure(1, weight=1)
            self.scales.append((var, scale))
            row += 1

            # Marcas bajo el slider (5 marcas)
            tick = ttk.Frame(frame)
            tick.grid(row=row, column=1, sticky="ew", pady=(0,6))
            self.tick_frames.append(tick)
            row += 1

            # step & deadband (se mantienen en rad/mm)
            cfg = ttk.Frame(frame); cfg.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0,8))
            ttk.Label(cfg, text="step (rad/mm):").pack(side="left")
            sv = tk.DoubleVar(value=self.node.step[i]); ttk.Entry(cfg, textvariable=sv, width=6).pack(side="left", padx=(2,8))
            ttk.Label(cfg, text="deadband (rad/mm):").pack(side="left")
            dv = tk.DoubleVar(value=self.node.deadband[i]); ttk.Entry(cfg, textvariable=dv, width=6).pack(side="left", padx=(2,8))
            ttk.Button(cfg, text="Aplicar", command=lambda idx=i, sv=sv, dv=dv: self.apply_smoothing(idx, sv.get(), dv.get())).pack(side="left")
            self.step_vars.append(sv); self.db_vars.append(dv)
            row += 1

        # ---------- Estado ----------
        self.lbl_state = ttk.Label(frame, text="pos: […] | sp: […] | err: […]")
        self.lbl_state.grid(row=row, column=0, columnspan=2, sticky="w", pady=(0,6))
        row += 1

        # ---------- Paneles ----------
        self.canvas_sp_pos = tk.Canvas(frame, width=760, height=220, bg="#111")
        self.canvas_sp_pos.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(8,4))
        row += 1
        self.canvas_err    = tk.Canvas(frame, width=760, height=180, bg="#111")
        self.canvas_err.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(0,8))

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        # Inicializa marcas
        self.refresh_ticks()
        self.update_gui()

    # ---------- Utilidades de color ----------
    def _hex_to_rgb(self, hx):
        hx = hx.lstrip('#'); return tuple(int(hx[i:i+2], 16) for i in (0,2,4))
    def _rgb_to_hex(self, rgb):
        r,g,b = rgb; return f"#{r:02X}{g:02X}{b:02X}"
    def _lighten(self, hx, frac=0.55):
        r,g,b = self._hex_to_rgb(hx)
        r = int(r + (255 - r)*frac); g = int(g + (255 - g)*frac); b = int(b + (255 - b)*frac)
        return self._rgb_to_hex((r,g,b))

    # ---------- Handlers superiores ----------
    def toggle_units(self):
        self.angle_mode.set("deg" if self.angle_mode.get()=="rad" else "rad")
        self.btn_units.config(text=f"Modo: {self.angle_mode.get().upper()}")
        # Reconfigura rangos de los 4 primeros sliders y sus marcas
        for i in range(4):
            _, scale = self.scales[i]
            if self.angle_mode.get() == "deg":
                scale.configure(from_=-180.0, to=180.0)  # UI en grados
                # Convierte el valor mostrado (interno rad) a deg
                cur_rad = self.node.setpoints[i]
                scale.set(math.degrees(cur_rad))
            else:
                scale.configure(from_=-math.pi, to=math.pi)
                # Valor mostrado en rad
                scale.set(self.node.setpoints[i])
        self.refresh_ticks()

    def apply_smoothing(self, idx, step, deadband):
        try:
            self.node.step[idx] = float(step)
            self.node.deadband[idx] = float(deadband)
        except ValueError:
            pass

    def apply_window(self):
        try:
            w = float(self.win_var.get())
            if w > 1.0:
                self.node.window_secs = w
        except ValueError:
            pass

    # ---------- Sliders ----------
    def on_slider(self, idx: int, var: tk.DoubleVar):
        val = var.get()
        # Si es J1..J4 y estamos en DEG, convierte a rad para enviar
        if idx < 4 and self.angle_mode.get() == "deg":
            self.node.set_joint(idx, math.radians(val))
        else:
            self.node.set_joint(idx, val)

    # ---------- Marcas bajo cada slider ----------
    def refresh_ticks(self):
        for i, tick in enumerate(self.tick_frames):
            for w in tick.winfo_children():
                w.destroy()
            # 5 marcas equidistantes
            if i < 4:
                if self.angle_mode.get() == "deg":
                    labels = ["−180", "−90", "0", "90", "180"]
                else:
                    labels = [f"−{math.pi:.2f}", f"−{(math.pi/2):.2f}", "0", f"{(math.pi/2):.2f}", f"{math.pi:.2f}"]
            else:
                labels = ["0", "112.5", "225", "337.5", "450"]
            # distribuye en 5 columnas
            for c, txt in enumerate(labels):
                ttk.Label(tick, text=txt).grid(row=0, column=c, sticky="e" if c==0 else ("w" if c==4 else "nsew"))
            # que el contenedor estire
            for c in range(5):
                tick.columnconfigure(c, weight=1)

    # ---------- Dibujo de paneles ----------
    def autoscale(self, series_list):
        vals = [v for s in series_list for v in (s if s else [])]
        if not vals: return -1.0, 1.0
        mn = min(vals); mx = max(vals)
        if mn == mx: mn -= 1.0; mx += 1.0
        span = mx - mn
        return mn - 0.05*span, mx + 0.05*span

    def draw_series_time(self, canvas, t_all, series_list, colors, mn, mx, pad=40):
        W  = int(canvas['width']); H = int(canvas['height'])
        canvas.create_line(pad, H-pad, W-pad, H-pad, fill="#555")
        canvas.create_line(pad, pad, pad, H-pad, fill="#555")
        canvas.create_text(pad-12, pad, text=f"{mx:.2f}", fill="#bbb", anchor="e")
        canvas.create_text(pad-12, H-pad, text=f"{mn:.2f}", fill="#bbb", anchor="e")

        window = self.node.window_secs
        x0 = pad; x1 = W - pad; y0 = H - pad
        for frac, label in ((0.0, "0"), (0.5, f"{window/2:.0f}"), (1.0, f"{window:.0f}s")):
            x = x0 + (x1 - x0) * frac
            canvas.create_line(x, y0, x, y0+5, fill="#777")
            canvas.create_text(x, y0+14, text=label, fill="#bbb")

        if not t_all or max((len(s) for s in series_list), default=0) < 2:
            return

        tmax = t_all[-1]
        for s, col in zip(series_list, colors):
            if len(s) < 2: 
                continue
            t = t_all[-len(s):]
            pts = []
            for ti, val in zip(t, s):
                frac = (ti - (tmax - window)) / window
                frac = max(0.0, min(1.0, frac))
                x = pad + (W - 2*pad) * frac
                y = H - pad - (H - 2*pad) * ((val - mn) / (mx - mn))
                pts.extend((x, y))
            canvas.create_line(*pts, fill=col, width=2)

    def draw_legend(self, canvas, labels, colors, pad=40):
        x = pad + 10; y = pad - 14
        for lab, col in zip(labels, colors):
            canvas.create_rectangle(x, y-6, x+14, y+6, fill=col, outline=col)
            canvas.create_text(x+22, y, text=lab, fill="#ddd", anchor="w")
            x += 130

    def draw_sp_pos_panel(self):
        c = self.canvas_sp_pos
        c.delete("all")
        enabled_idx = [i for i,b in enumerate(self.joint_enabled) if b.get()]
        if not enabled_idx or len(self.node.hist_t) < 2:
            return

        series, colors, labels = [], [], []
        for i in enabled_idx:
            base = self.BASE_COLORS[i]
            lite = self._lighten(base, 0.55)
            series.append(self.node.hist_sp[i]);   colors.append(base); labels.append(f"J{i+1} setpoint")
            series.append(self.node.hist_pos[i]);  colors.append(lite); labels.append(f"J{i+1} pos")

        mn, mx = self.autoscale(series)
        self.draw_series_time(c, self.node.hist_t, series, colors, mn, mx)
        self.draw_legend(c, labels, colors)

    def draw_err_panel(self):
        c = self.canvas_err
        c.delete("all")
        enabled_idx = [i for i,b in enumerate(self.joint_enabled) if b.get()]
        if not enabled_idx or len(self.node.hist_t) < 2:
            return

        series = [self.node.hist_err[i] for i in enabled_idx]
        colors = [self.BASE_COLORS[i] for i in enabled_idx]
        labels = [f"J{i+1} error" for i in enabled_idx]

        mn, mx = self.autoscale(series)
        self.draw_series_time(c, self.node.hist_t, series, colors, mn, mx)
        self.draw_legend(c, labels, colors)

    # ---------- Loop ----------
    def update_gui(self):
        # Texto en la unidad visual actual (J1..J4)
        pos = self.node.positions[:]
        sp  = self.node.setpoints[:]

        if self.angle_mode.get() == "deg":
            pos_show = [math.degrees(p) if i<4 else p for i,p in enumerate(pos)]
            sp_show  = [math.degrees(x) if i<4 else x for i,x in enumerate(sp)]
        else:
            pos_show = pos[:]; sp_show = sp[:]

        err_show = [sp_show[i]-pos_show[i] for i in range(5)]

        self.lbl_state.config(
            text="pos: [" + ", ".join(f"{p:.3f}" for p in pos_show) + "] | " +
                 "sp: ["  + ", ".join(f"{s:.3f}" for s in sp_show ) + "] | " +
                 "err: [" + ", ".join(f"{e:.3f}" for e in err_show) + "]"
        )

        self.draw_sp_pos_panel()
        self.draw_err_panel()
        self.root.after(100, self.update_gui)  # 10 Hz

    def on_close(self):
        self.root.quit()
        self.root.destroy()

    def run(self):
        self.root.mainloop()


def main():
    rclpy.init()
    node = SliderNode()
    t = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
    t.start()
    try:
        gui = SliderGUI(node)
        gui.run()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
