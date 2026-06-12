#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time, threading
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os 
from xml.etree import ElementTree as ET 
import ament_index_python.packages 

import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from std_msgs.msg import String, Float32MultiArray
from sensor_msgs.msg import JointState

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt

JOINT_NAMES = ['J1 (rad)', 'J2 (rad)', 'J3 (rad)', 'J4 (rad)', 'J5 (mm)']
N_JOINTS = 5
MAX_HISTORY = 10000

# --- VERSION HARDCODEADA PARA CONFIRMACIÓN VISUAL ---
GUI_VERSION = "V10"

# ===================== utilidades y trayectorias =====================
def clamp(x, a, b): return a if x < a else b if x > b else x
def rad(x): return np.deg2rad(x)
def deg(x): return np.rad2deg(x)

def get_package_version(package_name):
    """Retorna la versión hardcodeada para asegurar la confirmación visual."""
    return GUI_VERSION

def ramp_traj(q0, qf, tf, t):
    """Rampa / Lineal: devuelve q, dq, ddq."""
    q = np.zeros_like(t, dtype=float)
    dq = np.zeros_like(t, dtype=float)
    ddq = np.zeros_like(t, dtype=float)
    if tf > 1e-6:
        dq_const = (qf - q0) / tf
        dq.fill(dq_const)
        q = q0 + dq_const * t
    return q, dq, ddq 

def vel_trapezoidal(q0, qf, dqmax, tf, tb, t):
    """Generador Trapezoidal del usuario"""
    # Adaptación para punto único
    if t < 0: return q0, 0, 0
    if t > tf: return qf, 0, 0
    
    q, dq, ddq = 0.0, 0.0, 0.0
    
    if t <= tb:
        q = q0 + 0.5 * (dqmax / tb) * t**2
        dq = (dqmax / tb) * t
        ddq = dqmax / tb
    elif t <= tf - tb:
        q = q0 - 0.5 * tb * dqmax + dqmax * t
        dq = dqmax
        ddq = 0.0
    else:
        q = qf - 0.5 * dqmax * (t - tf)**2 / tb
        dq = -dqmax / tb * (t - tf)
        ddq = -dqmax / tb
        
    return q, dq, ddq

# ------------------ Node Definition ------------------

class TrajNode(Node):
    def __init__(self):
        super().__init__('can_traj')
        self.pub_cmd = self.create_publisher(String, 'can_command', 100)
        
        # QoS coincidente con can_node
        q_state = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=50
        )
        # Cambiado a JointState para tener timestamp
        self.sub_state = self.create_subscription(JointState, 'joint_states', self.on_state, q_state)
        
        self.pos = np.zeros(N_JOINTS, dtype=float)
        self.vel = np.zeros(N_JOINTS, dtype=float)
        
        # Guardamos el tiempo del último mensaje para calcular dt real
        self.last_msg_time = 0.0
        self.new_data_available = False
        
        # Lock para evitar condiciones de carrera al leer/escribir datos compartidos
        self.data_lock = threading.Lock()

    def on_state(self, msg: JointState):
        # Extraer timestamp en segundos
        t_sec = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
        
        with self.data_lock:
            # Asumimos que el orden es [J1, J2, J3, J4, J5] como en can_node.py
            if len(msg.position) >= 5:
                self.pos[:] = msg.position[:5]
            if len(msg.velocity) >= 5:
                self.vel[:] = msg.velocity[:5]
            
            self.last_msg_time = t_sec
            self.new_data_available = True

    # --- helpers envío ---
    def send_A_all(self):
        for i in range(1, 6):
            self.pub_cmd.publish(String(data=f"A{i}"))

    def send_C_rot(self, idx, pos_rad, vel_rads):
        msg = String(data=f"C{idx}:{pos_rad:.4f},{vel_rads:.4f}")
        self.pub_cmd.publish(msg)
        # print(f"DEBUG: Sent {msg.data}")

    def send_C_pris(self, pos_mm):
        self.pub_cmd.publish(String(data=f"C5:{pos_mm}"))


class TrajGUI:
    def __init__(self, node: TrajNode):
        self.node = node
        
        # --- Imprimir versión al iniciar ---
        self.version = get_package_version('can_comm_pkg')
        print(f"--- CAN TRAJECTORY GUI V{self.version} INICIADA ---")
        
        self.root = tk.Tk(); self.root.title(f"V{self.version} - CAN Trajectory (OFFLINE MODE)") # Versión en el título
        
        # --- Estado ---
        self.mode_units = tk.StringVar(value="DEG") 
        self.gen_mode   = tk.StringVar(value="LSPB")
        self.dt_s       = tk.DoubleVar(value=0.01) # 100Hz for smoothness
        self.win_s      = tk.DoubleVar(value=30.0)
        self.deadband   = tk.DoubleVar(value=0.0)
        self.view_joint = tk.StringVar(value="Seleccionados")
        self.poll_dt_s  = tk.DoubleVar(value=0.01) # 100Hz for smoother recording
        self.safe_poll_dt = 0.01
        self.poll_dt_s.trace_add("write", lambda *args: setattr(self, 'safe_poll_dt', self._get_safe_float(self.poll_dt_s, 0.01)))
        
        self.auto_pause = tk.BooleanVar(value=True) # ALWAYS TRUE for Offline Mode
        self.blend_T    = tk.DoubleVar(value=0.5)
        self.max_vel    = tk.DoubleVar(value=10.0) 
        
        # Ring Buffer Initialization
        self.buf_size = MAX_HISTORY
        self.buf_idx = 0
        self.buf_len = 0
        
        self.t_buf = np.zeros(self.buf_size)
        self.q_sp_buf = np.zeros((self.buf_size, N_JOINTS))
        self.q_pos_buf = np.zeros((self.buf_size, N_JOINTS))
        self.dq_sp_buf = np.zeros((self.buf_size, N_JOINTS))
        self.dq_vel_buf = np.zeros((self.buf_size, N_JOINTS))
        self.ddq_sp_buf = np.zeros((self.buf_size, N_JOINTS))
        self.ddq_accel_buf = np.zeros((self.buf_size, N_JOINTS))

        self._t0 = time.time()
        
        self.last_sp = np.zeros(N_JOINTS, dtype=float) 
        self._running = False
        self._polling = True
        self._paused = False 
        
        # Para el cálculo de aceleración basado en tiempo real
        self.prev_msg_time = None
        self.prev_vel_for_accel = np.zeros(N_JOINTS)

        self.targets = [tk.DoubleVar(value=0.0) for _ in range(N_JOINTS)]
        self.Ts      = [tk.DoubleVar(value=3.0)  for _ in range(N_JOINTS)]
        self.sel     = [tk.BooleanVar(value=(i==0)) for i in range(N_JOINTS)]
        
        self.traj_plan = None 
        self.traj_idx = 0
        self.traj_t0 = 0.0 # Time when trajectory started
        self.traj_dt = 0.01 # dt used for planning
        self.traj_funcs = {"rampa": ramp_traj, "LSPB": vel_trapezoidal}
        self.last_vel_for_accel_calc = np.zeros(N_JOINTS)
        
        self.plot_counter = 0 # Counter for lazy autoscaling
        
        self._reset_history() 

        self._build_ui()
        # self._build_plot() # REMOVED: Plot is now in a separate window
        # self._update_visibility(rebuild=True) # Not needed here anymore

        # Iniciar hilos
        threading.Thread(target=self._poll_A_loop, daemon=True).start()
        
        # CRITICAL FIX: Start ROS spinning in a background thread
        threading.Thread(target=lambda: rclpy.spin(self.node), daemon=True).start()
        
        self._recording = True
        # Start threaded recorder
        threading.Thread(target=self._threaded_data_recorder, daemon=True).start()
        
        self._status_checker()
        self.plot_after_id = None

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.mainloop()

    def _get_safe_float(self, var, default):
        try:
            return float(var.get())
        except:
            return default



    # ---------- UI ----------
    def _build_ui(self):
        # Main Container for Centering
        main_container = ttk.Frame(self.root)
        main_container.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Inner Frame for content (Centered)
        content_frame = ttk.Frame(main_container)
        content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        top = ttk.Frame(content_frame, padding=6); top.pack(side=tk.TOP, fill=tk.X)

        # Fila 1: Controles de unidades y modo
        f1 = ttk.Frame(top); f1.pack(side=tk.TOP, fill=tk.X)
        ttk.Label(f1, text="Unidades:").pack(side=tk.LEFT)
        self.cmb_units = ttk.OptionMenu(f1, self.mode_units, self.mode_units.get(), "RAD", "DEG", command=lambda e: self._update_plot(True))
        self.cmb_units.pack(side=tk.LEFT, padx=4)

        ttk.Label(f1, text="Generador:").pack(side=tk.LEFT, padx=(12,2))
        # Usar OptionMenu con command para actualizar UI
        self.cmb_gen = ttk.OptionMenu(f1, self.gen_mode, self.gen_mode.get(), "rampa", "escalon", "LSPB", command=self._on_gen_mode_change)
        self.cmb_gen.pack(side=tk.LEFT, padx=4)
        
        # Botón de Info
        ttk.Button(f1, text="ℹ️", width=3, command=self._show_mode_info).pack(side=tk.LEFT, padx=2)

        # Frame dinámico para parámetros
        self.f_params = ttk.Frame(top); self.f_params.pack(side=tk.TOP, fill=tk.X, pady=2)
        
        # Widgets para Rampa/General
        self.lbl_dt = ttk.Label(self.f_params, text="dt [s]:")
        self.ent_dt = ttk.Entry(self.f_params, textvariable=self.dt_s, width=6)
        self.lbl_win = ttk.Label(self.f_params, text="Ventana [s]:")
        self.ent_win = ttk.Entry(self.f_params, textvariable=self.win_s, width=6)
        self.lbl_db = ttk.Label(self.f_params, text="deadband:")
        self.ent_db = ttk.Entry(self.f_params, textvariable=self.deadband, width=6)
        
        # Widgets para LSPB
        self.lbl_blend = ttk.Label(self.f_params, text="Blend T [s]:")
        self.ent_blend = ttk.Entry(self.f_params, textvariable=self.blend_T, width=6)
        self.lbl_maxvel = ttk.Label(self.f_params, text="Max Vel [u/s]:")
        self.ent_maxvel = ttk.Entry(self.f_params, textvariable=self.max_vel, width=6)

        # Fila 2: Plot y Acciones
        f2 = ttk.Frame(top); f2.pack(side=tk.TOP, fill=tk.X)

        ttk.Label(f2, text="Ver:").pack(side=tk.LEFT, padx=(0,2))
        cmb = ttk.Combobox(f2, textvariable=self.view_joint, state="readonly", width=13,
                           values=["Seleccionados","Todos","J1","J2","J3","J4","J5"])
        cmb.pack(side=tk.LEFT, padx=4)
        cmb.bind("<<ComboboxSelected>>", lambda e: self._update_visibility(rebuild=True))

        ttk.Button(f2, text="Iniciar", command=self._start).pack(side=tk.LEFT, padx=(16,4))
        self.btn_pause = ttk.Button(f2, text="Pausar Gráfico", command=self._toggle_pause)
        self.btn_pause.pack(side=tk.LEFT)
        ttk.Button(f2, text="Detener", command=self._stop).pack(side=tk.LEFT, padx=(4,0))
        ttk.Button(f2, text="Reset Hist. & Gráfico", command=self._reset_and_redraw).pack(side=tk.LEFT, padx=8)
        ttk.Button(f2, text="Grabar (Gráfica + Datos)", command=self._save_all).pack(side=tk.LEFT)
        ttk.Button(f2, text="Calcular Métricas", command=self._calc_metrics).pack(side=tk.LEFT, padx=8)
        
        # Checkbox Auto-Pause REMOVED for Offline Mode
        # ttk.Checkbutton(f2, text="Priorizar Control", variable=self.auto_pause).pack(side=tk.LEFT, padx=4)
        
        # Botón Cerrar (Rojo oscuro para destacar)
        style = ttk.Style()
        style.configure("Red.TButton", foreground="red")
        ttk.Button(f2, text="Cerrar", command=self._on_close, style="Red.TButton").pack(side=tk.RIGHT, padx=4)
        
        # Inicializar estado UI
        self._on_gen_mode_change(self.gen_mode.get())


        # Fila 3: Sondeo y Tabla
        f3 = ttk.Frame(content_frame, padding=(6,2)); f3.pack(side=tk.TOP, fill=tk.X)
        ttk.Label(f3, text="Sondeo A# [s]:").pack(side=tk.LEFT, padx=(0,2))
        ttk.Entry(f3, textvariable=self.poll_dt_s, width=6).pack(side=tk.LEFT)

        grid = ttk.Frame(content_frame, padding=(6,2)); grid.pack(side=tk.TOP, fill=tk.X)
        hdr = ["Usar", "Joint", "Target (rad/mm o deg*)", "T total [s]"]
        for c,h in enumerate(hdr):
            ttk.Label(grid, text=h, font=("TkDefaultFont",9,"bold")).grid(row=0,column=c,padx=4,pady=2,sticky='w')
        for i in range(N_JOINTS):
            ttk.Checkbutton(grid, variable=self.sel[i], command=lambda: self._update_visibility(rebuild=True))\
                .grid(row=i+1, column=0, padx=4)
            ttk.Label(grid, text=JOINT_NAMES[i]).grid(row=i+1, column=1, padx=4, sticky='w')
            ttk.Entry(grid, textvariable=self.targets[i], width=12).grid(row=i+1, column=2, padx=4)
            ttk.Entry(grid, textvariable=self.Ts[i], width=8).grid(row=i+1, column=3, padx=4)

        ttk.Label(content_frame, text="* Si eliges DEG, introduce objetivos en grados; internamente se convierten a rad. J5 siempre en mm.", foreground="#555").pack(side=tk.TOP, anchor='w', padx=8, pady=(2,6))

    def _on_gen_mode_change(self, mode):
        # Limpiar fila de parámetros
        for widget in self.f_params.winfo_children():
            widget.pack_forget()
            
        # Siempre mostrar dt, window, deadband (útiles para todos o casi todos)
        self.lbl_dt.pack(side=tk.LEFT, padx=(0,2))
        self.ent_dt.pack(side=tk.LEFT)
        self.lbl_win.pack(side=tk.LEFT, padx=(12,2))
        self.ent_win.pack(side=tk.LEFT)
        self.lbl_db.pack(side=tk.LEFT, padx=(12,2))
        self.ent_db.pack(side=tk.LEFT)
        
        if mode == "LSPB":
            self.lbl_blend.pack(side=tk.LEFT, padx=(12,2))
            self.ent_blend.pack(side=tk.LEFT)
            self.lbl_maxvel.pack(side=tk.LEFT, padx=(12,2))
            self.ent_maxvel.pack(side=tk.LEFT)
            
    def _show_mode_info(self):
        mode = self.gen_mode.get()
        info = ""
        if mode == "rampa":
            info = "RAMPA LINEAL:\n\nMueve las articulaciones a velocidad constante desde el inicio hasta el fin.\n\nParámetros:\n- T total: Tiempo de duración del movimiento."
        elif mode == "escalon":
            info = "ESCALÓN (STEP):\n\nEnvía el comando de posición final inmediatamente.\n¡Cuidado! Puede causar movimientos bruscos si el error es grande."
        elif mode == "LSPB":
            info = "LSPB (Linear Segment with Parabolic Blend):\n\nTrayectoria suave con aceleración y desaceleración parabólica y un tramo central de velocidad constante.\n\nParámetros:\n- Blend T: Tiempo de aceleración/desaceleración.\n- Max Vel: Velocidad máxima permitida en el tramo central."
            
        messagebox.showinfo(f"Info: {mode.upper()}", info)

    # ---------- Plotting y Conversión de Unidades ----------
    # ---------- Plotting y Conversión de Unidades ----------
    # ---------- Plotting y Conversión de Unidades ----------
    def _show_results_window(self):
        """Abre una ventana nueva con los resultados gráficos (NATIVE MATPLOTLIB)."""
        
        # Apply Style
        plt.style.use('ggplot')
        
        # --- Figure ---
        fig, (ax_q, ax_dq, ax_ddq) = plt.subplots(3, 1, figsize=(10, 8), sharex=True, constrained_layout=True)
        fig.canvas.manager.set_window_title(f"Resultados de Trayectoria - {datetime.now().strftime('%H:%M:%S')}")
        
        ax_q.set_title("Posición y Error"); ax_dq.set_title("Velocidad y Error"); ax_ddq.set_title("Aceleración y Error")
        ax_ddq.set_xlabel("Tiempo [s]")
        
        # --- Plot Data ---
        if self.buf_len > 0:
            idxs = (np.arange(self.buf_len) + self.buf_idx - self.buf_len) % self.buf_size
            t = self.t_buf[idxs]
            
            # Convert units
            q_sp_arr = self._apply_unit_conversion(self.q_sp_buf[idxs])
            q_pos_arr = self._apply_unit_conversion(self.q_pos_buf[idxs])
            dq_sp_arr = self._apply_unit_conversion(self.dq_sp_buf[idxs])
            dq_vel_arr = self._apply_unit_conversion(self.dq_vel_buf[idxs])
            ddq_sp_arr = self._apply_unit_conversion(self.ddq_sp_buf[idxs])
            # ddq_accel_arr = self._apply_unit_conversion(self.ddq_accel_buf[idxs]) # We will recalc this

            # --- SMOOTHING & FILTERING (Ported from j4_performance_test) ---
            def robust_diff(y, t, window=5):
                n = len(y)
                dy = np.zeros(n)
                for i in range(n):
                    i_min = max(0, i - window)
                    i_max = min(n - 1, i + window)
                    if i_max == i_min: continue
                    dt_w = t[i_max] - t[i_min]
                    if dt_w > 1e-6:
                        dy[i] = (y[i_max] - y[i_min]) / dt_w
                return dy

            def smooth(y, alpha=0.3):
                res = np.zeros_like(y)
                if len(y) == 0: return res
                val = y[0]
                for i in range(len(y)):
                    val = val * (1.0 - alpha) + y[i] * alpha
                    res[i] = val
                return res

            # Apply smoothing per joint
            ddq_accel_arr = np.zeros_like(dq_vel_arr)
            
            for j in range(N_JOINTS):
                # 1. Smooth Velocity
                dq_vel_arr[:, j] = smooth(dq_vel_arr[:, j], alpha=0.3)
                
                # 2. Calculate Acceleration from Smoothed Velocity (Robust Diff)
                # Note: We use the smoothed velocity to get a cleaner acceleration derivative
                ddq_accel_arr[:, j] = robust_diff(dq_vel_arr[:, j], t, window=4)
                
                # 3. Smooth Acceleration
                ddq_accel_arr[:, j] = smooth(ddq_accel_arr[:, j], alpha=0.1)

            # Calculate Errors
            q_err_arr = q_sp_arr - q_pos_arr
            dq_err_arr = dq_sp_arr - dq_vel_arr
            ddq_err_arr = ddq_sp_arr - ddq_accel_arr
            
            colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
            
            for j in range(N_JOINTS):
                if not self.sel[j].get() and self.view_joint.get() == "Seleccionados": continue
                if self.view_joint.get() != "Todos" and self.view_joint.get() != "Seleccionados" and self.view_joint.get() != f"J{j+1}": continue

                c = colors[j % len(colors)]
                name = f"J{j+1}"
                
                ax_q.plot(t, q_sp_arr[:, j], label=f"{name} SP", color=c, linestyle='-')
                ax_q.plot(t, q_pos_arr[:, j], label=f"{name} Medido", color=c, linestyle='--')
                ax_q.plot(t, q_err_arr[:, j], label=f"{name} Error", color=c, linestyle=':', alpha=0.7)
                
                ax_dq.plot(t, dq_sp_arr[:, j], label=f"{name} SP", color=c, linestyle='-')
                ax_dq.plot(t, dq_vel_arr[:, j], label=f"{name} Medido", color=c, linestyle='--')
                ax_dq.plot(t, dq_err_arr[:, j], label=f"{name} Error", color=c, linestyle=':', alpha=0.7)
                
                ax_ddq.plot(t, ddq_sp_arr[:, j], label=f"{name} SP", color=c, linestyle='-')
                ax_ddq.plot(t, ddq_accel_arr[:, j], label=f"{name} Medido", color=c, linestyle='--')
                ax_ddq.plot(t, ddq_err_arr[:, j], label=f"{name} Error", color=c, linestyle=':', alpha=0.7)

        # Labels
        units = self.mode_units.get()
        pos_unit = units if units == "RAD" else "°"
        ax_q.set_ylabel(f"Pos [{pos_unit}] / [mm]")
        ax_dq.set_ylabel(f"Vel [{pos_unit}/s] / [mm/s]")
        ax_ddq.set_ylabel(f"Acc [{pos_unit}/s²] / [mm/s²]")
        
        for ax in (ax_q, ax_dq, ax_ddq):
            ax.grid(True, linestyle=':', alpha=0.6)
            ax.legend(ncol=3, fontsize=8, loc='upper right')

        # Native Show
        plt.show()


    def _status_checker(self):
        try:
            # Check if running state changed from True to False
            if hasattr(self, '_was_running') and self._was_running and not self._running:
                # Finished! Show results
                self.root.after(100, self._show_results_window)
            
            self._was_running = self._running
            
            # Keep checking
            self.plot_after_id = self.root.after(200, self._status_checker) 
        except Exception as e:
            print(f"Error in status checker: {e}")
            self.plot_after_id = self.root.after(500, self._status_checker)

    def _on_plot_hover(self, event):
        if event.inaxes in self.annots:
            ax = event.inaxes
            annot = self.annots[ax]
            found = False
            
            # Hide other annotations
            for other_ax, other_annot in self.annots.items():
                if other_ax != ax and other_annot.get_visible():
                    other_annot.set_visible(False)
                    self.fig.canvas.draw_idle()

            for line in ax.get_lines():
                if not line.get_visible(): continue # Ignore hidden lines
                if line.contains(event)[0]:
                    x, y = event.xdata, event.ydata
                    annot.xy = (x, y)
                    text = f"{line.get_label()}: {y:.3f}"
                    annot.set_text(text)
                    annot.set_visible(True)
                    self.fig.canvas.draw_idle()
                    found = True
                    break
            
            if not found and annot.get_visible():
                annot.set_visible(False)
                self.fig.canvas.draw_idle()


    def _set_ylabels(self):
        units = self.mode_units.get()
        pos_unit = units if units == "RAD" else "°"
        vel_unit = f"{pos_unit}/s"
        accel_unit = f"{pos_unit}/s²"
        
        self.ax_q.set_ylabel(f"Posición [{pos_unit}] / [mm]")
        self.ax_dq.set_ylabel(f"Velocidad [{vel_unit}] / [mm/s]")
        self.ax_ddq.set_ylabel(f"Aceleración [{accel_unit}] / [mm/s²]")


    def _apply_unit_conversion(self, data_list):
        # Fix: Check len() explicitly to avoid "The truth value of an array is ambiguous"
        if self.mode_units.get() != "DEG" or len(data_list) == 0:
            return np.array(data_list)
        
        data_array = np.array(data_list)
        
        if data_array.ndim == 2:
            data_array[:, :4] = np.rad2deg(data_array[:, :4])
        elif data_array.ndim == 1 and data_array.size >= 4:
            data_array[:4] = np.rad2deg(data_array[:4])
            
        return data_array


    def _update_plot(self, units_changed=False):
        if self.buf_len == 0 or self._paused: 
            if units_changed: self._set_ylabels()
            return
        
        # 1. Obtener índices ordenados cronológicamente
        idxs = (np.arange(self.buf_len) + self.buf_idx - self.buf_len) % self.buf_size
        
        # 2. Filtrar por ventana de tiempo
        t_latest = self.t_buf[idxs[-1]]
        win = float(self.win_s.get())
        
        # Optimización: búsqueda binaria o simple slicing si asumimos monotonía, 
        # pero con ring buffer es más seguro usar máscara o buscar el punto de corte.
        # Dado que t es monótono, el corte es simple.
        # Sin embargo, para simplicidad y robustez (y dado que numpy es rápido):
        valid_mask = self.t_buf[idxs] > (t_latest - win)
        idxs = idxs[valid_mask]
        
        if len(idxs) == 0: return

        # 3. Decimation (Dynamic: Fast Mode vs High Res)
        step = 1
        n_points = len(idxs)
        
        # FAST MODE: If running, downsample heavily to save CPU
        if self._running:
            target_points = 200 # Reduced from 300 for better performance
        else:
            target_points = self.buf_size # SHOW ALL POINTS (Max Quality) when stopped
            
        if n_points > target_points:
            step = n_points // target_points + 1
        
        idxs = idxs[::step]
        
        t = self.t_buf[idxs]
        
        # 4. Convertir y calcular errores
        q_sp_arr = self._apply_unit_conversion(self.q_sp_buf[idxs])
        q_pos_arr = self._apply_unit_conversion(self.q_pos_buf[idxs])
        dq_sp_arr = self._apply_unit_conversion(self.dq_sp_buf[idxs])
        dq_vel_arr = self._apply_unit_conversion(self.dq_vel_buf[idxs])
        ddq_sp_arr = self._apply_unit_conversion(self.ddq_sp_buf[idxs])
        ddq_accel_arr = self._apply_unit_conversion(self.ddq_accel_buf[idxs])
        
        q_err_arr = q_sp_arr - q_pos_arr
        dq_err_arr = dq_sp_arr - dq_vel_arr
        ddq_err_arr = ddq_sp_arr - ddq_accel_arr

        # 3. Actualizar Plots
        for j in range(N_JOINTS):
            # Posición (SP, Medido, Error)
            q_lines = self.lines_q[j*3:(j+1)*3]
            q_lines[0].set_data(t, q_sp_arr[:, j]); q_lines[1].set_data(t, q_pos_arr[:, j]); q_lines[2].set_data(t, q_err_arr[:, j])
            # Velocidad (SP, Medido, Error)
            dq_lines = self.lines_dq[j*3:(j+1)*3]
            dq_lines[0].set_data(t, dq_sp_arr[:, j]); dq_lines[1].set_data(t, dq_vel_arr[:, j]); dq_lines[2].set_data(t, dq_err_arr[:, j])
            # Aceleración (SP, Medido, Error)
            ddq_lines = self.lines_ddq[j*3:(j+1)*3]
            ddq_lines[0].set_data(t, ddq_sp_arr[:, j]); ddq_lines[1].set_data(t, ddq_accel_arr[:, j]); ddq_lines[2].set_data(t, ddq_err_arr[:, j])
            
        # 4. Actualizar límites de ejes y labels
        self._set_ylabels()
        self._update_visibility()
        
        # Fast X Update
        t_latest = t[-1]
        t_min = t_latest - win
        
        # Lazy Y Autoscale (every 5th frame, BUT ONLY IF NOT RUNNING)
        # When running, we avoid autoscaling to save massive CPU
        # do_autoscale = (not self._running) and (self.plot_counter % 5 == 0)
        
        # FIX: Stabilized Autoscaling
        if self._running:
            # Update X axis always
            for ax in (self.ax_q, self.ax_dq, self.ax_ddq):
                ax.set_xlim(t_min, t_latest + win * 0.02)
            
            # Update Y axis with hysteresis (every 10 frames)
            if self.plot_counter % 10 == 0:
                for ax in (self.ax_q, self.ax_dq, self.ax_ddq):
                    # Get data limits
                    dmin, dmax = float('inf'), float('-inf')
                    has_data = False
                    for line in ax.get_lines():
                        if not line.get_visible(): continue
                        y = line.get_ydata()
                        if len(y) > 0:
                            dmin = min(dmin, np.min(y))
                            dmax = max(dmax, np.max(y))
                            has_data = True
                    
                    if not has_data: continue
                    
                    # Current limits
                    ymin, ymax = ax.get_ylim()
                    h = ymax - ymin
                    
                    # Expand if needed
                    margin = 0.1 * (dmax - dmin) if dmax != dmin else 1.0
                    req_min = dmin - margin
                    req_max = dmax + margin
                    
                    if req_min < ymin or req_max > ymax:
                        ax.set_ylim(min(req_min, ymin), max(req_max, ymax))
                    # Contract only if significant (hysteresis)
                    elif (req_max - req_min) < 0.7 * h:
                        ax.set_ylim(req_min, req_max)

        else:
            # Stopped mode: Standard autoscale
            for ax in (self.ax_q, self.ax_dq, self.ax_ddq):
                ax.set_xlim(t_min, t_latest + win * 0.02)
                ax.grid(True, linestyle=':', alpha=0.6)
                if self.plot_counter % 5 == 0:
                    ax.relim()
                    ax.autoscale_view(scalex=False, scaley=True)
            
        self.plot_counter += 1
        self.canvas.draw_idle()

    # --- Visibilidad, Historial, Guardar ---
    def _visible_for_joint(self, j):
        v = self.view_joint.get()
        if v == "Todos": return True
        if v == "Seleccionados": return bool(self.sel[j].get())
        return v == f"J{j+1}"

    def _rebuild_legends(self):
        for ax, all_lines in zip([self.ax_q, self.ax_dq, self.ax_ddq], [self.lines_q, self.lines_dq, self.lines_ddq]):
            handles = []
            labels = []
            
            for line in all_lines:
                if line.get_visible():
                    handles.append(line)
                    labels.append(line.get_label()) 

            if handles:
                ax.legend(handles, labels, ncol=3, fontsize=8, loc='upper right')
            else:
                if ax.get_legend(): ax.get_legend().remove()

        self.canvas.draw_idle()

    def _update_visibility(self, rebuild=False):
        # No-op for offline mode as there are no live lines to hide/show
        pass

    def _save_data_to_file(self, fpath):
        if self.buf_len == 0: return

        idxs = (np.arange(self.buf_len) + self.buf_idx - self.buf_len) % self.buf_size
        
        headers = ['t']
        data_cols = [self.t_buf[idxs]]
        
        q_sp_all = self._apply_unit_conversion(self.q_sp_buf[idxs])
        q_pos_all = self._apply_unit_conversion(self.q_pos_buf[idxs])
        dq_sp_all = self._apply_unit_conversion(self.dq_sp_buf[idxs])
        dq_vel_all = self._apply_unit_conversion(self.dq_vel_buf[idxs])
        ddq_sp_all = self._apply_unit_conversion(self.ddq_sp_buf[idxs])
        ddq_acc_all = self._apply_unit_conversion(self.ddq_accel_buf[idxs])

        for j in range(N_JOINTS):
            name = f"J{j+1}"
            headers.extend([f'{name}_q_sp', f'{name}_q_pos', f'{name}_dq_sp', f'{name}_dq_vel', f'{name}_ddq_sp', f'{name}_ddq_acc'])
            data_cols.extend([q_sp_all[:, j], q_pos_all[:, j], dq_sp_all[:, j], dq_vel_all[:, j], ddq_sp_all[:, j], ddq_acc_all[:, j]])

        data_matrix = np.column_stack(data_cols)
        header_line = ",".join(headers)
        np.savetxt(fpath, data_matrix, fmt='%.6f', delimiter=',', header=header_line, comments='')


    def _save_all(self):
        SAVE_DIR = "robot_data/traj_plots"
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)
            
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 1. Guardar Gráfica (PDF y SVG)
        plot_base_name = os.path.join(SAVE_DIR, f"traj_plot_{ts}")
        
        try:
            self.fig.savefig(f"{plot_base_name}.pdf", dpi=300, bbox_inches='tight')
            pdf_saved = True
        except Exception as e:
            pdf_saved = False
            
        try:
            self.fig.savefig(f"{plot_base_name}.svg", dpi=300, bbox_inches='tight')
            svg_saved = True
        except Exception as e:
            svg_saved = False

        # 2. Guardar Datos (CSV)
        data_path = os.path.join(SAVE_DIR, f"traj_data_{ts}.csv")
        try:
            self._save_data_to_file(data_path)
            data_saved = True
        except Exception as e:
            data_saved = False
        
        # 3. Notificación
        msg = f"Guardado completado en la carpeta '{SAVE_DIR}':\n"
        msg += f"- Gráfico PDF: {'ÉXITO' if pdf_saved else 'FALLÓ'}\n"
        msg += f"- Gráfico SVG: {'ÉXITO' if svg_saved else 'FALLÓ'}\n"
        msg += f"- Datos CSV: {'ÉXITO' if data_saved else 'FALLÓ'}"
        msg += f"- Datos CSV: {'ÉXITO' if data_saved else 'FALLÓ'}"
        messagebox.showinfo("Guardado Automático", msg)


    def _calc_metrics(self):
        """Calcula % Overshoot y Settling Time (Ts) para los joints seleccionados."""
        if self.buf_len < 10:
            messagebox.showwarning("Métricas", "No hay suficientes datos para calcular métricas.")
            return

        idxs = (np.arange(self.buf_len) + self.buf_idx - self.buf_len) % self.buf_size
        t = self.t_buf[idxs]
        
        # Convertir a unidades visuales actuales (DEG/RAD)
        q_pos_arr = self._apply_unit_conversion(self.q_pos_buf[idxs])
        q_sp_arr  = self._apply_unit_conversion(self.q_sp_buf[idxs])

        report = "Métricas de Respuesta (Última ventana):\n\n"
        
        for j in range(N_JOINTS):
            if not self.sel[j].get():
                continue
                
            name = JOINT_NAMES[j]
            y = q_pos_arr[:, j]
            sp = q_sp_arr[:, j]
            
            # 1. Valor Final (Steady State) - Promedio de los últimos 10% de datos
            n_tail = max(5, int(len(y) * 0.1))
            y_ss = np.mean(y[-n_tail:])
            sp_final = sp[-1]
            
            # Si el setpoint es 0, el %OS no tiene sentido matemático estándar (división por cero)
            # Usaremos una referencia absoluta si sp es muy pequeño
            ref_val = y_ss if abs(y_ss) > 1e-3 else 1.0
            
            # 2. Peak Value
            y_max = np.max(y)
            y_min = np.min(y)
            
            # Detectar dirección del escalón (subida o bajada)
            # Simplificación: asumimos subida si y_ss > y[0], bajada si y_ss < y[0]
            if y_ss > y[0]:
                peak = y_max
                overshoot = (peak - y_ss) / abs(ref_val) * 100.0
            else:
                peak = y_min
                overshoot = (y_ss - peak) / abs(ref_val) * 100.0
            
            # Overshoot no puede ser negativo por definición en control clásico (si no llega, es 0%)
            overshoot = max(0.0, overshoot)

            # 3. Settling Time (2% criterion)
            # Tiempo desde que entra en la banda del 2% y NO vuelve a salir
            band = 0.02 * abs(y_ss)
            upper = y_ss + band
            lower = y_ss - band
            
            ts = 0.0
            # Recorremos hacia atrás para encontrar cuándo entró por última vez
            for i in range(len(y)-1, -1, -1):
                if y[i] > upper or y[i] < lower:
                    # Salió de la banda en el índice i
                    # Entonces entró en i+1
                    if i < len(y) - 1:
                        ts = t[i+1] - t[0] # Tiempo relativo al inicio de la ventana
                    else:
                        ts = -1.0 # Nunca se asentó
                    break
            else:
                # Si llega aquí, nunca salió de la banda (siempre estuvo dentro??)
                ts = 0.0

            report += f"[{name}]\n"
            report += f"  Final: {y_ss:.3f}\n"
            report += f"  %OS:   {overshoot:.2f}%\n"
            report += f"  Ts:    {ts:.3f} s (crit. 2%)\n"
            report += "-"*20 + "\n"

        messagebox.showinfo("Resultados de Métricas", report)


    def _reset_history(self):
        self.buf_idx = 0
        self.buf_len = 0
        self._t0 = time.time()
        
        self.prev_msg_time = None
        self.prev_vel_for_accel = np.zeros(N_JOINTS)

        # Inicializar historial con el estado actual del nodo
        current_pos = self.node.pos.copy()
        current_vel = self.node.vel.copy()
        
        self._push_history(0.0, current_pos, np.zeros(N_JOINTS), np.zeros(N_JOINTS), 
                        current_pos, current_vel, np.zeros(N_JOINTS))


    def _reset_and_redraw(self):
        self._reset_history()
        for lines in [self.lines_q, self.lines_dq, self.lines_ddq]:
            for ln in lines: ln.set_data([], [])
        self._rebuild_legends()

    # ---------- Bucle de Datos ----------
    # ---------- Bucle de Datos ----------
    def _push_history(self, t, q_sp, dq_sp, ddq_sp, q_pos, dq_vel, accel_m):
        
        idx = self.buf_idx
        
        self.t_buf[idx] = float(t)
        self.q_sp_buf[idx] = q_sp
        self.q_pos_buf[idx] = q_pos
        self.dq_sp_buf[idx] = dq_sp
        self.dq_vel_buf[idx] = dq_vel
        self.ddq_sp_buf[idx] = ddq_sp
        self.ddq_accel_buf[idx] = accel_m
        
        self.buf_idx = (self.buf_idx + 1) % self.buf_size
        self.buf_len = min(self.buf_len + 1, self.buf_size)


    def _toggle_pause(self):
        """Pausa o reanuda la actualización de los gráficos."""
        self._paused = not self._paused
        if self._paused:
            self.btn_pause.config(text="Reanudar Gráfico")
        else:
            self.btn_pause.config(text="Pausar Gráfico")


    def _threaded_data_recorder(self):
        """High frequency threaded loop for recording data (Precision Timing)"""
        t_next = time.perf_counter()
        stale_count = 0
        stale_count = 0
        total_count = 0
        
        # Filters
        self.filt_vel = np.zeros(N_JOINTS)
        self.filt_acc = np.zeros(N_JOINTS)
        alpha_v = 0.1 # Lower alpha for smoother velocity
        alpha_a = 0.05
        
        # Velocity Calculation State
        self.prev_pos_for_vel = None
        self.prev_time_for_vel = None
        
        while self._recording:
            try:
                # FIX: Record continuously to keep graph alive
                # if not self._running:
                #     time.sleep(0.1)
                #     continue

                dt = self.safe_poll_dt
                if dt <= 0.001: dt = 0.01 # Safety clamp
                
                now = time.time()
                t_current = now - self._t0
                
                # Logic to get setpoints
                q_sp, dq_sp, ddq_sp = self.last_sp.copy(), np.zeros(N_JOINTS), np.zeros(N_JOINTS)
                
                if self._running and self.traj_plan:
                    # Sample the trajectory plan based on EXACT time elapsed
                    # This decouples recording from the generator loop frequency/jitter
                    elapsed = time.perf_counter() - self.traj_t0
                    if elapsed < 0: elapsed = 0
                    
                    # Use the dt that was used to generate the plan
                    idx = int(elapsed / self.traj_dt)
                    
                    # Clamp index
                    q_plan, dq_plan, ddq_plan = self.traj_plan
                    if idx >= len(q_plan):
                        idx = len(q_plan) - 1
                        
                    q_sp, dq_sp, ddq_sp = q_plan[idx], dq_plan[idx], ddq_plan[idx]
                
                # Logic to get measured state
                with self.node.data_lock:
                    curr_pos = self.node.pos.copy()
                    raw_vel = self.node.vel.copy()
                    curr_time = self.node.last_msg_time
                    new_data = self.node.new_data_available
                    self.node.new_data_available = False
                
                # FIX: Use raw encoder velocity
                curr_vel = raw_vel.copy()
                
                # self.prev_pos_for_vel = curr_pos.copy() # Not needed anymore
                # self.prev_time_for_vel = curr_time

                # Filter Velocity (Optional, but user liked raw data, so we skip filtering for now or keep it light)
                # self.filt_vel = self.filt_vel * (1.0 - alpha_v) + curr_vel * alpha_v
                # curr_vel = self.filt_vel.copy()
                # Using RAW velocity as requested
                pass
                
                # Debug Stale Data (Disabled to reduce spam)
                # total_count += 1
                # if not new_data:
                #     stale_count += 1
                
                # if total_count % 100 == 0:
                #     ratio = stale_count / total_count * 100
                #     print(f"Recorder Stats: Stale Data: {ratio:.1f}% (Freq: {1/dt:.1f}Hz)")
                #     stale_count = 0
                #     total_count = 0
                
                # Calculate acceleration
                
                # Calculate acceleration
                accel_m = np.zeros(N_JOINTS)
                if new_data and self.prev_msg_time is not None:
                    dt_real = curr_time - self.prev_msg_time
                    if dt_real > 1e-6:
                        raw_acc = (curr_vel - self.prev_vel_for_accel) / dt_real
                        self.filt_acc = self.filt_acc * (1.0 - alpha_a) + raw_acc * alpha_a
                        accel_m = self.filt_acc.copy()
                
                self.prev_msg_time = curr_time
                self.prev_vel_for_accel = curr_vel.copy()

                self._push_history(t_current, q_sp, dq_sp, ddq_sp, curr_pos, curr_vel, accel_m)
                
                # Drift-corrected sleep
                t_next += dt
                sleep_time = t_next - time.perf_counter()
                if sleep_time > 0:
                    time.sleep(sleep_time)
                else:
                    t_next = time.perf_counter() # Reset if lagging
            except Exception as e:
                print(f"Error in threaded recorder: {e}")
                time.sleep(0.1)

    # Removed _plot_updater as it is replaced by _status_checker and _show_results_window


    # ---------- Generación y Envío (Lógica del Control) ----------
    def _start(self):
        if self._running: return
        
        # No need to hide plot frame as it is not there anymore
        # self.plot_frame.pack_forget()
        
        # FIX: Reset history before starting a new run
        # self._reset_history()
        
        dt = max(0.005, float(self.dt_s.get()))
        tgs = np.zeros(N_JOINTS, dtype=float)
        
        for j in range(4):
            v = float(self.targets[j].get())
            if self.mode_units.get() == "DEG": v = np.deg2rad(v)
            tgs[j] = v
        tgs[4] = float(self.targets[4].get()) 
        
        # FIX: Leer la posición actual desde el nodo ROS
        cur = np.copy(self.node.pos)
        
        # FIX: Si no hay datos de ROS (todo ceros) y tenemos historial, usar el buffer
        if not cur.any() and self.buf_len > 0:
            idx = (self.buf_idx - 1) % self.buf_size
            cur = self.q_pos_buf[idx].copy()
        elif not cur.any() and self.buf_len == 0:
            print("ADVERTENCIA: No hay datos de posición del robot ni historial. Usando ceros como inicio.")
            # Opcional: Podríamos mostrar un messagebox aquí
            # messagebox.showwarning("Advertencia", "No se ha recibido posición del robot. Se asume inicio en 0.")

        db = float(self.deadband.get())
        for j in range(N_JOINTS):
            if abs(tgs[j] - cur[j]) < db: tgs[j] = cur[j]
        
        self.last_sp = cur.copy() 
        
        print(f"--- START TRAJECTORY ---")
        print(f"Current Pos (q0): {cur}")
        print(f"Target Pos (qf):  {tgs}")
        
        mode = self.gen_mode.get()
        Tvec = np.array([float(self.Ts[j].get()) for j in range(N_JOINTS)], dtype=float)
        
        self.traj_plan = None
        self.traj_idx = 0
        self._running = True

        # Capture selection flags safely in the main thread
        sel_values = [bool(self.sel[j].get()) for j in range(N_JOINTS)]

        th = threading.Thread(target=self._run_generator, args=(mode, cur, tgs, Tvec, dt, sel_values), daemon=True)
        th.start()

    def _stop(self): 
        self._running = False
        if self.last_sp is not None:
            for j in range(4):
                if self.sel[j].get():
                    self.node.send_C_rot(j+1, float(self.last_sp[j]), 0.0)
            if self.sel[4].get():
                self.node.send_C_pris(float(self.last_sp[4]))

        self._running = False
        self.traj_plan = None
        self.traj_idx = 0
        
        # Force one final update if auto-paused
        if self.auto_pause.get():
            self.root.after(10, lambda: self._update_plot())


    def _run_generator(self, mode, cur, tgt, Tvec, dt, sel_values):
        
        try:
            if mode == "escalon":
                for j in range(4): 
                    if sel_values[j]:
                        self.node.send_C_rot(j+1, float(tgt[j]), 0.0)
                if sel_values[4]:
                    self.node.send_C_pris(float(tgt[4]))
                
                self.last_sp = tgt.copy()
                time.sleep(dt) 
                return
            
            T_max = float(max(0.0, float(max(Tvec))))
            if T_max <= 0.0:
                self._stop()
                return
            
            tt = np.arange(0.0, T_max + dt/2, dt)
            
            q_plans = []; dq_plans = []; ddq_plans = []
            tb = float(self.blend_T.get())
            max_vel_user = float(self.max_vel.get())
            
            if self.mode_units.get() == "DEG":
                max_vel_user = rad(max_vel_user) 
            
            for j in range(N_JOINTS):
                if not sel_values[j]:
                    q_plans.append(cur[j] * np.ones_like(tt)); dq_plans.append(np.zeros_like(tt)); ddq_plans.append(np.zeros_like(tt))
                    continue
                
                q0 = cur[j]
                qf = tgt[j]
                T = Tvec[j]
                
                if mode == "LSPB":
                    # Calcular dqmax y tb para el generador del usuario
                    q_diff = qf - q0
                    # Perfil estándar (tb = tf/3)
                    dqmax_val = 1.5 * abs(q_diff) / T
                    dqmax_signed = dqmax_val * np.sign(q_diff)
                    
                    # Calcular tb con la fórmula del usuario
                    tb_val = (q0 - qf + dqmax_signed * T) / dqmax_signed
                    
                    # Generar vectorizado
                    q = np.zeros_like(tt)
                    dq = np.zeros_like(tt)
                    ddq = np.zeros_like(tt)
                    
                    for i, t_curr in enumerate(tt):
                        q[i], dq[i], ddq[i] = vel_trapezoidal(q0, qf, dqmax_signed, T, tb_val, t_curr)

                elif mode == "rampa":
                    q, dq, ddq = ramp_traj(q0, qf, T, tt)

                q_plans.append(q)
                dq_plans.append(dq)
                ddq_plans.append(ddq)

            self.traj_plan = (np.array(q_plans).T, np.array(dq_plans).T, np.array(ddq_plans).T)
            n_points = len(self.traj_plan[0])
            self.traj_dt = dt # Store for recorder
            
            self.traj_t0 = time.perf_counter()
            
            while self._running:
                # Time-based indexing (Frame Skipping)
                elapsed = time.perf_counter() - self.traj_t0
                idx = int(elapsed / dt)
                
                if idx >= n_points:
                    break # Finished
                
                self.traj_idx = idx
                p = self.traj_plan[0][idx]
                v = self.traj_plan[1][idx]
                
                self.last_sp = p.copy()
                
                for j in range(4):
                    if sel_values[j]:
                        self.node.send_C_rot(j+1, float(p[j]), float(v[j]))
                if sel_values[4]:
                    self.node.send_C_pris(float(p[4]))
                
                # Sleep remainder of the slot if we are ahead
                next_slot_time = (idx + 1) * dt
                sleep_time = next_slot_time - (time.perf_counter() - self.traj_t0)
                
                if sleep_time > 0:
                    time.sleep(sleep_time)
                
            # Ensure final point is always sent
            self.last_sp = tgt.copy()
            
            for j in range(4):
                if sel_values[j]:
                    self.node.send_C_rot(j+1, float(tgt[j]), 0.0)
            if sel_values[4]:
                self.node.send_C_pris(float(tgt[4]))
                
        finally:
            self._running = False
            self.traj_plan = None
            self.traj_idx = 0
        
    def _poll_A_loop(self):
        print("DEBUG: _poll_A_loop started")
        while self._polling:
            try:
                # FIX: Poll at reduced rate (20Hz) during movement to get feedback without saturation
                if self._running:
                    time.sleep(0.05)
                else:
                    # Normal polling rate when stopped
                    dt = self.safe_poll_dt
                    if dt < 0.005: dt = 0.005
                    time.sleep(dt)

                self.node.send_A_all()
            except Exception:
                time.sleep(0.1)

    def _on_close(self):
        self._running = False
        self._polling = False 
        
        if self.plot_after_id:
            try:
                self.root.after_cancel(self.plot_after_id)
            except: pass
            
        try:
            self.node.destroy_node()
        except: pass
        rclpy.shutdown()
        self.root.destroy()


def main(args=None):
    rclpy.init(args=args)
    node = TrajNode()
    gui = TrajGUI(node)

if __name__ == '__main__': main()
