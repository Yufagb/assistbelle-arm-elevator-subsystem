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

# Configuración inicial de pasos
DEFAULT_STEP_XYZ = 0.01  # 1 cm
DEFAULT_STEP_Z_ELEV = 0.01 # 1 cm

# Posición Home (Referencia visual, pero el comando será ceros)
HOME_XYZ = np.array([0.4, 0.0, 0.5])
HOME_J5 = 0.0

def get_key(timeout=0.1):
    """Lee una tecla con timeout. Retorna None si no hay tecla."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], timeout)
        if rlist:
            ch = sys.stdin.read(1)
        else:
            ch = None
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

class TeleopNodeSeparated(Node):
    def __init__(self):
        super().__init__('control_teclado_sistemas_separados')
        self.pub = self.create_publisher(String, 'can_command', 10)
        self.sub = self.create_subscription(Float32MultiArray, 'motors_state', self.listener_callback, 10)
        
        # Estado del robot
        self.current_pos = np.array([0.4, 0.0, 0.5]) # Default fallback
        self.current_joints = np.zeros(5) # [th1, th2, th3, th4, d0_mm]
        self.data_received = False
        
        self.get_logger().info("Esperando datos de encoders...")
        
        # Timer para solicitar posiciones (10 Hz)
        self.timer = self.create_timer(0.1, self.poll_motors)

    def poll_motors(self):
        for i in range(1, 6):
            self.pub.publish(String(data=f"A{i}"))

    def listener_callback(self, msg):
        if len(msg.data) < 5: return
        
        # Guardar joints actuales
        # msg.data: [th1, th2, th3, th4, d0_mm]
        self.current_joints = np.array(msg.data)
        
        # Calcular FK para actualizar posición actual
        th1, th2, th3, th4 = msg.data[0], msg.data[1], msg.data[2], msg.data[3]
        d0_m = msg.data[4] / 1000.0
        
        pos = fk_forward(d0_m, th1, th2, th3, th4)
        self.current_pos = np.array(pos)
        
        if not self.data_received:
            self.get_logger().info(f"Datos recibidos. Posición inicial: {self.current_pos}")
            self.data_received = True

    def send_command(self, q_sol, verbose=True):
        # q_sol = [d0_m, th1, th2, th3, th4]
        
        # Validar NaNs
        if np.isnan(q_sol).any():
            self.get_logger().error(f"INTENTO DE ENVIAR NaNs: {q_sol}")
            return

        # Primero J1-J4 (Brazo)
        for i in range(1, 5):
            # q_sol indices: 1->J1, 2->J2, 3->J3, 4->J4
            val_rad = q_sol[i]
            msg = f"C{i}:{val_rad:.4f},0.0"
            if verbose:
                self.get_logger().info(f"TX: {msg}") # DEBUG
            self.pub.publish(String(data=msg))
            time.sleep(0.005) # 5ms delay (más rápido)

        # Luego J5 (Ascensor)
        val_j5_mm = q_sol[0] * 1000.0
        msg = f"C5:{val_j5_mm:.2f}"
        if verbose:
            self.get_logger().info(f"TX: {msg}") # DEBUG
        self.pub.publish(String(data=msg))
        time.sleep(0.005)

    def send_gripper(self, pct):
        msg = f"D2:{pct:.1f}"
        self.pub.publish(String(data=msg))

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_interface(mode, target_pos, target_d0, real_pos, real_d0, real_joints, target_joints, 
                    step_xyz, step_elev, error_val, parallel_mode, gripper_pct, message=""):
    clear_screen()
    print("============================================")
    print("   CONTROL TECLADO - SISTEMAS SEPARADOS")
    print("============================================")
    print(f"MODO ACTUAL: {mode}")
    print("--------------------------------------------")
    print(f"PASOS DE MOVIMIENTO:")
    print(f"  XYZ: {step_xyz:.3f} m  (Ajustar con +/-)")
    print(f"  Elev: {step_elev:.3f} m")
    print("--------------------------------------------")
    print("ESTADO CARTESIANO:")
    print(f"  Target XYZ : [{target_pos[0]:.3f}, {target_pos[1]:.3f}, {target_pos[2]:.3f}]")
    print(f"  Real XYZ   : [{real_pos[0]:.3f}, {real_pos[1]:.3f}, {real_pos[2]:.3f}]")
    print(f"  ERROR POS  : {error_val:.4f} m")
    print("--------------------------------------------")
    print("ESTADO ARTICULAR (Target | Real):")
    
    # J5 (Ascensor)
    t_j5_mm = target_joints[0] * 1000.0
    r_j5_mm = real_joints[4]
    print(f"  J5 (Elev): {t_j5_mm:6.1f} mm | {r_j5_mm:6.1f} mm")
    
    # J1-J4 (Grados)
    t_degs = np.rad2deg(target_joints[1:5])
    r_degs = np.rad2deg(real_joints[0:4])
    
    print(f"  J1 (Base): {t_degs[0]:6.1f}°  | {r_degs[0]:6.1f}°")
    print(f"  J2 (Homb): {t_degs[1]:6.1f}°  | {r_degs[1]:6.1f}°")
    print(f"  J3 (Codo): {t_degs[2]:6.1f}°  | {r_degs[2]:6.1f}°")
    print(f"  J4 (Muñe): {t_degs[3]:6.1f}°  | {r_degs[3]:6.1f}°")
    print("--------------------------------------------")
    print(f"ESTADO EXTRA:")
    mode_str = "PARALELO AL PISO" if parallel_mode else "LIBRE"
    print(f"  Modo J4   : {mode_str}")
    print(f"  Gripper   : {gripper_pct:.0f}%")
    print("--------------------------------------------")
    print("COMANDOS DISPONIBLES:")
    print("  [m]   : Cambiar Modo (ELEV -> ARM -> WRIST -> CAM)")
    
    if mode == 'ELEVATOR':
        print("  [w/s] : Subir/Bajar Ascensor (J5)")
    elif mode == 'ARM':
        print("  [w/s] : +/- X (Adelante/Atrás Global)")
        print("  [a/d] : +/- Y (Izq/Der Global)")
        print("  [q/e] : +/- Z (Arriba/Abajo Global)")
    elif mode == 'WRIST':
        print("  [w/s] : +/- Pitch Muñeca (J4)")
    elif mode == 'CAMERA':
        print("  [w/s] : Arriba/Abajo (Eje Z Global)")
        print("  [a/d] : Izquierda/Derecha (Lateral Cámara)")
        print("  [q/e] : Acercar/Alejar (Profundidad Cámara)")
        
    print("  [+/-] : Ajustar paso XYZ")
    print("  [r]   : Resetear Target a Real")
    print("  [h]   : HOME (Todo a 0)")
    print("  [l]   : Toggle Modo Paralelo J4")
    print("  [o/p] : Abrir/Cerrar Gripper")
    print("  [x]   : Salir")
    print("--------------------------------------------")
    if message:
        print(f"MSG: {message}")
    print("--------------------------------------------")
    print("Comando: ", end='', flush=True)

def main():
    rclpy.init()
    node = TeleopNodeSeparated()
    
    # Ejecutar nodo en background
    import threading
    spinner = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
    spinner.start()
    
    print("Esperando sincronización con encoders...")
    time.sleep(1.0)
    
    # Variables de estado
    current_mode = 'ELEVATOR' 
    step_xyz = DEFAULT_STEP_XYZ
    step_elev = DEFAULT_STEP_Z_ELEV
    
    # Lanzar rqt_image_view al inicio (una sola vez)
    print("Lanzando rqt_image_view...")
    try:
        import subprocess
        subprocess.Popen(['ros2', 'run', 'rqt_image_view', 'rqt_image_view'], 
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        node.get_logger().warn(f"No se pudo lanzar rqt: {e}")
    
    # Inicializar target con la posición actual
    if not node.data_received:
        print("ADVERTENCIA: No se han recibido datos de encoders. Usando posición por defecto.")
    
    last_target_pos = node.current_pos.copy()
    last_target_d0 = node.current_joints[4] / 1000.0
    
    # Para mostrar target joints, necesitamos calcularlos o guardarlos.
    # Inicialmente usamos los reales.
    # target_joints_full = [d0, th1, th2, th3, th4]
    last_target_joints_full = np.concatenate(([last_target_d0], node.current_joints[0:4]))
    
    parallel_mode = False
    gripper_pct = 0.0 # Asumimos cerrado o desconocido
    
    last_ui_update = 0
    last_command_time = 0
    message = "Listo. RQT lanzado."
    
    try:
        while True:
            # Calcular error actual
            real_pos = node.current_pos
            real_d0 = node.current_joints[4] / 1000.0
            real_joints = node.current_joints
            
            # Error XYZ
            error_val = np.linalg.norm(last_target_pos - real_pos)
            
            # Actualizar UI periódicamente o cuando haya mensaje
            if time.time() - last_ui_update > 0.2:
                print_interface(current_mode, last_target_pos, last_target_d0, 
                              real_pos, real_d0, real_joints, last_target_joints_full,
                              step_xyz, step_elev, error_val, parallel_mode, gripper_pct, message)
                last_ui_update = time.time()
                if time.time() - last_ui_update > 2.0: 
                    message = ""

            # Reenvío periódico de comandos (10 Hz) para asegurar llegada
            if time.time() - last_command_time > 0.1:
                if last_target_joints_full is not None:
                    node.send_command(last_target_joints_full, verbose=False)
                    last_command_time = time.time()

            key = get_key(timeout=0.1)
            if key is None:
                continue
            
            # Procesar teclas
            if key == 'x':
                break
            
            elif key == 'm':
                # Ciclo: ELEVATOR -> ARM -> WRIST -> CAMERA -> ELEVATOR
                if current_mode == 'ELEVATOR':
                    current_mode = 'ARM'
                elif current_mode == 'ARM':
                    current_mode = 'WRIST'
                elif current_mode == 'WRIST':
                    current_mode = 'CAMERA'
                elif current_mode == 'CAMERA':
                    current_mode = 'ELEVATOR'
                else:
                    current_mode = 'ELEVATOR'
                message = f"Modo cambiado a {current_mode}"
                continue
            
            # Tecla 'c' eliminada, ahora es parte del ciclo 'm'

            elif key == 'r':
                last_target_pos = node.current_pos.copy()
                # FIX J5: Usar el valor correcto del diccionario motor_states si existe
                # node.current_joints es [th1, th2, th3, th4, d0] ? No, miremos update_state
                # En update_state: self.current_joints = [th1, th2, th3, th4, d0]
                last_target_d0 = node.current_joints[4] / 1000.0
                last_target_joints_full = np.concatenate(([last_target_d0], node.current_joints[0:4]))
                message = "Target reseteado a posición real."
                continue
            
            elif key == 'h':
                # HOME: Todo a 0
                q_home = np.zeros(5) # [0,0,0,0,0]
                node.send_command(q_home)
                
                # Actualizar targets virtuales
                last_target_joints_full = q_home
                last_target_d0 = 0.0
                last_target_pos = fk_forward(*q_home) # XYZ resultante de todo 0
                
                message = "Enviando a HOME (Todo 0)..."
                continue

            elif key == 'l':
                parallel_mode = not parallel_mode
                message = f"Modo Paralelo: {'ACTIVADO' if parallel_mode else 'DESACTIVADO'}"
                continue
                
            elif key == 'o':
                gripper_pct = 100.0
                node.send_gripper(gripper_pct)
                message = "Abriendo Gripper..."
                continue
                
            elif key == 'p':
                gripper_pct = 0.0
                node.send_gripper(gripper_pct)
                message = "Cerrando Gripper..."
                continue
                
            elif key == '+':
                step_xyz += 0.005
                message = f"Paso XYZ aumentado a {step_xyz:.3f}"
                continue
                
            elif key == '-':
                step_xyz = max(0.001, step_xyz - 0.005)
                message = f"Paso XYZ reducido a {step_xyz:.3f}"
                continue

            # Movimiento
            move_requested = False
            q_sol = None
            
            # Copias temporales para calcular
            target_pos = last_target_pos.copy()
            target_d0 = last_target_d0
            
            if current_mode == 'ELEVATOR':
                if key == 'w': 
                    target_d0 += step_elev
                    move_requested = True
                    message = "Subiendo ascensor..."
                elif key == 's': 
                    target_d0 -= step_elev
                    move_requested = True
                    message = "Bajando ascensor..."
                
                if move_requested:
                    # Validar límites
                    if not (0.0 <= target_d0 <= 0.35):
                        message = f"Límite J5 alcanzado: {target_d0:.3f}"
                        move_requested = False
                    else:
                        # Solución: nuevo d0, mismos ángulos de brazo que target anterior
                        # last_target_joints_full = [d0, th1, th2, th3, th4]
                        q_sol = last_target_joints_full.copy()
                        q_sol[0] = target_d0

            elif current_mode == 'WRIST':
                # Control manual de J4 (Muñeca)
                step_j4_deg = 5.0 # 5 grados por toque
                step_j4_rad = np.deg2rad(step_j4_deg)
                
                current_j4 = last_target_joints_full[4] 
                
                if key == 'w': 
                    current_j4 += step_j4_rad
                    move_requested = True
                    message = "Subiendo muñeca (J4)..."
                elif key == 's': 
                    current_j4 -= step_j4_rad
                    move_requested = True
                    message = "Bajando muñeca (J4)..."
                
                if move_requested:
                    if not (-np.pi <= current_j4 <= np.pi):
                         message = f"Límite J4 alcanzado: {np.rad2deg(current_j4):.1f}°"
                         move_requested = False
                    else:
                        q_sol = last_target_joints_full.copy()
                        q_sol[4] = current_j4

            elif current_mode == 'CAMERA':
                # Control Intuitivo de Cámara (Vectorial)
                # La cámara apunta en la dirección del brazo (determinado por J1/th1)
                # w/s -> Arriba/Abajo (J5 Elevador) - Eje Y Cámara (invertido en pantalla, pero intuitivo en 3D)
                # a/d -> Izquierda/Derecha (Perpendicular a J1) - Eje X Cámara
                # q/e -> Adelante/Atrás (Paralelo a J1) - Eje Z Cámara (Profundidad)
                
                # Obtener ángulo base actual (th1)
                # last_target_joints_full = [d0, th1, th2, th3, th4]
                th1 = last_target_joints_full[1]
                
                # Vectores de dirección
                # Forward (Adelante en el plano XY)
                # th1 es el ángulo de la base.
                # Si th1=0, el brazo apunta a X+. Forward es X+.
                dir_fwd_x = np.cos(th1)
                dir_fwd_y = np.sin(th1)
                
                # Right (Derecha en el plano XY)
                # Si th1=0 (X+), Right es Y- (d).
                # Vector perpendicular (-y, x) o (y, -x).
                # Rotación -90 deg: (x,y) -> (y, -x)
                dir_right_x = np.sin(th1)
                dir_right_y = -np.cos(th1)
                
                if key == 'w': # Arriba (Z Global)
                    target_pos[2] += step_xyz
                    move_requested = True
                    message = "Cámara ARRIBA (Z Global)"
                elif key == 's': # Abajo (Z Global)
                    target_pos[2] -= step_xyz
                    move_requested = True
                    message = "Cámara ABAJO (Z Global)"
                
                elif key == 'a': # Izquierda
                    target_pos[0] -= dir_right_x * step_xyz
                    target_pos[1] -= dir_right_y * step_xyz
                    move_requested = True
                    message = "Cámara IZQUIERDA"
                    
                elif key == 'd': # Derecha
                    target_pos[0] += dir_right_x * step_xyz
                    target_pos[1] += dir_right_y * step_xyz
                    move_requested = True
                    message = "Cámara DERECHA"

                elif key == 'q': # Adelante (Zoom In)
                    # Moverse en la dirección a la que apunta el brazo
                    target_pos[0] += dir_fwd_x * step_xyz
                    target_pos[1] += dir_fwd_y * step_xyz
                    move_requested = True
                    message = f"Cámara ADELANTE (Zoom In) [Dir: {dir_fwd_x:.2f}, {dir_fwd_y:.2f}]"
                    
                elif key == 'e': # Atrás (Zoom Out)
                    target_pos[0] -= dir_fwd_x * step_xyz
                    target_pos[1] -= dir_fwd_y * step_xyz
                    move_requested = True
                    message = "Cámara ATRÁS (Zoom Out)"

                # Lógica de resolución para CAMERA
                if move_requested:
                    # Validar J5 primero (si cambió)
                    if not (0.0 <= target_d0 <= 0.35):
                        message = f"Límite J5 alcanzado: {target_d0:.3f}"
                        move_requested = False
                        q_sol = None
                    else:
                        # Resolver IK para la nueva posición XYZ (target_pos) con el nuevo d0 (target_d0)
                        q0_arm = last_target_joints_full[1:5]
                        d0_fixed = target_d0
                        
                        # En MODO CAMERA, siempre forzamos Pitch=0 (Mirar adelante)
                        q_full, err = ik_solve_arm_pitch_constrained(target_pos, d0_fixed, pitch_goal=0.0, q0_arm=q0_arm)
                        
                        if err > 1e-2:
                            message = f"Inalcanzable (Err: {err:.4f})"
                            move_requested = False
                        else:
                            q_sol = q_full

            elif current_mode == 'ARM':
                if key == 'w': target_pos[0] += step_xyz; move_requested = True
                elif key == 's': target_pos[0] -= step_xyz; move_requested = True
                elif key == 'a': target_pos[1] += step_xyz; move_requested = True
                elif key == 'd': target_pos[1] -= step_xyz; move_requested = True
                elif key == 'q': target_pos[2] += step_xyz; move_requested = True
                elif key == 'e': target_pos[2] -= step_xyz; move_requested = True
                
                if move_requested:
                    message = "Calculando IK..."
                    # Resolver IK
                    q0_arm = last_target_joints_full[1:5] # th1..th4 actuales del target
                    d0_fixed = last_target_d0 # Mantenemos J5 fijo en modo ARM
                    
                    if parallel_mode:
                        # Usar IK 4DOF con Pitch Constrained (Pitch=0)
                        q_full, err = ik_solve_arm_pitch_constrained(target_pos, d0_fixed, pitch_goal=0.0, q0_arm=q0_arm)
                    else:
                        # Usar IK 4DOF normal
                        q_full, err = ik_solve_arm_only(target_pos, d0_fixed, q0_arm=q0_arm)
                    
                    if err > 1e-2: # 1cm tolerancia
                        message = f"Inalcanzable (Err: {err:.4f})"
                        move_requested = False
                    else:
                        q_sol = q_full

            if move_requested and q_sol is not None:
                # Enviar comando
                node.send_command(q_sol)
                
                # Actualizar estado target
                # IMPORTANTE: Siempre recalcular la posición Cartesiana (XYZ) basada en la solución Articular (q_sol)
                # Esto mantiene la consistencia si movimos solo una articulación (J1, J4, J5)
                # q_sol = [d0, th1, th2, th3, th4]
                
                last_target_d0 = q_sol[0]
                last_target_pos = fk_forward(q_sol[0], *q_sol[1:5])
                last_target_joints_full = q_sol
                
                message = "Comando enviado."
                # Forzar actualización de UI inmediata
                print_interface(current_mode, last_target_pos, last_target_d0, 
                              real_pos, real_d0, real_joints, last_target_joints_full,
                              step_xyz, step_elev, error_val, parallel_mode, gripper_pct, message)
                last_ui_update = time.time()

    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
        print("\nSaliendo...")

if __name__ == "__main__":
    main()
