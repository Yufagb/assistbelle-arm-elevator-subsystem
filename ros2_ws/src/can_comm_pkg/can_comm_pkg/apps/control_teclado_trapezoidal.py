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

# ===================== CONFIGURACIÓN =====================
# Velocidades Máximas (Target)
MAX_VEL_XYZ_M_S = 0.10   # 10 cm/s (Cartesiano) - Reducido para suavidad
MAX_VEL_ELEV_M_S = 0.10  # 10 cm/s (Elevador)
MAX_VEL_WRIST_RAD_S = 1.0 # ~60 deg/s

# Aceleraciones (Slew Rate Limits)
ACCEL_XYZ_M_S2 = 0.2     # 20 cm/s^2 - Reducido para suavidad
ACCEL_ELEV_M_S2 = 0.5
ACCEL_WRIST_RAD_S2 = 1.5 # Reducido

# Timeout para detener movimiento si no hay tecla
INPUT_TIMEOUT = 0.15 # segundos

# Frecuencia de Loop (Restaurada a 50Hz para suavidad)
LOOP_RATE = 50.0 # Hz
DT = 1.0 / LOOP_RATE

# Posición Home
HOME_XYZ = np.array([0.4, 0.0, 0.5])
HOME_J5 = 0.0

# Límites Articulares (Copiados de cinematica_inversa.py)
# Formato: (min, max)
JOINT_LIMITS = [
    (0.0, 0.35),                  # J5 (d0) [m]
    (np.deg2rad(-135), np.deg2rad(34)),  # J1 (th1)
    (np.deg2rad(-45), np.deg2rad(70)),   # J2 (th2)
    (np.deg2rad(-140), np.deg2rad(120)), # J3 (th3)
    (np.deg2rad(-180), np.deg2rad(180))  # J4 (th4)
]

JOINT_NAMES = ["J5 (Elev)", "J1 (Base)", "J2 (Homb)", "J3 (Codo)", "J4 (Muñe)"]

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
    """
    Verifica si alguna articulación está en (o excediendo) sus límites.
    q_full: [d0, th1, th2, th3, th4]
    Retorna lista de strings con advertencias.
    """
    warnings = []
    # Tolerancia pequeña para considerar que "tocó" el límite
    tol = 1e-3
    
    # Orden en q_full: d0, th1, th2, th3, th4
    # Orden en JOINT_LIMITS: d0, th1, th2, th3, th4
    
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

# ===================== CLASE NODO =====================
class TeleopNodeVelocity(Node):
    def __init__(self):
        super().__init__('control_teclado_trapezoidal') # Mismo nombre para no romper setup.py
        self.pub = self.create_publisher(String, 'can_command', 10)
        self.sub = self.create_subscription(Float32MultiArray, 'motors_state', self.listener_callback, 10)
        
        # Estado del robot
        self.current_pos = np.array([0.4, 0.0, 0.5]) 
        self.current_joints = np.zeros(5) # [th1, th2, th3, th4, d0_mm]
        self.data_received = False
        
        # Timer para solicitar posiciones (10 Hz)
        self.timer = self.create_timer(0.1, self.poll_motors)
        
        self.get_logger().info("Esperando datos de encoders...")

    def poll_motors(self):
        for i in range(1, 6):
            self.pub.publish(String(data=f"A{i}"))

    def listener_callback(self, msg):
        if len(msg.data) < 5: return
        
        # msg.data: [th1, th2, th3, th4, d0_mm]
        self.current_joints = np.array(msg.data)
        
        # Calcular FK
        th1, th2, th3, th4 = msg.data[0], msg.data[1], msg.data[2], msg.data[3]
        d0_m = msg.data[4] / 1000.0
        
        pos = fk_forward(d0_m, th1, th2, th3, th4)
        self.current_pos = np.array(pos)
        
        if not self.data_received:
            self.data_received = True

    def send_command(self, q_sol, vel_sol=None):
        # q_sol = [d0_m, th1, th2, th3, th4]
        if np.isnan(q_sol).any(): return

        # J1-J4 (Brazo)
        for i in range(1, 5):
            val_rad = q_sol[i]
            # vel_rad = vel_sol[i] if vel_sol is not None else 0.0
            # Enviamos solo posición por ahora para asegurar robustez, 
            # el driver interno del motor manejará el movimiento suave si los comandos son continuos
            msg = f"C{i}:{val_rad:.4f},0.0" 
            self.pub.publish(String(data=msg))
        
        # J5 (Ascensor)
        val_j5_mm = q_sol[0] * 1000.0
        msg = f"C5:{val_j5_mm:.2f}" 
        self.pub.publish(String(data=msg))

    def send_gripper(self, pct):
        msg = f"D2:{pct:.1f}"
        self.pub.publish(String(data=msg))

# ===================== UI & LOGIC =====================
def print_interface(mode, target_pos, target_d0, real_pos, real_d0, real_joints, target_joints, 
                    vel_vector, parallel_mode, gripper_pct, warnings, message=""):
    
    lines = []
    lines.append("============================================")
    lines.append("   CONTROL VELOCIDAD (JOGGING)")
    lines.append("============================================")
    lines.append(f"MODO ACTUAL: {mode}")
    
    # Instrucciones Dinámicas
    if mode == 'ELEVATOR':
        lines.append("  [w/s]: Subir/Bajar Ascensor")
    elif mode == 'ARM':
        lines.append("  [w/s]: X (Adelante/Atrás)")
        lines.append("  [a/d]: Y (Izquierda/Derecha)")
        lines.append("  [q/e]: Z (Arriba/Abajo)")
    elif mode == 'WRIST':
        lines.append("  [w/s]: Pitch Muñeca")
    elif mode == 'CAMERA':
        lines.append("  [w/s]: Arriba/Abajo (Global)")
        lines.append("  [a/d]: Izquierda/Derecha (Cam)")
        lines.append("  [q/e]: Zoom In/Out (Cam)")
        
    lines.append("--------------------------------------------")
    lines.append("VELOCIDAD OBJETIVO:")
    # Visualizar barra de velocidad
    v_norm = np.linalg.norm(vel_vector)
    bar_len = int(v_norm * 20) # Escala visual
    bar = "#" * bar_len
    lines.append(f"  [{bar:<20}] {v_norm:.2f}")
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
    
    # Advertencias de Límites
    if warnings:
        lines.append("\033[91mALERTA DE LIMITES:\033[0m") # Rojo
        for w in warnings:
            lines.append(f"  \033[93m{w}\033[0m") # Amarillo
        lines.append("--------------------------------------------")
    
    lines.append(f"  Modo J4   : {'PARALELO' if parallel_mode else 'LIBRE'}")
    lines.append(f"  Gripper   : {gripper_pct:.0f}%")
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
    node = TeleopNodeVelocity()
    
    import threading
    spinner = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
    spinner.start()
    
    print("Esperando sincronización...")
    time.sleep(1.0)
    
    # --- ESTADO DE CONTROL ---
    current_mode = 'ELEVATOR'
    parallel_mode = False
    gripper_pct = 0.0
    
    # --- ESTADO DE MOVIMIENTO ---
    # Target (Posición Virtual Integrada)
    if not node.data_received:
        print("WARN: Sin datos. Usando default.")
    
    # Inicializar Target con la posición actual real
    target_d0 = node.current_joints[4] / 1000.0
    target_joints_arm = node.current_joints[0:4] # th1..th4
    target_pos_xyz = node.current_pos.copy()
    
    # Limitadores de Velocidad (Slew Limiters)
    # Usamos un vector genérico de 3 o 4 dimensiones según el modo
    # XYZ: 3, Elev: 1, Wrist: 1
    slew_x = SlewLimiter(0.0)
    slew_y = SlewLimiter(0.0)
    slew_z = SlewLimiter(0.0)
    
    last_input_time = 0.0
    last_ui_update = 0
    message = "Listo. Mantén teclas para mover."
    
    # Estado de envío
    last_sent_target = np.zeros(5)
    last_sent_time = 0.0
    CMD_TOLERANCE = 1e-5 # Tolerancia muy fina para movimiento
    HEARTBEAT_TIME = 1.0 # Enviar cada 1s aunque no se mueva
    
    old_settings = save_terminal_settings()
    
    try:
        set_raw_mode()
        
        while True:
            loop_start = time.time()
            now = time.time()
            
            # 1. LEER INPUT
            key = None
            if is_data():
                key = sys.stdin.read(1)
                last_input_time = now
            
            # 2. PROCESAR COMANDOS DISCRETOS (Toggle)
            if key == 'x': break
            elif key == '\x03': break
            elif key == 'm':
                modes = ['ELEVATOR', 'ARM', 'WRIST', 'CAMERA']
                idx = modes.index(current_mode)
                current_mode = modes[(idx + 1) % len(modes)]
                message = f"Modo: {current_mode}"
                # Resetear velocidades al cambiar modo
                slew_x.val = 0.0; slew_y.val = 0.0; slew_z.val = 0.0
                
                # Sincronizar Target con Real para evitar saltos
                target_d0 = node.current_joints[4] / 1000.0
                target_joints_arm = node.current_joints[0:4]
                target_pos_xyz = node.current_pos.copy()

            elif key == 'l':
                parallel_mode = not parallel_mode
                message = f"Paralelo: {parallel_mode}"
            elif key == 'h': # HOME
                target_d0 = 0.0
                target_joints_arm = np.zeros(4)
                target_pos_xyz = fk_forward(0.0, *target_joints_arm)
                message = "Yendo a HOME..."
            elif key == 'o':
                gripper_pct = 100.0
                node.send_gripper(100.0)
            elif key == 'p':
                gripper_pct = 0.0
                node.send_gripper(0.0)
            
            # 3. DETERMINAR TARGET VELOCITY (Input Map)
            v_target = np.zeros(3) # [vx, vy, vz] genérico
            
            # Check Timeout (Auto-Stop)
            if now - last_input_time < INPUT_TIMEOUT:
                if key in ['w', 's', 'a', 'd', 'q', 'e']:
                    # Asignar velocidad según tecla
                    val = 1.0 
                    
                    if key == 'w': v_target[0] = val
                    elif key == 's': v_target[0] = -val
                    elif key == 'a': v_target[1] = val
                    elif key == 'd': v_target[1] = -val
                    elif key == 'q': v_target[2] = val
                    elif key == 'e': v_target[2] = -val
            
            # 4. ACTUALIZAR DINÁMICA (Slew Rate Limiter)
            # Escalar v_target por MAX_VEL según modo
            
            current_vel_vec = np.zeros(3)
            
            if current_mode == 'ELEVATOR':
                # Solo usamos v_target[0] (w/s)
                v_req = v_target[0] * MAX_VEL_ELEV_M_S
                v_act = slew_x.update(v_req, DT, ACCEL_ELEV_M_S2)
                
                # Integrar Posición
                target_d0 += v_act * DT
                target_d0 = clamp(target_d0, 0.0, 0.35)
                
                # Actualizar XYZ resultante (El brazo se mueve con el ascensor)
                target_pos_xyz = fk_forward(target_d0, *target_joints_arm)
                
                current_vel_vec[0] = v_act
                
            elif current_mode == 'WRIST':
                # Solo usamos v_target[0] (w/s) para Pitch J4
                v_req = v_target[0] * MAX_VEL_WRIST_RAD_S
                v_act = slew_x.update(v_req, DT, ACCEL_WRIST_RAD_S2)
                
                target_joints_arm[3] += v_act * DT
                target_joints_arm[3] = clamp(target_joints_arm[3], -np.pi, np.pi)
                
                # Actualizar XYZ resultante
                target_pos_xyz = fk_forward(target_d0, *target_joints_arm)
                current_vel_vec[0] = v_act

            elif current_mode == 'ARM':
                # XYZ Global
                req_vx = v_target[0] * MAX_VEL_XYZ_M_S
                req_vy = v_target[1] * MAX_VEL_XYZ_M_S
                req_vz = v_target[2] * MAX_VEL_XYZ_M_S
                
                act_vx = slew_x.update(req_vx, DT, ACCEL_XYZ_M_S2)
                act_vy = slew_y.update(req_vy, DT, ACCEL_XYZ_M_S2)
                act_vz = slew_z.update(req_vz, DT, ACCEL_XYZ_M_S2)
                
                target_pos_xyz[0] += act_vx * DT
                target_pos_xyz[1] += act_vy * DT
                target_pos_xyz[2] += act_vz * DT
                
                current_vel_vec = np.array([act_vx, act_vy, act_vz])
                
            elif current_mode == 'CAMERA':
                # XYZ Relativo a Base
                th1 = target_joints_arm[0]
                fwd = np.array([np.cos(th1), np.sin(th1), 0])
                right = np.array([np.sin(th1), -np.cos(th1), 0])
                up = np.array([0, 0, 1])
                
                # w/s -> Eje Z Global (Up/Down)
                v_local_up = v_target[0] * MAX_VEL_XYZ_M_S
                # a/d -> Eje Lateral (Right/Left)
                v_local_right = -v_target[1] * MAX_VEL_XYZ_M_S 
                # q/e -> Eje Frontal (Fwd/Back)
                v_local_fwd = v_target[2] * MAX_VEL_XYZ_M_S
                
                act_v_up = slew_x.update(v_local_up, DT, ACCEL_XYZ_M_S2)
                act_v_right = slew_y.update(v_local_right, DT, ACCEL_XYZ_M_S2)
                act_v_fwd = slew_z.update(v_local_fwd, DT, ACCEL_XYZ_M_S2)
                
                # Compose Global Velocity
                v_global = act_v_up * up + act_v_right * right + act_v_fwd * fwd
                
                target_pos_xyz += v_global * DT
                current_vel_vec = v_global

            # 5. RESOLVER IK (Si es necesario)
            if current_mode in ['ARM', 'CAMERA']:
                q0_seed = target_joints_arm
                if parallel_mode or current_mode == 'CAMERA':
                    q_sol, err = ik_solve_arm_pitch_constrained(target_pos_xyz, target_d0, 0.0, q0_seed)
                else:
                    q_sol, err = ik_solve_arm_only(target_pos_xyz, target_d0, q0_seed)
                
                # Si IK falla, revertir integración (Clamp implícito por no actualizar)
                if err < 0.05:
                    target_joints_arm = q_sol[1:5]
                else:
                    # Revertir target_pos_xyz para no acumular error
                    # (Opcional: implementar clamp de espacio de trabajo)
                    pass

            # 6. ENVIAR COMANDO (Smart Transmission)
            # Construir vector completo
            full_target = np.concatenate(([target_d0], target_joints_arm))
            
            # Condición: Se movió significativamente O pasó tiempo de heartbeat
            moved = np.linalg.norm(full_target - last_sent_target) > CMD_TOLERANCE
            timeout = (now - last_sent_time) > HEARTBEAT_TIME
            
            if moved or timeout:
                node.send_command(full_target)
                last_sent_target = full_target.copy()
                last_sent_time = now
            
            # 7. CHEQUEAR LIMITES Y ACTUALIZAR UI
            if now - last_ui_update > 0.1:
                # Verificar límites
                warnings = check_limits(full_target)
                
                print_interface(current_mode, target_pos_xyz, target_d0, 
                              node.current_pos, node.current_joints[4]/1000.0, node.current_joints, 
                              full_target, current_vel_vec, parallel_mode, gripper_pct, warnings, message)
                last_ui_update = now
            
            # Loop Timing
            elapsed = time.time() - loop_start
            sleep_time = DT - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

    except KeyboardInterrupt:
        pass
    except Exception as e:
        # Capturar errores para restaurar terminal
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
