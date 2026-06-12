#!/usr/bin/env python3
import sys
import tty
import termios
import numpy as np
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32MultiArray
from .cinematica_inversa import ik_solve_position, ik_solve_arm_only, fk_forward
import select
import time

# Configuración de pasos
STEP_XYZ = 0.01  # 1 cm
STEP_Z_ELEV = 0.01 # 1 cm

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

class TeleopNode4GDL(Node):
    def __init__(self):
        super().__init__('control_teclado_4gdl')
        self.pub = self.create_publisher(String, 'can_command', 10)
        self.sub = self.create_subscription(Float32MultiArray, 'motors_state', self.listener_callback, 10)
        
        # Estado del robot
        self.current_pos = np.array([0.4, 0.0, 0.5]) # Default fallback
        self.current_joints = np.zeros(5) # [th1, th2, th3, th4, d0_mm]
        self.data_received = False
        
        self.get_logger().info("Esperando datos de encoders...")

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

    def send_command(self, q_sol):
        # q_sol = [d0_m, th1, th2, th3, th4]
        
        # J5 (Ascensor)
        val_j5_mm = q_sol[0] * 1000.0
        msg = f"C5:{val_j5_mm:.2f}"
        self.get_logger().info(f"Publicando: {msg}")
        self.pub.publish(String(data=msg))
        time.sleep(0.02)
        
        # J1-J4
        for i in range(1, 5):
            # q_sol indices: 1->J1, 2->J2, 3->J3, 4->J4
            val_rad = q_sol[i]
            msg = f"C{i}:{val_rad:.4f},0.0"
            self.get_logger().info(f"Publicando: {msg}")
            self.pub.publish(String(data=msg))
            time.sleep(0.02)

def main():
    rclpy.init()
    node = TeleopNode4GDL()
    
    # Ejecutar nodo en background
    import threading
    spinner = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
    spinner.start()
    
    print("--- Control de Robot 4GDL + Ascensor ---")
    print("Modos:")
    print("  m   : Cambiar Modo (ASCENSOR <-> BRAZO)")
    print("Controles Comunes:")
    print("  x   : Salir")
    print("------------------------------------")
    print("Esperando sincronización con encoders...")
    
    time.sleep(1.0)
    if not node.data_received:
        print("ADVERTENCIA: No se han recibido datos de encoders. Usando posición por defecto.")

    # Modos: 'ELEVATOR', 'ARM'
    current_mode = 'ELEVATOR' 
    
    # Estado virtual para comandos rápidos
    last_target_pos = None
    last_target_d0 = None # Solo para modo ascensor
    last_command_time = 0

    try:
        last_print_time = 0
        while True:
            # Sincronización con realidad si pasa tiempo
            if time.time() - last_command_time > 2.0:
                last_target_pos = node.current_pos.copy()
                last_target_d0 = node.current_joints[4] / 1000.0
            
            # Inicialización
            if last_target_pos is None: last_target_pos = node.current_pos.copy()
            if last_target_d0 is None: last_target_d0 = node.current_joints[4] / 1000.0

            # Actualizar pantalla
            if time.time() - last_print_time > 0.5:
                real_pos = node.current_pos
                d0_real_mm = node.current_joints[4]
                
                mode_str = "[ASCENSOR]" if current_mode == 'ELEVATOR' else "[BRAZO 4GDL]"
                
                sys.stdout.write(f"\r{mode_str} RealXYZ:[{real_pos[0]:.2f}, {real_pos[1]:.2f}, {real_pos[2]:.2f}] J5:{d0_real_mm:.1f}mm | Cmd: ")
                sys.stdout.flush()
                last_print_time = time.time()
            
            key = get_key(timeout=0.1)
            if key is None:
                continue
            
            print(key) 

            if key == 'x':
                break
            elif key == 'm':
                current_mode = 'ARM' if current_mode == 'ELEVATOR' else 'ELEVATOR'
                print(f"\n>>> CAMBIO DE MODO A: {current_mode} <<<")
                # Resincronizar al cambiar de modo para evitar saltos
                last_target_pos = node.current_pos.copy()
                last_target_d0 = node.current_joints[4] / 1000.0
                continue

            # Lógica según modo
            q_sol = None
            target_pos = last_target_pos.copy()
            target_d0 = last_target_d0
            
            move_requested = False

            if current_mode == 'ELEVATOR':
                # Solo controla J5 (Z del ascensor)
                # w/s para subir/bajar ascensor
                if key == 'w': 
                    target_d0 += STEP_Z_ELEV
                    move_requested = True
                elif key == 's': 
                    target_d0 -= STEP_Z_ELEV
                    move_requested = True
                else:
                    print(" En modo Ascensor usa w/s.")
                    continue
                
                # En modo ascensor, mantenemos los ángulos actuales del brazo fijos
                # y solo cambiamos d0.
                # Pero necesitamos recalcular la XYZ resultante para mostrarla?
                # O simplemente mandamos el comando directo.
                # Para ser consistentes con send_command que pide q_sol completo:
                q_sol = np.concatenate(([target_d0], node.current_joints[0:4]))
                
                # Validar límites de J5 (0 a 0.35m)
                if not (0.0 <= target_d0 <= 0.35):
                    print(f" Límite de ascensor alcanzado: {target_d0:.3f}m")
                    # Revertir
                    target_d0 = last_target_d0
                    move_requested = False

            elif current_mode == 'ARM':
                # Controla X, Y, Z del efector, pero MANTENIENDO J5 FIJO
                # w/s: X, a/d: Y, q/e: Z
                if key == 'w': target_pos[0] += STEP_XYZ; move_requested = True
                elif key == 's': target_pos[0] -= STEP_XYZ; move_requested = True
                elif key == 'a': target_pos[1] += STEP_XYZ; move_requested = True
                elif key == 'd': target_pos[1] -= STEP_XYZ; move_requested = True
                elif key == 'q': target_pos[2] += STEP_XYZ; move_requested = True
                elif key == 'e': target_pos[2] -= STEP_XYZ; move_requested = True
                
                if move_requested:
                    # Resolver IK 4GDL
                    # Semilla: joints actuales del brazo
                    q0_arm = node.current_joints[0:4] # th1..th4
                    
                    # Usamos el d0 ACTUAL (fijo)
                    d0_fixed = node.current_joints[4] / 1000.0
                    
                    # Llamar a la nueva función IK
                    q_full, err = ik_solve_arm_only(target_pos, d0_fixed, q0_arm=q0_arm)
                    
                    if err > 5e-3: # Tolerancia un poco mayor
                        print(f" Objetivo inalcanzable con brazo fijo (Err: {err:.4f})")
                        move_requested = False
                    else:
                        q_sol = q_full

            if move_requested and q_sol is not None:
                # Mostrar propuesta
                d0_mm = q_sol[0] * 1000.0
                th_deg = np.rad2deg(q_sol[1:5])
                
                print("-" * 30)
                print(f"Propuesta ({current_mode}):")
                if current_mode == 'ARM':
                    print(f"  Destino XYZ: [{target_pos[0]:.3f}, {target_pos[1]:.3f}, {target_pos[2]:.3f}]")
                else:
                    print(f"  Destino J5: {d0_mm:.1f} mm")
                    
                print(f"  Joints: [J5:{d0_mm:.1f}, J1:{th_deg[0]:.1f}, J2:{th_deg[1]:.1f}, J3:{th_deg[2]:.1f}, J4:{th_deg[3]:.1f}]")
                print("Confirmar? [ENTER]: ", end='', flush=True)
                
                confirm = None
                while confirm is None:
                    confirm = get_key(timeout=0.1)
                
                if confirm == '\r' or confirm == '\n':
                    print("SI -> Enviando")
                    node.send_command(q_sol)
                    
                    # Actualizar estados virtuales
                    if current_mode == 'ELEVATOR':
                        last_target_d0 = target_d0
                        # Al mover J5, la posición XYZ cambia, actualizamos last_target_pos con FK
                        last_target_pos = fk_forward(target_d0, *q_sol[1:5])
                    else:
                        last_target_pos = target_pos
                        # J5 no cambia
                    
                    last_command_time = time.time()
                    time.sleep(0.1)
                else:
                    print("NO")

            last_print_time = 0

    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
