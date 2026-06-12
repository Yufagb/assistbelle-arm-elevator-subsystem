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
JOINT_IDX = 4  # J4
DT = 0.01      # 100Hz control loop
POLL_DT = 0.05 # 20Hz polling rate
TF = 3.0       # Tiempo por movimiento
MAX_VEL = 10.0 # rad/s (referencia)

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

class J4TestNode(Node):
    def __init__(self):
        super().__init__('j4_test_node')
        self.pub = self.create_publisher(String, 'can_command', 10)
        
        # Match QoS with can_node
        q_state = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )
        self.sub = self.create_subscription(JointState, 'joint_states', self.on_state, q_state)
        
        self.current_pos = 0.0
        self.current_vel = 0.0 # Store velocity
        self.data_lock = threading.Lock()
        self.running = True
        
        # Historial
        self.history = {
            't': [],
            'q_sp': [], 'dq_sp': [], 'ddq_sp': [],
            'q_meas': [], 'dq_meas': [] # Add dq_meas
        }
        self.start_time = time.time()

    def on_state(self, msg):
        with self.data_lock:
            if len(msg.position) >= 5:
                self.current_pos = msg.position[JOINT_IDX-1]
            if len(msg.velocity) >= 5:
                self.current_vel = msg.velocity[JOINT_IDX-1]

    def send_cmd(self, q, dq):
        msg = String(data=f"C{JOINT_IDX}:{q:.4f},{dq:.4f}")
        self.pub.publish(msg)

    def send_poll(self):
        # FIX: Send specific poll for J4 instead of generic A_all
        self.pub.publish(String(data=f"A{JOINT_IDX}"))

def run_test():
    rclpy.init()
    node = J4TestNode()
    
    # Thread para ROS spin
    spin_thread = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
    spin_thread.start()
    
    print("--- INICIANDO TEST DE RENDIMIENTO J4 ---")
    print("Secuencia: 0 -> 90 -> -90")
    print("Grabando datos silenciosamente...")
    
    try:
        # Secuencia de movimientos
        targets = [np.deg2rad(90), np.deg2rad(-90)]
        q_start = 0.0
        
        t0_global = time.time()
        
        # Fase 1: Ir a 0 (Home)
        print("Moviendo a Home (0)...")
        node.send_cmd(0.0, 0.0)
        time.sleep(2.0)
        
        for target in targets:
            print(f"Ejecutando movimiento hacia {np.rad2deg(target):.1f} deg...")
            t_start_move = time.time()
            
            while True:
                t_now = time.time()
                t_traj = t_now - t_start_move
                
                if t_traj > TF:
                    break
                
                # Generar setpoint
                # Calcular dqmax y tb para el generador del usuario
                q_diff = target - q_start
                # Elegir dqmax para que tb sea razonable (tb <= tf/2)
                # tb = (q_diff + dqmax*tf)/dqmax  => tb*dqmax = q_diff + dqmax*tf => dqmax(tb-tf) = q_diff
                # Si tb = tf/3 (perfil seguro), entonces dqmax = q_diff / (tf/3 - tf) = q_diff / (-2/3 tf) = -1.5 * q_diff / tf
                # Usamos un perfil estándar:
                dqmax_val = 1.5 * abs(q_diff) / TF
                
                # Calcular tb con la fórmula del usuario
                # tb = (q0 - qf + dqmax * tf) / dqmax
                # Nota: la fórmula asume dqmax positivo? Si q0 > qf, dqmax debería ser negativo?
                # La función del usuario usa dqmax positivo en las fórmulas condicionales?
                # Revisando la función:
                # if t <= tb: q = q0 + 0.5 * (dqmax/tb) * t**2
                # Si qf > q0, dqmax debe ser positivo. Si qf < q0, dqmax debe ser negativo.
                
                dqmax_signed = dqmax_val * np.sign(q_diff)
                
                # tb = (q0 - qf + dqmax*tf) / dqmax
                # Si q0=0, qf=90, dqmax=45, tf=3
                # tb = (0 - 90 + 45*3) / 45 = (45)/45 = 1.0. Correcto (tf/3).
                
                tb_val = (q_start - target + dqmax_signed * TF) / dqmax_signed
                
                q_sp, dq_sp, ddq_sp = vel_trapezoidal(q_start, target, dqmax_signed, TF, tb_val, t_traj)
                
                # Enviar comando
                node.send_cmd(q_sp, dq_sp)
                
                # Polling (20Hz)
                if int(t_traj * 100) % 5 == 0:
                    node.send_poll()
                
                # Guardar datos
                with node.data_lock:
                    q_meas = node.current_pos
                    dq_meas = node.current_vel
                
                node.history['t'].append(t_now - t0_global)
                node.history['q_sp'].append(q_sp)
                node.history['dq_sp'].append(dq_sp)
                node.history['ddq_sp'].append(ddq_sp)
                node.history['q_meas'].append(q_meas)
                node.history['dq_meas'].append(dq_meas)
                
                time.sleep(DT)
            
            q_start = target
            time.sleep(0.5) # Pausa entre movimientos
            
    except KeyboardInterrupt:
        print("Test interrumpido!")
    finally:
        print("Test finalizado. Procesando gráficas...")
        node.running = False
        rclpy.shutdown()
        plot_results(node.history)

def plot_results(h):
    t = np.array(h['t'])
    q_sp = np.array(h['q_sp'])
    dq_sp = np.array(h['dq_sp'])
    ddq_sp = np.array(h['ddq_sp'])
    q_meas = np.array(h['q_meas'])
    dq_meas_raw = np.array(h['dq_meas']) # Raw encoder velocity
    
    # --- Robust Differentiation ---
    # Instead of adjacent diff, use a window to reduce quantization noise
    def robust_diff(y, t, window=5):
        n = len(y)
        dy = np.zeros(n)
        for i in range(n):
            # Indices for window
            i_min = max(0, i - window)
            i_max = min(n - 1, i + window)
            
            if i_max == i_min: continue
            
            # Simple slope between endpoints of window
            dt_w = t[i_max] - t[i_min]
            if dt_w > 1e-6:
                dy[i] = (y[i_max] - y[i_min]) / dt_w
        return dy

    # Calculate Velocity
    # dq_meas = robust_diff(q_meas, t, window=4) # REMOVED: Using encoder velocity
    dq_meas = dq_meas_raw
    
    # Calculate Acceleration from Velocity
    ddq_meas = robust_diff(dq_meas, t, window=4)
    
    # Additional Smoothing (EMA)
    def smooth(y, alpha=0.3):
        res = np.zeros_like(y)
        val = y[0]
        for i in range(len(y)):
            val = val * (1.0 - alpha) + y[i] * alpha
            res[i] = val
        return res

    dq_meas = smooth(dq_meas, alpha=0.3)
    ddq_meas = smooth(ddq_meas, alpha=0.1)
    
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, figsize=(10, 8))
    
    # Posición
    ax1.plot(t, np.rad2deg(q_sp), 'r-', label='Target')
    ax1.plot(t, np.rad2deg(q_meas), 'b--', label='Medido')
    ax1.set_ylabel('Posición [deg]')
    ax1.legend()
    ax1.grid(True)
    ax1.set_title('Rendimiento J4 - Encoder Feedback')
    
    # Velocidad
    ax2.plot(t, np.rad2deg(dq_sp), 'r-', label='Target')
    ax2.plot(t, np.rad2deg(dq_meas), 'b--', label='Medido (Encoder)')
    ax2.set_ylabel('Velocidad [deg/s]')
    ax2.legend()
    ax2.grid(True)
    
    # Aceleración
    ax3.plot(t, np.rad2deg(ddq_sp), 'r-', label='Target')
    ax3.plot(t, np.rad2deg(ddq_meas), 'b--', label='Medido (Calc)')
    ax3.set_ylabel('Aceleración [deg/s²]')
    ax3.set_xlabel('Tiempo [s]')
    ax3.legend()
    ax3.grid(True)
    
    plt.tight_layout()
    plt.show()

def main():
    run_test()

if __name__ == '__main__':
    main()
