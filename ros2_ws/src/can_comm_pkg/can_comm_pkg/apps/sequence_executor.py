#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32MultiArray
import numpy as np
import time
from can_comm_pkg.apps.cinematica_inversa import ik_solve_position, fk_forward, ik_solve_arm_only

# --- Trajectory Generator (Copied from can_traj.py) ---
def vel_trapezoidal(q0, qf, tf, tb, t):
    """
    Generador Trapezoidal (LSPB).
    Calcula q, dq, ddq para un instante t.
    dqmax se calcula automáticamente para cumplir con tf y tb.
    """
    dist = qf - q0
    if abs(dist) < 1e-6:
        return qf, 0.0, 0.0
    
    # Calcular velocidad de crucero necesaria para llegar en tf con rampas de tb
    # Area = dq_cruise * (tf - tb) = dist
    # dq_cruise = dist / (tf - tb)
    
    # Validar tb
    if tb * 2 > tf:
        tb = tf / 2.0
        
    dqmax = dist / (tf - tb)
    
    q, dq, ddq = 0.0, 0.0, 0.0
    
    if t < 0: return q0, 0, 0
    if t > tf: return qf, 0, 0
    
    if t <= tb:
        # Aceleración constante
        acc = dqmax / tb
        q = q0 + 0.5 * acc * t**2
        dq = acc * t
        ddq = acc
    elif t <= tf - tb:
        # Velocidad constante
        q = q0 + 0.5 * (dqmax / tb) * tb**2 + dqmax * (t - tb)
        # Simplificando: q0 + 0.5*dqmax*tb + dqmax*(t-tb)
        dq = dqmax
        ddq = 0.0
    else:
        # Desaceleración
        # Tiempo desde el inicio de la desaceleración
        td = t - (tf - tb)
        q_start_dec = q0 + 0.5 * dqmax * tb + dqmax * (tf - 2*tb)
        # q = qf - 0.5 * acc * (tf - t)^2
        acc = dqmax / tb
        t_rem = tf - t
        q = qf - 0.5 * acc * t_rem**2
        dq = acc * t_rem
        ddq = -acc
        
    return q, dq, ddq

class SequenceExecutor(Node):
    def __init__(self):
        super().__init__('sequence_executor')
        self.pub = self.create_publisher(String, 'can_command', 10)
        self.sub = self.create_subscription(Float32MultiArray, 'motors_state', self.listener_callback, 10)
        
        self.current_joints = np.zeros(5) # [th1, th2, th3, th4, d0_mm]
        self.data_received = False
        
        # Timer para solicitar estado (necesario para saber dónde estamos antes de mover)
        self.timer = self.create_timer(0.1, self.poll_motors)
        self.get_logger().info("Esperando datos del robot...")

    def poll_motors(self):
        for i in range(1, 6):
            self.pub.publish(String(data=f"A{i}"))

    def listener_callback(self, msg):
        if len(msg.data) < 5: return
        self.current_joints = np.array(msg.data)
        if not self.data_received:
            self.get_logger().info("Datos recibidos. Listo para ejecutar.")
            self.data_received = True

    def send_command(self, q_sol):
        # q_sol = [d0_m, th1, th2, th3, th4]
        # Enviar J1-J4
        for i in range(1, 5):
            val_rad = q_sol[i]
            msg = f"C{i}:{val_rad:.4f},0.0"
            self.pub.publish(String(data=msg))
            # time.sleep(0.002) 

        # Enviar J5
        val_j5_mm = q_sol[0] * 1000.0
        msg = f"C5:{val_j5_mm:.2f}"
        self.pub.publish(String(data=msg))

    def send_gripper(self, pct):
        msg = f"D2:{pct:.1f}"
        self.pub.publish(String(data=msg))
        self.get_logger().info(f"Gripper: {pct}%")

    def move_arm(self, target_arm_joints, duration=2.0):
        """Mueve solo J1-J4, manteniendo J5 actual."""
        while not self.data_received: rclpy.spin_once(self, timeout_sec=0.1)
        
        start_joints = np.zeros(5)
        start_joints[0] = self.current_joints[4] / 1000.0
        start_joints[1:5] = self.current_joints[0:4]
        
        # Target completo (J5 igual al inicio)
        target_full = start_joints.copy()
        target_full[1:5] = target_arm_joints
        
        self.get_logger().info(f"Moviendo BRAZO a: {target_arm_joints} en {duration}s")
        self._execute_trajectory(start_joints, target_full, duration)

    def move_elevator(self, target_d0, duration=2.0):
        """Mueve solo J5, manteniendo J1-J4 actuales."""
        while not self.data_received: rclpy.spin_once(self, timeout_sec=0.1)
        
        start_joints = np.zeros(5)
        start_joints[0] = self.current_joints[4] / 1000.0
        start_joints[1:5] = self.current_joints[0:4]
        
        # Target completo (Arm igual al inicio)
        target_full = start_joints.copy()
        target_full[0] = target_d0
        
        self.get_logger().info(f"Moviendo ASCENSOR a: {target_d0:.3f}m en {duration}s")
        self._execute_trajectory(start_joints, target_full, duration)

    def _execute_trajectory(self, start_q, end_q, duration):
        steps = int(duration * 50)
        dt = duration / steps
        tb = duration * 0.2
        
        for i in range(steps + 1):
            t = i * dt
            q_cmd = np.zeros(5)
            for j in range(5):
                q, _, _ = vel_trapezoidal(start_q[j], end_q[j], duration, tb, t)
                q_cmd[j] = q
            self.send_command(q_cmd)
            time.sleep(dt)
        self.send_command(end_q)
        time.sleep(0.2)

    def move_smart(self, target_joints, total_duration=4.0):
        """
        Decide el orden basado en la altura (J5).
        - Si sube (Target J5 > Current J5): Ascensor primero, luego Brazo.
        - Si baja (Target J5 < Current J5): Brazo primero, luego Ascensor.
        """
        while not self.data_received: rclpy.spin_once(self, timeout_sec=0.1)
        
        current_d0 = self.current_joints[4] / 1000.0
        target_d0 = target_joints[0]
        target_arm = target_joints[1:5]
        
        # Dividir tiempo
        duration_phase = total_duration / 2.0
        
        if target_d0 > current_d0 + 0.005: # Subiendo (con histéresis)
            self.get_logger().info("ESTRATEGIA: SUBIR -> Primero Ascensor, luego Brazo")
            self.move_elevator(target_d0, duration=duration_phase)
            self.move_arm(target_arm, duration=duration_phase)
        else: # Bajando o igual
            self.get_logger().info("ESTRATEGIA: BAJAR/IGUAL -> Primero Brazo, luego Ascensor")
            self.move_arm(target_arm, duration=duration_phase)
            self.move_elevator(target_d0, duration=duration_phase)

    def execute_sequence(self):
        # Esperar inicialización
        while not self.data_received:
            rclpy.spin_once(self, timeout_sec=0.1)
            
        self.get_logger().info("INICIANDO SECUENCIA...")
        
        # 1. HOME
        self.get_logger().info("PASO 1: HOME")
        home_joints = np.zeros(5)
        self.move_smart(home_joints, total_duration=4.0)
        time.sleep(1.0)
        
        # Definir puntos cartesianos
        p_pre_agarre = (0.311, -0.455, 0.454)
        p_agarre     = (0.311, -0.452, 0.429)
        p_final      = (-0.286, -0.427, 0.737)
        p_vision     = (-0.250, -0.391, 0.681)
        
        # 2. PRE-AGARRE (ASCENSOR PROHIBIDO -> Usar IK Arm Only con d0=0)
        self.get_logger().info(f"PASO 2: PRE-AGARRE {p_pre_agarre} (J5 Fijo)")
        # Asumimos d0=0 (Home)
        d0_fixed = 0.0
        q_pre_full, err = ik_solve_arm_only(p_pre_agarre, d0_fixed, q0_arm=None)
        if err > 0.02: self.get_logger().warn(f"IK Error alto: {err}")
        
        # move_arm espera [th1, th2, th3, th4]
        self.move_arm(q_pre_full[1:5], duration=3.0) # Solo mover brazo
        self.send_gripper(100.0) # Abrir
        time.sleep(1.0)
        
        # 3. AGARRE (ASCENSOR PROHIBIDO)
        self.get_logger().info(f"PASO 3: AGARRE {p_agarre} (J5 Fijo)")
        q_agarre_full, err = ik_solve_arm_only(p_agarre, d0_fixed, q0_arm=q_pre_full[1:5])
        if err > 0.02: self.get_logger().warn(f"IK Error alto: {err}")
        
        self.move_arm(q_agarre_full[1:5], duration=2.0) # Solo mover brazo
        self.send_gripper(0.0) # Cerrar
        time.sleep(1.0)
        
        # 4. FINAL (SUBIR ASCENSOR -> LUEGO BRAZO)
        self.get_logger().info(f"PASO 4: FINAL {p_final}")
        # Aquí sí usamos IK completa para encontrar el mejor d0
        q_final, err = ik_solve_position(p_final, q0=None) # q0=None para buscar mejor config global
        if err > 0.02: self.get_logger().warn(f"IK Error alto: {err}")
        
        # Secuencia estricta: Subir Ascensor -> Mover Brazo
        self.move_elevator(q_final[0], duration=2.0)
        self.move_arm(q_final[1:5], duration=3.0)
        
        self.send_gripper(100.0) # Abrir
        time.sleep(1.0)
        
        # 5. VISION
        self.get_logger().info(f"PASO 5: VISION {p_vision}")
        q_vision, err = ik_solve_position(p_vision, q0=q_final)
        if err > 0.02: self.get_logger().warn(f"IK Error alto: {err}")
        
        # Usar move_smart para decidir (probablemente bajará o se mantendrá)
        self.move_smart(q_vision, total_duration=4.0)
        time.sleep(2.0)
        
        # 6. HOME
        self.get_logger().info("PASO 6: REGRESO A HOME")
        self.move_smart(home_joints, total_duration=4.0)
        
        self.get_logger().info("SECUENCIA COMPLETADA.")

def main(args=None):
    rclpy.init(args=args)
    executor = SequenceExecutor()
    
    # Ejecutar secuencia en un hilo aparte para no bloquear el spin de ROS (si fuera necesario)
    # Pero aquí podemos intercalar spin_once dentro de las funciones de espera si hiciera falta.
    # Como move_to_joints tiene un loop con sleep, necesitamos asegurar que los callbacks se procesen.
    # La forma más simple es llamar a spin_once dentro del loop de trayectoria, 
    # pero move_to_joints ya hace sleeps.
    # Mejor: Ejecutar la secuencia y llamar spin_once periódicamente.
    
    try:
        executor.execute_sequence()
    except KeyboardInterrupt:
        pass
    finally:
        executor.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
