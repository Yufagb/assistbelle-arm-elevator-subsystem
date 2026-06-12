#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from std_msgs.msg import String
from sensor_msgs.msg import JointState
import time
import numpy as np
import matplotlib.pyplot as plt
import threading

# --- Configuración ---
JOINT_IDX = 3  # J3
DT = 0.01      # 100Hz recording
TF = 4.0       # Tiempo por movimiento (suficiente para asentar)
REPETITIONS = 5
TARGET_DEG = 90.0

class StepTestNode(Node):
    def __init__(self):
        super().__init__(f'j{JOINT_IDX}_step_test')
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
            't': [],
            'q_sp': [],
            'q_meas': []
        }
        self.start_time = time.time()

    def on_state(self, msg):
        with self.data_lock:
            if len(msg.position) >= 5:
                self.current_pos = msg.position[JOINT_IDX-1]
            if len(msg.velocity) >= 5:
                self.current_vel = msg.velocity[JOINT_IDX-1]

    def send_cmd(self, q):
        # Enviar solo posición (velocidad 0 o ignorada en modo posición, pero enviamos 0.0)
        msg = String(data=f"C{JOINT_IDX}:{q:.4f},0.0")
        self.pub.publish(msg)

    def send_poll(self):
        self.pub.publish(String(data=f"A{JOINT_IDX}"))

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

def run_test():
    rclpy.init()
    node = StepTestNode()
    
    spin_thread = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
    spin_thread.start()
    
    print(f"--- TEST ESCALÓN J{JOINT_IDX} ({REPETITIONS} Repeticiones) ---")
    print(f"Secuencia: 0 -> {TARGET_DEG} -> 0")
    
    try:
        # 1. Ir a Home
        print("Yendo a Home (0)...")
        node.send_cmd(0.0)
        time.sleep(2.0)
        
        t0_global = time.time()
        
        for i in range(REPETITIONS):
            print(f"Repetición {i+1}/{REPETITIONS}...")
            
            # --- Paso 1: 0 -> 90 ---
            target = np.deg2rad(TARGET_DEG)
            node.send_cmd(target) # ESCALÓN
            
            t_start = time.time()
            while time.time() - t_start < TF:
                t_now = time.time()
                
                # Polling
                if int((t_now - t_start)*100) % 5 == 0:
                    node.send_poll()
                
                # Grabar
                with node.data_lock:
                    q_m = node.current_pos
                
                node.history['t'].append(t_now - t0_global)
                node.history['q_sp'].append(target)
                node.history['q_meas'].append(q_m)
                time.sleep(DT)
                
            # --- Paso 2: 90 -> 0 ---
            target = 0.0
            node.send_cmd(target) # ESCALÓN
            
            t_start = time.time()
            while time.time() - t_start < TF:
                t_now = time.time()
                
                if int((t_now - t_start)*100) % 5 == 0:
                    node.send_poll()
                
                with node.data_lock:
                    q_m = node.current_pos
                
                node.history['t'].append(t_now - t0_global)
                node.history['q_sp'].append(target)
                node.history['q_meas'].append(q_m)
                time.sleep(DT)
                
    except KeyboardInterrupt:
        print("Interrumpido.")
    finally:
        print("Finalizado. Procesando...")
        node.destroy_node()
        rclpy.shutdown()
        plot_results(node.history)

def plot_results(h):
    t = np.array(h['t'])
    q_sp = np.array(h['q_sp'])
    q_meas_raw = np.array(h['q_meas'])
    
    # --- PROCESAMIENTO AVANZADO ---
    # 1. Suavizar Posición (SG Filter)
    q_meas = savgol_filter(q_meas_raw, window_length=31, polyorder=2, deriv=0)
    
    # 2. Calcular Velocidad (Derivada SG)
    dt_avg = np.mean(np.diff(t)) if len(t) > 1 else 0.01
    dq_meas = savgol_filter(q_meas, window_length=31, polyorder=2, deriv=1, delta=dt_avg)
    
    # 3. Calcular Aceleración (Derivada SG de Velocidad)
    ddq_meas = savgol_filter(dq_meas, window_length=31, polyorder=2, deriv=1, delta=dt_avg)
    
    # --- GRAFICAR ---
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, figsize=(10, 10))
    
    ax1.set_title(f'Respuesta al Escalón J{JOINT_IDX} - {REPETITIONS} Repeticiones')
    
    # Posición
    ax1.plot(t, np.rad2deg(q_sp), 'r-', label='Target')
    ax1.plot(t, np.rad2deg(q_meas), 'b--', label='Medido (Suavizado)')
    ax1.plot(t, np.rad2deg(q_meas_raw), 'g:', alpha=0.3, label='Raw')
    ax1.set_ylabel('Pos [deg]')
    ax1.legend()
    ax1.grid(True)
    
    # Velocidad
    ax2.plot(t, np.rad2deg(dq_meas), 'b-', label='Velocidad (Calc)')
    ax2.set_ylabel('Vel [deg/s]')
    ax2.legend()
    ax2.grid(True)
    
    # Aceleración
    ax3.plot(t, np.rad2deg(ddq_meas), 'b-', label='Aceleración (Calc)')
    ax3.set_ylabel('Acc [deg/s²]')
    ax3.set_xlabel('Tiempo [s]')
    ax3.legend()
    ax3.grid(True)
    
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    run_test()
