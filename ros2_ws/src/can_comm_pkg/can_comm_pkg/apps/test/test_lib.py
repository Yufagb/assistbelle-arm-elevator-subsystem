import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from std_msgs.msg import String
from sensor_msgs.msg import JointState
import time
import numpy as np
import matplotlib.pyplot as plt
import threading
import sys
import os
import termios
import tty

# --- UTILS ---
def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def savgol_filter(y, window_length, polyorder, deriv=0, delta=1.0):
    """Filtro Savitzky-Golay (Implementación NumPy)"""
    try:
        if len(y) < window_length: return y
        if window_length % 2 == 0: window_length += 1
        half_window = (window_length - 1) // 2
        x = np.arange(-half_window, half_window + 1)
        A = np.vander(x, polyorder + 1)[:, ::-1]
        m = np.linalg.pinv(A)
        coeffs = m[deriv]
        y_smooth = np.convolve(y, coeffs[::-1], mode='same')
        if deriv > 0:
            import math
            y_smooth *= math.factorial(deriv) / (delta ** deriv)
        return y_smooth
    except:
        return y

# --- NODE ---
class PerformanceTestNode(Node):
    def __init__(self, joint_idx):
        super().__init__(f'j{joint_idx}_perf_test')
        self.joint_idx = joint_idx
        self.pub = self.create_publisher(String, 'can_command', 10)
        
        q_state = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )
        self.sub = self.create_subscription(JointState, 'joint_states', self.on_state, q_state)
        
        self.current_pos = 0.0
        self.current_vel = 0.0
        self.data_lock = threading.Lock()
        
        self.history = {
            't': [], 'q_sp': [], 'dq_sp': [], 'ddq_sp': [],
            'q_meas': []
        }
        self.start_time = time.time()

    def on_state(self, msg):
        with self.data_lock:
            if len(msg.position) >= 5:
                self.current_pos = msg.position[self.joint_idx-1]
            if len(msg.velocity) >= 5:
                self.current_vel = msg.velocity[self.joint_idx-1]

    def send_cmd(self, q, dq=0.0):
        # Enviar comando
        if self.joint_idx == 5:
            # J5 (Prismatic) solo acepta posición (1 float)
            msg = String(data=f"C{self.joint_idx}:{q:.4f}")
        else:
            # J1-J4 aceptan Posición y Velocidad FF (2 floats)
            msg = String(data=f"C{self.joint_idx}:{q:.4f},{dq:.4f}")
        self.pub.publish(msg)

    def send_poll(self):
        self.pub.publish(String(data=f"A{self.joint_idx}"))

# --- TRAJECTORY GENERATORS ---
def gen_step(t, q0, qf, tf):
    if t < 0: return q0, 0, 0
    return qf, 0, 0

def gen_ramp(t, q0, qf, tf):
    if t < 0: return q0, 0, 0
    if t > tf: return qf, 0, 0
    
    dq = (qf - q0) / tf
    q = q0 + dq * t
    return q, dq, 0

def gen_trap(t, q0, qf, tf):
    # Perfil trapezoidal simple (1/3 accel, 1/3 const, 1/3 decel)
    if t < 0: return q0, 0, 0
    if t > tf: return qf, 0, 0
    
    dist = qf - q0
    v_max = 1.5 * dist / tf
    tb = tf / 3.0
    a_max = v_max / tb
    
    if t <= tb:
        q = q0 + 0.5 * a_max * t**2
        dq = a_max * t
        ddq = a_max
    elif t <= tf - tb:
        q = q0 + 0.5 * a_max * tb**2 + v_max * (t - tb)
        dq = v_max
        ddq = 0
    else:
        t_dec = t - (tf - tb)
        q = qf - 0.5 * a_max * (tb - t_dec)**2
        dq = v_max - a_max * t_dec
        ddq = -a_max
        
    return q, dq, ddq

# --- MAIN RUNNER ---
def run_test(joint_idx, profile_type, script_path=None):
    print(f"\n=== TEST DE RENDIMIENTO J{joint_idx}: {profile_type.upper()} ===")
    
    # Determine units based on joint
    # User requested J5 in mm. Assuming J5 is linear (e.g. prismatic).
    # Others are rotational (deg).
    is_linear = (joint_idx == 5)
    unit_str = "mm" if is_linear else "deg"
    
    # 1. Get Parameters
    try:
        default_target = 100.0 if is_linear else 90.0
        target_val = float(input(f"Objetivo [{unit_str}] (default {default_target}): ") or default_target)
        tf = float(input("Tiempo de movimiento [s] (default 3.0): ") or 3.0)
        reps = int(input("Repeticiones (default 5): ") or 5)
    except ValueError:
        print("Error en parámetros. Usando defaults.")
        target_val = 100.0 if is_linear else 90.0
        tf = 3.0
        reps = 5

    print(f"\nConfiguración: {reps} reps de 0 -> {target_val} {unit_str} en {tf} s")
    print("Iniciando ROS2...")
    
    rclpy.init()
    node = PerformanceTestNode(joint_idx)
    spin_thread = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
    spin_thread.start()
    
    try:
        # 0. Ir a Home
        print(f"Yendo a Home (0 {unit_str})...")
        node.send_cmd(0.0, 0.0)
        time.sleep(2.0)
        
        t0_global = time.time()
        dt = 0.01
        
        # Convert target to internal units (rad or meters/mm)
        if is_linear:
            # J5 uses mm directly (no conversion to meters)
            target_internal = target_val
        else:
            # deg -> rad
            target_internal = np.deg2rad(target_val)
        
        for i in range(reps):
            print(f"--- Repetición {i+1}/{reps} ---")
            
            # Movimiento IDA (0 -> Target)
            q_start = 0.0
            q_end = target_internal
            
            t_start_move = time.time()
            while True:
                t_now = time.time()
                t_traj = t_now - t_start_move
                
                if t_traj > tf + 0.5: # 0.5s extra settling
                    break
                
                # Generar setpoint
                if profile_type == 'step':
                    q, dq, ddq = gen_step(t_traj, q_start, q_end, tf)
                elif profile_type == 'ramp':
                    q, dq, ddq = gen_ramp(t_traj, q_start, q_end, tf)
                elif profile_type == 'trap':
                    q, dq, ddq = gen_trap(t_traj, q_start, q_end, tf)
                
                # Enviar
                node.send_cmd(q, dq)
                
                # Poll (20Hz)
                if int(t_traj * 100) % 5 == 0:
                    node.send_poll()
                
                # Record
                with node.data_lock:
                    q_m = node.current_pos
                
                node.history['t'].append(t_now - t0_global)
                node.history['q_sp'].append(q)
                node.history['dq_sp'].append(dq)
                node.history['ddq_sp'].append(ddq)
                node.history['q_meas'].append(q_m)
                
                time.sleep(dt)
            
            time.sleep(0.5)
            
            # Movimiento VUELTA (Target -> 0)
            q_start = target_internal
            q_end = 0.0
            
            t_start_move = time.time()
            while True:
                t_now = time.time()
                t_traj = t_now - t_start_move
                
                if t_traj > tf + 0.5:
                    break
                
                if profile_type == 'step':
                    q, dq, ddq = gen_step(t_traj, q_start, q_end, tf)
                elif profile_type == 'ramp':
                    q, dq, ddq = gen_ramp(t_traj, q_start, q_end, tf)
                elif profile_type == 'trap':
                    q, dq, ddq = gen_trap(t_traj, q_start, q_end, tf)
                
                node.send_cmd(q, dq)
                
                if int(t_traj * 100) % 5 == 0:
                    node.send_poll()
                
                with node.data_lock:
                    q_m = node.current_pos
                
                node.history['t'].append(t_now - t0_global)
                node.history['q_sp'].append(q)
                node.history['dq_sp'].append(dq)
                node.history['ddq_sp'].append(ddq)
                node.history['q_meas'].append(q_m)
                
                time.sleep(dt)
                
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nInterrumpido por usuario.")
    finally:
        print("Finalizando y graficando...")
        node.destroy_node()
        rclpy.shutdown()
        plot_results(node.history, joint_idx, profile_type, reps, target_val, script_path)

def plot_results(h, joint_idx, profile_type, reps, target_val, script_path):
    t = np.array(h['t'], dtype=float)
    q_sp = np.array(h['q_sp'], dtype=float)
    dq_sp = np.array(h['dq_sp'], dtype=float)
    ddq_sp = np.array(h['ddq_sp'], dtype=float)
    q_meas_raw = np.array(h['q_meas'], dtype=float)
    
    # --- PROCESAMIENTO AVANZADO ---
    # 1. Suavizar Posición (SG Filter)
    q_meas = savgol_filter(q_meas_raw, window_length=31, polyorder=2, deriv=0)
    
    # 2. Calcular Velocidad (Derivada SG)
    dt_avg = np.mean(np.diff(t)) if len(t) > 1 else 0.01
    dq_meas = savgol_filter(q_meas, window_length=31, polyorder=2, deriv=1, delta=dt_avg)
    
    # 3. Calcular Aceleración (Derivada SG de Velocidad)
    ddq_meas = savgol_filter(dq_meas, window_length=31, polyorder=2, deriv=1, delta=dt_avg)
    
    # --- CALCULAR ERRORES ---
    q_err = q_sp - q_meas
    dq_err = dq_sp - dq_meas
    ddq_err = ddq_sp - ddq_meas
    
    # --- CONVERSIÓN DE UNIDADES PARA GRAFICAR ---
    is_linear = (joint_idx == 5)
    unit_pos = "mm" if is_linear else "deg"
    unit_vel = "mm/s" if is_linear else "deg/s"
    unit_acc = "mm/s²" if is_linear else "deg/s²"
    
    if is_linear:
        # meters -> mm (BUT internal is already mm, so scale=1.0)
        scale = 1.0
    else:
        # rad -> deg
        scale = 180.0 / np.pi
        
    q_sp *= scale
    q_meas *= scale
    q_err *= scale
    
    dq_sp *= scale
    dq_meas *= scale
    dq_err *= scale
    
    ddq_sp *= scale
    ddq_meas *= scale
    ddq_err *= scale
    
    # --- GUARDAR DATOS (CSV) ---
    # Naming: jx_movimiento_posicon(grados)_numerorepeticiones
    # Example: j4_step_90.0deg_5reps OR j1_step_100.0mm_5reps
    filename_base = f"j{joint_idx}_{profile_type}_{target_val}{unit_pos}_{reps}reps"
    
    # Location: "una carpetita que se llame resultados" -> CWD/resultados
    save_dir = os.path.join(os.getcwd(), "resultados")
        
    # Ensure dir exists
    os.makedirs(save_dir, exist_ok=True)
    
    csv_path = os.path.join(save_dir, f"{filename_base}.csv")
    header = f"t,q_sp,dq_sp,ddq_sp,q_meas,dq_meas,ddq_meas,q_err,dq_err,ddq_err"
    # Note: Data saved is already converted to display units (mm or deg)
    data = np.column_stack((t, q_sp, dq_sp, ddq_sp, q_meas, dq_meas, ddq_meas, q_err, dq_err, ddq_err))
    try:
        np.savetxt(csv_path, data, delimiter=",", header=header, comments="")
        print(f"Datos guardados en: {csv_path}")
    except Exception as e:
        print(f"Error guardando CSV: {e}")
        # Fallback to cwd if permission denied
        np.savetxt(f"{filename_base}.csv", data, delimiter=",", header=header, comments="")
        print(f"Guardado en local (fallback): {filename_base}.csv")

    # --- GRAFICAR ---
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, figsize=(12, 10))
    
    fig.suptitle(f'Test J{joint_idx} - {profile_type.upper()} ({reps} Reps)', fontsize=16)
    
    # Posición
    ax1.plot(t, q_sp, 'r-', label='Target')
    ax1.plot(t, q_meas, 'b--', label='Medido')
    ax1.plot(t, q_err, 'm:', label='Error')
    ax1.set_ylabel(f'Pos [{unit_pos}]')
    ax1.legend()
    ax1.grid(True)
    ax1.set_title("Posición y Error")
    
    # Velocidad
    ax2.plot(t, dq_sp, 'r-', label='Target')
    ax2.plot(t, dq_meas, 'b--', label='Medido')
    ax2.plot(t, dq_err, 'm:', label='Error')
    ax2.set_ylabel(f'Vel [{unit_vel}]')
    ax2.legend()
    ax2.grid(True)
    ax2.set_title("Velocidad y Error")
    
    # Aceleración
    ax3.plot(t, ddq_sp, 'r-', label='Target')
    ax3.plot(t, ddq_meas, 'b--', label='Medido')
    ax3.plot(t, ddq_err, 'm:', label='Error')
    ax3.set_ylabel(f'Acc [{unit_acc}]')
    ax3.set_xlabel('Tiempo [s]')
    ax3.legend()
    ax3.grid(True)
    ax3.set_title("Aceleración y Error")
    
    plt.tight_layout()
    
    # --- GUARDAR IMAGEN (PNG) ---
    png_path = os.path.join(save_dir, f"{filename_base}.png")
    try:
        plt.savefig(png_path)
        print(f"Gráfica guardada en: {png_path}")
    except Exception as e:
        print(f"Error guardando PNG: {e}")
    
    plt.show()
