#!/usr/bin/env python3
import sys
import tty
import termios
import numpy as np
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32MultiArray
from .cinematica_inversa import ik_solve_position, ik_solve_arm_only, fk_forward, ik_solve_arm_pitch_constrained
import select
import time
import os
import json

# ===================== CONFIGURACIÓN =====================
# Velocidades Máximas (Target)
MAX_VEL_XYZ_M_S = 0.10   # 10 cm/s (Cartesiano)
MAX_VEL_ELEV_M_S = 0.10  # 10 cm/s (Elevador)
MAX_VEL_WRIST_RAD_S = 1.0 # ~60 deg/s

# Aceleraciones (Slew Rate Limits)
ACCEL_XYZ_M_S2 = 0.2     # 20 cm/s^2
ACCEL_ELEV_M_S2 = 0.5
ACCEL_WRIST_RAD_S2 = 1.5

# Timeout para detener movimiento si no hay tecla
INPUT_TIMEOUT = 0.15 # segundos

# Frecuencia de Loop
LOOP_RATE = 50.0 # Hz
DT = 1.0 / LOOP_RATE

# Posición Home
HOME_XYZ = np.array([0.4, 0.0, 0.5])
HOME_J5 = 0.0

# Límites Articulares (Copiados de cinematica_inversa.py)
JOINT_LIMITS = [
    (0.0, 0.35),                  # J5 (d0) [m]
    (np.deg2rad(-135), np.deg2rad(34)),  # J1 (th1)
    (np.deg2rad(-45), np.deg2rad(70)),   # J2 (th2)
    (np.deg2rad(-140), np.deg2rad(120)), # J3 (th3)
    (np.deg2rad(-180), np.deg2rad(180))  # J4 (th4)
]

JOINT_NAMES = ["J5 (Elev)", "J1 (Base)", "J2 (Homb)", "J3 (Codo)", "J4 (Muñe)"]

TRAJECTORY_FILE = "trajectory.json"

# ===================== UTILIDADES =====================
class SlewLimiter:
    def __init__(self, val=0.0):
        self.val = val

    def update(self, target, dt, max_rate):
        diff = target - self.val
        max_change = max_rate * dt
        
        if abs(diff) < max_change:
            self.val = target
        else:
            self.val += max_change * np.sign(diff)
        return self.val

def save_terminal_settings():
    fd = sys.stdin.fileno()
    return termios.tcgetattr(fd)

def restore_terminal_settings(old_settings):
    fd = sys.stdin.fileno()
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def set_raw_mode():
    fd = sys.stdin.fileno()
    tty.setraw(fd)

def is_data():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def clear_screen():
    sys.stdout.write('\033[2J\033[H')
    sys.stdout.flush()

def check_limits(q_full):
    warnings = []
    tol = 1e-3
    for i in range(5):
        val = q_full[i]
        min_l, max_l = JOINT_LIMITS[i]
        if val <= min_l + tol:
            val_disp = val if i==0 else np.rad2deg(val)
            unit = "m" if i==0 else "deg"
            warnings.append(f"MIN {JOINT_NAMES[i]}: {val_disp:.1f} {unit}")
        elif val >= max_l - tol:
            val_disp = val if i==0 else np.rad2deg(val)
            unit = "m" if i==0 else "deg"
            warnings.append(f"MAX {JOINT_NAMES[i]}: {val_disp:.1f} {unit}")
    return warnings

def save_waypoints(waypoints, filename):
    try:
        data = []
        for wp in waypoints:
            # Convert numpy arrays to list for JSON serialization
            item = {
                'd0': float(wp['d0']),
                'joints': wp['joints'].tolist(),
                'gripper': float(wp['gripper'])
            }
            data.append(item)
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        return True, f"Guardado en {filename}"
    except Exception as e:
        return False, f"Error al guardar: {e}"

def load_waypoints(filename):
    try:
        if not os.path.exists(filename):
            return [], "Archivo no encontrado."
            
        with open(filename, 'r') as f:
            data = json.load(f)
            
        waypoints = []
        for item in data:
            wp = {
                'd0': float(item['d0']),
                'joints': np.array(item['joints']),
                'gripper': float(item['gripper'])
            }
            waypoints.append(wp)
        return waypoints, f"Cargados {len(waypoints)} puntos."
    except Exception as e:
        return [], f"Error al cargar: {e}"

# ===================== CLASE NODO =====================
class TeleopNodeRecord(Node):
    def __init__(self):
        super().__init__('control_teclado_record')
        self.pub = self.create_publisher(String, 'can_command', 10)
        self.sub = self.create_subscription(Float32MultiArray, 'motors_state', self.listener_callback, 10)
        
        self.current_pos = np.array([0.4, 0.0, 0.5]) 
        self.current_joints = np.zeros(5) # [th1, th2, th3, th4, d0_mm]
        self.data_received = False
        self.timer = self.create_timer(0.1, self.poll_motors)
        self.get_logger().info("Esperando datos de encoders...")

    def poll_motors(self):
        for i in range(1, 6):
            self.pub.publish(String(data=f"A{i}"))

    def listener_callback(self, msg):
        if len(msg.data) < 5: return
        self.current_joints = np.array(msg.data)
        th1, th2, th3, th4 = msg.data[0], msg.data[1], msg.data[2], msg.data[3]
        d0_m = msg.data[4] / 1000.0
        pos = fk_forward(d0_m, th1, th2, th3, th4)
        self.current_pos = np.array(pos)
        if not self.data_received:
            self.data_received = True

    def send_command(self, q_sol):
        if np.isnan(q_sol).any(): return
        for i in range(1, 5):
            val_rad = q_sol[i]
            msg = f"C{i}:{val_rad:.4f},0.0" 
            self.pub.publish(String(data=msg))
        val_j5_mm = q_sol[0] * 1000.0
        msg = f"C5:{val_j5_mm:.2f}" 
        self.pub.publish(String(data=msg))

    def send_gripper(self, pct):
        msg = f"D2:{pct:.1f}"
        self.pub.publish(String(data=msg))

# ===================== UI & LOGIC =====================
def print_interface(mode, target_pos, target_d0, real_pos, real_d0, real_joints, target_joints, 
                    vel_vector, parallel_mode, gripper_pct, warnings, waypoints, replay_idx, recording_continuous, message=""):
    
    lines = []
    lines.append("============================================")
    lines.append("   CONTROL RECORD & REPLAY (ENHANCED)")
    lines.append("============================================")
    lines.append(f"MODO ACTUAL: {mode}")
    
    if mode == 'REPLAY':
        lines.append(f"  REPRODUCIENDO: Paso {replay_idx+1}/{len(waypoints)}")
    else:
        lines.append("  [k]: Grabar Keypoint (Paso)")
        lines.append(f"  [R]: Grabar Continuo ({'ON' if recording_continuous else 'OFF'})")
        lines.append("  [p]: Reproducir Secuencia")
        lines.append("  [S]: Guardar a Archivo")
        lines.append("  [L]: Cargar de Archivo")
        lines.append("  [G]: Ir a Paso...")
        lines.append("  [c]: Borrar Todo")
        lines.append(f"  Puntos Guardados: {len(waypoints)}")

    lines.append("--------------------------------------------")
    lines.append("ESTADO:")
    lines.append(f"  Target XYZ : [{target_pos[0]:.3f}, {target_pos[1]:.3f}, {target_pos[2]:.3f}]")
    lines.append(f"  Real XYZ   : [{real_pos[0]:.3f}, {real_pos[1]:.3f}, {real_pos[2]:.3f}]")
    lines.append("--------------------------------------------")
    
    t_j5_mm = target_joints[0] * 1000.0
    r_j5_mm = real_joints[4]
    lines.append(f"  J5 (Elev): {t_j5_mm:6.1f} mm | {r_j5_mm:6.1f} mm")
    
    t_degs = np.rad2deg(target_joints[1:5])
    r_degs = np.rad2deg(real_joints[0:4])
    lines.append(f"  J1..J4   : {t_degs[0]:5.1f}, {t_degs[1]:5.1f}, {t_degs[2]:5.1f}, {t_degs[3]:5.1f} deg")
    lines.append(f"             {r_degs[0]:5.1f}, {r_degs[1]:5.1f}, {r_degs[2]:5.1f}, {r_degs[3]:5.1f} deg")
    lines.append("--------------------------------------------")
    
    if warnings:
        lines.append("\033[91mALERTA DE LIMITES:\033[0m")
        for w in warnings:
            lines.append(f"  \033[93m{w}\033[0m")
        lines.append("--------------------------------------------")
    
    lines.append(f"  Modo J4   : {'PARALELO' if parallel_mode else 'LIBRE'}")
    lines.append(f"  Gripper   : {gripper_pct:.0f}%  [o] Abrir / [i] Cerrar")
    lines.append("--------------------------------------------")
    lines.append("MANTENER TECLA PARA MOVER")
    lines.append("[m] Cambiar Modo, [h] Home, [x] Salir")
    if message:
        lines.append(f"MSG: {message}")
    lines.append("--------------------------------------------")
    
    clear_screen()
    for line in lines:
        sys.stdout.write(line + '\r\n')
    sys.stdout.flush()

def main():
    rclpy.init()
    node = TeleopNodeRecord()
    
    import threading
    spinner = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
    spinner.start()
    
    print("Esperando sincronización...")
    time.sleep(1.0)
    
    current_mode = 'ELEVATOR'
    parallel_mode = False
    gripper_pct = 0.0
    
    waypoints = []
    replay_index = 0
    replay_timer = 0.0
    REPLAY_WAIT_TIME = 0.5 # Menos espera para movimientos continuos
    
    recording_continuous = False
    last_record_time = 0.0
    RECORD_INTERVAL = 0.1 # 10 Hz
    
    if not node.data_received:
        print("WARN: Sin datos. Usando default.")
    
    target_d0 = node.current_joints[4] / 1000.0
    target_joints_arm = node.current_joints[0:4]
    target_pos_xyz = node.current_pos.copy()
    
    slew_x = SlewLimiter(0.0)
    slew_y = SlewLimiter(0.0)
    slew_z = SlewLimiter(0.0)
    
    last_input_time = 0.0
    last_ui_update = 0
    message = "Listo. Mantén teclas para mover."
    
    last_sent_target = np.zeros(5)
    last_sent_time = 0.0
    CMD_TOLERANCE = 1e-5
    HEARTBEAT_TIME = 1.0
    
    old_settings = save_terminal_settings()
    
    try:
        set_raw_mode()
        
        while True:
            loop_start = time.time()
            now = time.time()
            
            key = None
            if is_data():
                key = sys.stdin.read(1)
                last_input_time = now
            
            if key == 'x': break
            elif key == '\x03': break
            
            # --- LOGICA REPLAY ---
            if current_mode == 'REPLAY':
                if replay_index < len(waypoints):
                    wp = waypoints[replay_index]
                    
                    target_d0 = wp['d0']
                    target_joints_arm = wp['joints']
                    gripper_pct = wp['gripper']
                    
                    node.send_gripper(gripper_pct)
                    
                    full_target_wp = np.concatenate(([target_d0], target_joints_arm))
                    real_state_fmt = np.concatenate(([node.current_joints[4]/1000.0], node.current_joints[0:4]))
                    
                    dist = np.linalg.norm(full_target_wp - real_state_fmt)
                    
                    # Tolerancia adaptativa: si los puntos están muy cerca (grabación continua), relajar espera
                    # O simplemente avanzar si estamos cerca
                    if dist < 0.05: 
                        replay_timer += DT
                        # Si es grabación continua, el wait time debería ser casi 0
                        # Pero para keypoints manuales, queremos pausa.
                        # Por ahora, fijo pequeño.
                        if replay_timer > 0.05: # Muy rápido para fluidez
                            replay_index += 1
                            replay_timer = 0.0
                    else:
                        replay_timer = 0.0
                        
                else:
                    current_mode = 'ELEVATOR'
                    message = "Replay Finalizado."
            
            else:
                # --- LOGICA MANUAL ---
                if key == 'm':
                    modes = ['ELEVATOR', 'ARM', 'WRIST', 'CAMERA']
                    idx = modes.index(current_mode)
                    current_mode = modes[(idx + 1) % len(modes)]
                    message = f"Modo: {current_mode}"
                    slew_x.val = 0.0; slew_y.val = 0.0; slew_z.val = 0.0
                    target_d0 = node.current_joints[4] / 1000.0
                    target_joints_arm = node.current_joints[0:4]
                    target_pos_xyz = node.current_pos.copy()

                elif key == 'l':
                    parallel_mode = not parallel_mode
                    message = f"Paralelo: {parallel_mode}"
                elif key == 'h':
                    target_d0 = 0.0
                    target_joints_arm = np.zeros(4)
                    target_pos_xyz = fk_forward(0.0, *target_joints_arm)
                    message = "Yendo a HOME..."
                elif key == 'o':
                    gripper_pct = 100.0
                    node.send_gripper(100.0)
                    message = "Gripper Abierto"
                elif key == 'i': # CLOSE GRIPPER (New key)
                    gripper_pct = 0.0
                    node.send_gripper(0.0)
                    message = "Gripper Cerrado"
                
                elif key == 'p': # PLAY
                    if len(waypoints) > 0:
                        current_mode = 'REPLAY'
                        replay_index = 0
                        replay_timer = 0.0
                        message = "Iniciando Replay..."
                    else:
                        message = "No hay puntos guardados."
                
                elif key == 'k': # KEYPOINT (Manual)
                    wp = { 'd0': target_d0, 'joints': target_joints_arm.copy(), 'gripper': gripper_pct }
                    waypoints.append(wp)
                    message = f"Paso {len(waypoints)} guardado."
                
                elif key == 'R': # RECORD CONTINUOUS
                    recording_continuous = not recording_continuous
                    message = f"Grabación Continua: {'ON' if recording_continuous else 'OFF'}"
                
                elif key == 'c': # CLEAR
                    waypoints = []
                    recording_continuous = False
                    message = "Trayectoria borrada."
                
                elif key == 'S': # SAVE
                    restore_terminal_settings(old_settings)
                    fname = input(f"\nGuardar como [{TRAJECTORY_FILE}]: ").strip()
                    if not fname: fname = TRAJECTORY_FILE
                    ok, msg = save_waypoints(waypoints, fname)
                    message = msg
                    set_raw_mode()
                
                elif key == 'L': # LOAD
                    restore_terminal_settings(old_settings)
                    fname = input(f"\nCargar de [{TRAJECTORY_FILE}]: ").strip()
                    if not fname: fname = TRAJECTORY_FILE
                    wps, msg = load_waypoints(fname)
                    if wps: waypoints = wps
                    message = msg
                    set_raw_mode()
                
                elif key == 'G': # GOTO STEP
                    restore_terminal_settings(old_settings)
                    try:
                        idx_str = input(f"\nIr a Paso (1-{len(waypoints)}): ").strip()
                        idx = int(idx_str) - 1
                        if 0 <= idx < len(waypoints):
                            wp = waypoints[idx]
                            target_d0 = wp['d0']
                            target_joints_arm = wp['joints']
                            gripper_pct = wp['gripper']
                            # Update XYZ for consistency
                            target_pos_xyz = fk_forward(target_d0, *target_joints_arm)
                            message = f"Saltando a Paso {idx+1}"
                        else:
                            message = "Indice invalido."
                    except:
                        message = "Entrada invalida."
                    set_raw_mode()

                # ... (Movimiento Manual) ...
                v_target = np.zeros(3)
                if now - last_input_time < INPUT_TIMEOUT:
                    if key in ['w', 's', 'a', 'd', 'q', 'e']:
                        val = 1.0 
                        if key == 'w': v_target[0] = val
                        elif key == 's': v_target[0] = -val
                        elif key == 'a': v_target[1] = val
                        elif key == 'd': v_target[1] = -val
                        elif key == 'q': v_target[2] = val
                        elif key == 'e': v_target[2] = -val
                
                # Actualizar Dinámica
                if current_mode != 'REPLAY':
                    if current_mode == 'ELEVATOR':
                        v_req = v_target[0] * MAX_VEL_ELEV_M_S
                        v_act = slew_x.update(v_req, DT, ACCEL_ELEV_M_S2)
                        target_d0 += v_act * DT
                        target_d0 = clamp(target_d0, 0.0, 0.35)
                        target_pos_xyz = fk_forward(target_d0, *target_joints_arm)
                        
                    elif current_mode == 'WRIST':
                        v_req = v_target[0] * MAX_VEL_WRIST_RAD_S
                        v_act = slew_x.update(v_req, DT, ACCEL_WRIST_RAD_S2)
                        target_joints_arm[3] += v_act * DT
                        target_joints_arm[3] = clamp(target_joints_arm[3], -np.pi, np.pi)
                        target_pos_xyz = fk_forward(target_d0, *target_joints_arm)

                    elif current_mode == 'ARM':
                        req_vx = v_target[0] * MAX_VEL_XYZ_M_S
                        req_vy = v_target[1] * MAX_VEL_XYZ_M_S
                        req_vz = v_target[2] * MAX_VEL_XYZ_M_S
                        act_vx = slew_x.update(req_vx, DT, ACCEL_XYZ_M_S2)
                        act_vy = slew_y.update(req_vy, DT, ACCEL_XYZ_M_S2)
                        act_vz = slew_z.update(req_vz, DT, ACCEL_XYZ_M_S2)
                        target_pos_xyz[0] += act_vx * DT
                        target_pos_xyz[1] += act_vy * DT
                        target_pos_xyz[2] += act_vz * DT
                        
                    elif current_mode == 'CAMERA':
                        th1 = target_joints_arm[0]
                        fwd = np.array([np.cos(th1), np.sin(th1), 0])
                        right = np.array([np.sin(th1), -np.cos(th1), 0])
                        up = np.array([0, 0, 1])
                        v_local_up = v_target[0] * MAX_VEL_XYZ_M_S
                        v_local_right = -v_target[1] * MAX_VEL_XYZ_M_S 
                        v_local_fwd = v_target[2] * MAX_VEL_XYZ_M_S
                        act_v_up = slew_x.update(v_local_up, DT, ACCEL_XYZ_M_S2)
                        act_v_right = slew_y.update(v_local_right, DT, ACCEL_XYZ_M_S2)
                        act_v_fwd = slew_z.update(v_local_fwd, DT, ACCEL_XYZ_M_S2)
                        v_global = act_v_up * up + act_v_right * right + act_v_fwd * fwd
                        target_pos_xyz += v_global * DT

                    if current_mode in ['ARM', 'CAMERA']:
                        q0_seed = target_joints_arm
                        if parallel_mode or current_mode == 'CAMERA':
                            q_sol, err = ik_solve_arm_pitch_constrained(target_pos_xyz, target_d0, 0.0, q0_seed)
                        else:
                            q_sol, err = ik_solve_arm_only(target_pos_xyz, target_d0, q0_seed)
                        if err < 0.05:
                            target_joints_arm = q_sol[1:5]
                
                # GRABACION CONTINUA
                if recording_continuous and (now - last_record_time > RECORD_INTERVAL):
                    wp = { 'd0': target_d0, 'joints': target_joints_arm.copy(), 'gripper': gripper_pct }
                    waypoints.append(wp)
                    last_record_time = now

            # 6. ENVIAR COMANDO
            full_target = np.concatenate(([target_d0], target_joints_arm))
            moved = np.linalg.norm(full_target - last_sent_target) > CMD_TOLERANCE
            timeout = (now - last_sent_time) > HEARTBEAT_TIME
            
            if moved or timeout:
                node.send_command(full_target)
                last_sent_target = full_target.copy()
                last_sent_time = now
            
            # 7. UI
            if now - last_ui_update > 0.1:
                warnings = check_limits(full_target)
                print_interface(current_mode, target_pos_xyz, target_d0, 
                              node.current_pos, node.current_joints[4]/1000.0, node.current_joints, 
                              full_target, np.zeros(3), parallel_mode, gripper_pct, warnings, waypoints, replay_index, recording_continuous, message)
                last_ui_update = now
            
            elapsed = time.time() - loop_start
            sleep_time = DT - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

    except KeyboardInterrupt:
        pass
    except Exception as e:
        restore_terminal_settings(old_settings)
        print(f"Error: {e}")
        return

    finally:
        restore_terminal_settings(old_settings)
        node.destroy_node()
        rclpy.shutdown()
        print("\nSaliendo...")

def clamp(x, a, b): return a if x < a else b if x > b else x

if __name__ == "__main__":
    main()
