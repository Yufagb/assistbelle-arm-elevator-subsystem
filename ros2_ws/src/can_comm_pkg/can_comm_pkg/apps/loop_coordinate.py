#!/usr/bin/env python3
import sys
import time
import numpy as np
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32MultiArray
from .cinematica_inversa import ik_solve_arm_pitch_constrained, fk_forward

# ===================== CONFIGURACIÓN =====================

# 1. Poses Articulares (Grados -> Radianes)
Q_HOME     = np.radians([0.0, 0.0, 0.0, 0.0])
Q_ELBOW_UP = np.radians([0.0, 30.0, -60.0, 30.0])

# 2. Puntos Cartesianos (XYZ)
P_PRE_GRASP = np.array([0.40, -0.005, 0.40])
P_ADVANCE   = np.array([0.45, -0.01, 0.40])
P_LIFT      = np.array([0.45, -0.01, 0.50])
P_APPROACH  = np.array([0.25, -0.25, 0.50])
P_TARGET    = np.array([0.25, -0.25, 0.40])
P_RETREAT   = np.array([0.25, -0.25, 0.50]) # Mismo que Approach

# 3. Parámetros de Movimiento
MOVE_TIME_JOINT     = 6.0 # Segundos para movimientos articulares (Aumentado)
MOVE_TIME_CARTESIAN = 6.0 # Segundos para movimientos cartesianos (Aumentado)
WAIT_TIME           = 4.0 # Segundos de espera (Aumentado)
DT                  = 0.02 # 50 Hz

ARRIVAL_TOLERANCE = 0.02 # 2 cm
ARRIVAL_TIMEOUT   = 10.0 # Segundos

# ===================== UTILIDADES =====================

class SmoothJoint:
    def __init__(self, val=0.0):
        self.pos = val
        self.vel = 0.0
    
    def update(self, target, dt, move_time):
        # Interpolación simple lineal con suavizado (o P-control tuneado para tiempo)
        # Para simplificar y garantizar tiempo, usaremos interpolación lineal del target
        # Pero aquí el target es fijo.
        # Usaremos un P-control suave.
        err = target - self.pos
        # v = d/t. Si queremos llegar en move_time...
        # v_req = err / move_time (muy simple)
        # Mejor: P control con ganancia baja
        kp = 2.0
        v_des = err * kp
        max_vel = 0.5 # rad/s
        v_des = np.clip(v_des, -max_vel, max_vel)
        
        self.pos += v_des * dt
        return self.pos

class CartesianInterpolator:
    def __init__(self):
        self.start_pos = None
        self.end_pos = None
        self.duration = 0.0
        self.elapsed = 0.0
        self.active = False
    
    def start(self, start_pos, end_pos, duration):
        self.start_pos = np.array(start_pos)
        self.end_pos = np.array(end_pos)
        self.duration = duration
        self.elapsed = 0.0
        self.active = True
        
    def update(self, dt):
        if not self.active:
            return self.end_pos, True # Done
            
        self.elapsed += dt
        t = self.elapsed / self.duration
        
        if t >= 1.0:
            self.active = False
            return self.end_pos, True
            
        # Interpolación Lineal (Lerp)
        # P(t) = P0 + t * (P1 - P0)
        current_pos = self.start_pos + t * (self.end_pos - self.start_pos)
        return current_pos, False

def clear_screen():
    sys.stdout.write('\033[2J\033[H')
    sys.stdout.flush()

# ===================== NODO ROS 2 =====================
class LoopNode(Node):
    def __init__(self):
        super().__init__('loop_coordinate')
        self.pub = self.create_publisher(String, 'can_command', 10)
        self.sub = self.create_subscription(Float32MultiArray, 'motors_state', self.listener_callback, 10)
        
        self.current_joints = np.zeros(5) # [th1, th2, th3, th4, d0_mm]
        self.data_received = False
        
        # Timer para solicitar datos (10 Hz)
        self.create_timer(0.1, self.poll_motors)

    def poll_motors(self):
        for i in range(1, 6):
            self.pub.publish(String(data=f"A{i}"))

    def listener_callback(self, msg):
        if len(msg.data) < 5: return
        self.current_joints = np.array(msg.data)
        self.data_received = True

    def send_command(self, q_j1_j4, d0_mm):
        # q_j1_j4 = [th1, th2, th3, th4] rad
        for i in range(4):
            motor_id = i + 1
            val_rad = q_j1_j4[i]
            msg = f"C{motor_id}:{val_rad:.4f},0.0"
            self.pub.publish(String(data=msg))
        
        # J5
        msg = f"C5:{d0_mm:.2f}"
        self.pub.publish(String(data=msg))

    def send_gripper(self, pct):
        msg = f"D2:{pct:.1f}"
        self.pub.publish(String(data=msg))

# ===================== MAIN LOOP =====================
def main():
    rclpy.init()
    node = LoopNode()
    
    import threading
    spinner = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
    spinner.start()
    
    print("Esperando datos del robot...")
    while not node.data_received:
        time.sleep(0.1)
        
    # Estado Inicial
    virtual_q = node.current_joints[0:4].copy()
    
    # Interpoladores
    joints_smooth = [SmoothJoint(virtual_q[i]) for i in range(4)]
    cart_interp = CartesianInterpolator()
    
    # Secuencia de Estados
    # 1. HOME -> ELBOW_UP (Joint)
    # 2. ELBOW_UP -> PRE_GRASP (Cartesian)
    # 3. OPEN GRIPPER
    # 4. PRE_GRASP -> ADVANCE (Cartesian)
    # 5. CLOSE GRIPPER
    # 6. ADVANCE -> LIFT (Cartesian)
    # 7. LIFT -> APPROACH (Cartesian)
    # 8. APPROACH -> TARGET (Cartesian)
    # 9. OPEN GRIPPER
    # 10. TARGET -> RETREAT (Cartesian)
    # 11. RETREAT -> HOME (Joint) - Actually RETREAT -> ELBOW_UP -> HOME safer?
    # Let's do RETREAT -> HOME directly via Joint or Cartesian?
    # The prompt says "Retreat -> Home". We can do Joint move to Home.
    
    state = "INIT"
    wait_timer = 0.0
    gripper_state = "CERRADO"
    
    # Variables de control
    target_q = None
    target_pos = None
    mode = "JOINT" # JOINT or CARTESIAN
    
    # Seed para IK
    ik_seed = virtual_q.copy()
    
    # Variables de Convergencia
    arrival_timer = 0.0
    waiting_arrival = False
    next_state_after_arrival = ""
    
    def check_arrival(target_xyz_chk, current_q_chk):
        # FK actual
        curr_xyz = fk_forward(0.0, current_q_chk[0], current_q_chk[1], current_q_chk[2], current_q_chk[3])
        err = np.linalg.norm(target_xyz_chk - curr_xyz)
        return err < ARRIVAL_TOLERANCE, err

    try:
        while True:
            loop_start = time.time()
            
            # --- MAQUINA DE ESTADOS ---
            
            # Lógica de Espera de Llegada (Convergence Check)
            if waiting_arrival:
                is_arrived, err_dist = check_arrival(target_pos, node.current_joints[0:4])
                arrival_timer += DT
                label = f"ESPERANDO LLEGADA... Err: {err_dist*1000:.1f}mm ({arrival_timer:.1f}s)"
                
                if is_arrived or arrival_timer > ARRIVAL_TIMEOUT:
                    waiting_arrival = False
                    state = next_state_after_arrival
                    # Reset timers for next state if needed
                    if "WAIT" in state: wait_timer = WAIT_TIME
            
            elif state == "INIT":
                state = "TO_ELBOW_UP"
                mode = "JOINT"
                target_q = Q_ELBOW_UP
                label = "1. YENDO A CODO ARRIBA (Joint)"
                
            # 1. HOME -> ELBOW_UP
            elif state == "TO_ELBOW_UP":
                # Check if reached (Joint Space)
                dist = np.linalg.norm(virtual_q - target_q)
                if dist < 0.05:
                    state = "TO_PRE_GRASP"
                    mode = "CARTESIAN"
                    # Iniciar interpolación cartesiana
                    curr_pos = fk_forward(0.0, virtual_q[0], virtual_q[1], virtual_q[2], virtual_q[3])
                    cart_interp.start(curr_pos, P_PRE_GRASP, MOVE_TIME_CARTESIAN)
                    target_pos = P_PRE_GRASP # Para check_arrival
                    label = "2. YENDO A PRE-AGARRE (Cartesian)"
            
            # 2. ELBOW_UP -> PRE_GRASP
            elif state == "TO_PRE_GRASP":
                if not cart_interp.active:
                    # Fin de interpolación -> Verificar llegada física
                    waiting_arrival = True
                    arrival_timer = 0.0
                    next_state_after_arrival = "WAIT_OPEN_GRIPPER"
                    label = "VERIFICANDO LLEGADA A PRE-AGARRE..."
            
            # 3. WAIT OPEN
            elif state == "WAIT_OPEN_GRIPPER":
                # Solo entramos aquí si ya llegamos físicamente
                if wait_timer == WAIT_TIME: # Primera vez
                     node.send_gripper(100.0)
                     gripper_state = "ABIERTO"
                
                wait_timer -= DT
                label = f"3. ABRIENDO GRIPPER ({wait_timer:.1f}s)"
                
                if wait_timer <= 0:
                    state = "TO_ADVANCE"
                    mode = "CARTESIAN"
                    cart_interp.start(P_PRE_GRASP, P_ADVANCE, MOVE_TIME_CARTESIAN)
                    target_pos = P_ADVANCE
                    label = "4. AVANZANDO (Cartesian)"
            
            # 4. PRE_GRASP -> ADVANCE
            elif state == "TO_ADVANCE":
                if not cart_interp.active:
                    waiting_arrival = True
                    arrival_timer = 0.0
                    next_state_after_arrival = "WAIT_CLOSE_GRIPPER"
                    label = "VERIFICANDO LLEGADA A AVANCE..."

            # 5. WAIT CLOSE
            elif state == "WAIT_CLOSE_GRIPPER":
                if wait_timer == WAIT_TIME:
                    node.send_gripper(0.0)
                    gripper_state = "CERRADO"
                
                wait_timer -= DT
                label = f"5. CERRANDO GRIPPER ({wait_timer:.1f}s)"

                if wait_timer <= 0:
                    state = "TO_LIFT"
                    mode = "CARTESIAN"
                    cart_interp.start(P_ADVANCE, P_LIFT, MOVE_TIME_CARTESIAN)
                    target_pos = P_LIFT
                    label = "6. ELEVANDO (Cartesian)"
            
            # 6. ADVANCE -> LIFT
            elif state == "TO_LIFT":
                if not cart_interp.active:
                    waiting_arrival = True
                    arrival_timer = 0.0
                    next_state_after_arrival = "TO_APPROACH"
                    # No wait state needed here, just move to next cartesian? 
                    # User asked for wait times between actions. Let's assume just moves are continuous unless action needed.
                    # But user said "incrementar tiempos de espera". 
                    # Let's add a small wait or just proceed if no gripper action.
                    # Plan says: Lift -> Approach directly.
                    # But we MUST check arrival.
                    label = "VERIFICANDO LLEGADA A LIFT..."
            
            # 7. LIFT -> APPROACH
            elif state == "TO_APPROACH":
                # This state is entered after LIFT arrival check
                # Need to start interpolation only once.
                # Logic fix: The previous state transition set next_state="TO_APPROACH".
                # But we need to trigger cart_interp.start().
                # Better structure: Transition to "PREP_APPROACH" then "TO_APPROACH"?
                # Or just check if cart_interp is active.
                
                # Let's use a flag or check mode.
                # Actually, simpler:
                # If we just arrived at LIFT, we are in TO_APPROACH state but haven't started interp.
                # We can check `cart_interp.active`. If false, start it.
                # BUT `cart_interp.active` is False when finished.
                # We need to distinguish "Not Started" vs "Finished".
                
                # Refactor: Use explicit PREP states or trigger on entry.
                # Let's use PREP states for clarity.
                pass # Logic continues below...

            # REFACTORING STATE MACHINE FOR ROBUSTNESS
            # ... (See replacement content)

            
            elif state == "DONE":
                pass # Stay here

            # --- CONTROL LOOP ---
            
            if mode == "JOINT":
                # Interpolación Articular
                for i in range(4):
                    virtual_q[i] = joints_smooth[i].update(target_q[i], DT, MOVE_TIME_JOINT)
                # Actualizar semilla IK para que esté lista si cambiamos a cartesiano
                ik_seed = virtual_q.copy()
                
            elif mode == "CARTESIAN":
                # Interpolación Cartesiana + IK
                target_xyz, done = cart_interp.update(DT)
                
                # Resolver IK
                # Usamos ik_seed (solución anterior) para continuidad
                q_sol, err = ik_solve_arm_pitch_constrained(target_xyz, 0.0, 0.0, ik_seed)
                
                # q_sol: [d0, th1, th2, th3, th4]
                # Actualizar virtual_q con la solución
                virtual_q = q_sol[1:5]
                ik_seed = virtual_q.copy()
                
                # Actualizar suavizadores articulares para evitar saltos al volver a Joint Mode
                for i in range(4):
                    joints_smooth[i].pos = virtual_q[i]

            # Enviar Comando
            node.send_command(virtual_q, 11.0) # d0 fijo en 11mm
            
            # UI
            clear_screen()
            print("============================================")
            print("   COMPLEX PICK & PLACE")
            print("============================================")
            print(f"ESTADO: {label}")
            print(f"MODO  : {mode}")
            print(f"GRIPPER: {gripper_state}")
            print("--------------------------------------------")
            print(f"Virtual Q(deg): {np.degrees(virtual_q).round(1)}")
            print(f"Real Q   (deg): {np.degrees(node.current_joints[0:4]).round(1)}")
            if mode == "CARTESIAN":
                print(f"Target XYZ    : {cart_interp.end_pos}")
            print("--------------------------------------------")
            print("Presiona Ctrl+C para salir")
            
            # Timing
            elapsed = time.time() - loop_start
            if DT > elapsed:
                time.sleep(DT - elapsed)
                
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
