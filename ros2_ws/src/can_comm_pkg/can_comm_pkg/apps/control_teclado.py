#!/usr/bin/env python3
import sys
import tty
import termios
import numpy as np
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32MultiArray
from .cinematica_inversa import ik_solve_position, fk_forward

# Configuración de pasos
STEP = 0.01  # 1 cm por pulsación

import select

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

class TeleopNode(Node):
    def __init__(self):
        super().__init__('control_teclado')
        self.pub = self.create_publisher(String, 'can_command', 10)
        self.sub = self.create_subscription(Float32MultiArray, 'motors_state', self.listener_callback, 10)
        
        # Estado del robot
        self.current_pos = np.array([0.4, 0.0, 0.5]) # Default fallback
        self.current_joints = np.zeros(5)
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
        import time
        
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
    node = TeleopNode()
    
    # Ejecutar nodo en background para recibir callbacks
    import threading
    spinner = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
    spinner.start()
    
    print("--- Control de Robot por Teclado (Interactivo) ---")
    print("Controles:")
    print("  w/s : +/- X")
    print("  a/d : +/- Y")
    print("  q/e : +/- Z")
    print("  x   : Salir")
    print("------------------------------------")
    print("Esperando sincronización con encoders...")
    
    import time
    time.sleep(1.0)
    if not node.data_received:
        print("ADVERTENCIA: No se han recibido datos de encoders. Usando posición por defecto.")

    try:
        last_print_time = 0
        # Usamos last_target_pos para encadenar comandos sin esperar al lag de los encoders
        last_target_pos = None
        last_command_time = 0
        
        while True:
            # Sincronizar last_target_pos con la realidad si ha pasado tiempo sin comandos (ej. 2s)
            # o si es la primera vez
            if last_target_pos is None or (time.time() - last_command_time > 2.0):
                last_target_pos = node.current_pos.copy()

            # Actualizar pantalla cada 0.5s si no hay input
            if time.time() - last_print_time > 0.5:
                real_pos = node.current_pos
                # Mostrar tanto la Real como la "Virtual" (donde creemos que estamos/vamos)
                sys.stdout.write(f"\rReal: [{real_pos[0]:.3f}, {real_pos[1]:.3f}, {real_pos[2]:.3f}] | Virt: [{last_target_pos[0]:.3f}, {last_target_pos[1]:.3f}, {last_target_pos[2]:.3f}] Cmd: ")
                sys.stdout.flush()
                last_print_time = time.time()
            
            key = get_key(timeout=0.1)
            if key is None:
                continue
            
            print(key) # Echo del caracter presionado
            
            # Calculamos el nuevo target BASADO EN EL ÚLTIMO TARGET (para permitir pulsaciones rápidas)
            target_pos = last_target_pos.copy()
            
            if key == 'w': target_pos[0] += STEP
            elif key == 's': target_pos[0] -= STEP
            elif key == 'a': target_pos[1] += STEP
            elif key == 'd': target_pos[1] -= STEP
            elif key == 'q': target_pos[2] += STEP
            elif key == 'e': target_pos[2] -= STEP
            elif key == 'x': break
            else: continue
            
            # Resolver IK para el objetivo
            q_seed = [
                node.current_joints[4]/1000.0, 
                node.current_joints[0], 
                node.current_joints[1], 
                node.current_joints[2], 
                node.current_joints[3]
            ]
            
            q_sol, err = ik_solve_position(target_pos, q0=q_seed)
            
            if err > 1e-3:
                print(f"¡Objetivo inalcanzable! Error: {err:.4f}")
                continue
                
            # Mostrar propuesta
            d0_mm = q_sol[0] * 1000.0
            th_deg = np.rad2deg(q_sol[1:5])

            print("-" * 30)
            print(f"Propuesta de Movimiento:")
            print(f"  Destino XYZ: [{target_pos[0]:.3f}, {target_pos[1]:.3f}, {target_pos[2]:.3f}]")
            print(f"  Joints Calc: [Asc(J5): {d0_mm:.1f}mm, J1: {th_deg[0]:.1f}°, J2: {th_deg[1]:.1f}°, J3: {th_deg[2]:.1f}°, J4: {th_deg[3]:.1f}°]")
            print("-" * 30)
            print("¿Confirmar movimiento? [ENTER = Sí, Otro = No]: ", end='', flush=True)
            
            confirm = None
            while confirm is None:
                confirm = get_key(timeout=0.1)
            
            if confirm == '\r' or confirm == '\n':
                print("SI")
                print("Enviando comando...")
                node.send_command(q_sol)
                # Actualizamos last_target_pos y el tiempo
                last_target_pos = target_pos
                last_command_time = time.time()
                time.sleep(0.2)
            else:
                print("NO")
                print("Cancelado.")
            
            # Forzar reimpresión inmediata del estado
            last_print_time = 0

    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
