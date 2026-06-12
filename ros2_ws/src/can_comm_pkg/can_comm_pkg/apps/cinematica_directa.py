#!/usr/bin/env python3
import numpy as np
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray, String

# ------------------ Forward Kinematics ------------------

def dh_matrix(theta, d, a, alpha):
    """
    Calcula la matriz de transformación homogénea para un eslabón usando parámetros DH.
    """
    ct, st = np.cos(theta), np.sin(theta)
    ca, sa = np.cos(alpha), np.sin(alpha)
    return np.array([
        [ ct, -st*ca,  st*sa, a*ct],
        [ st,  ct*ca, -ct*sa, a*st],
        [  0,     sa,     ca,    d ],
        [  0,      0,      0,    1 ],
    ], dtype=float)

# Geometría / offsets del robot (Actualizado)
# Orden: [Ascensor, Base, Link Fijo, Hombro, Codo, Muñeca]
# Variables: d0, th1, (fixed), th2, th3, th4
DH_PARAMS = [
    # 0: Ascensor (P)
    {"type": "P", "d": 0.4, "a": 0.0, "alpha": 0.0, "offset": 0.0, "invert": False},
    # 1: Base (R)
    {"type": "R", "d": 0.0, "a": 0.0, "alpha": np.deg2rad(-90), "offset": np.deg2rad(360), "invert": False},
    # 2: Link Fijo (R) - Fijo
    {"type": "R", "d": 0.1, "a": -0.02, "alpha": 0.0, "offset": np.deg2rad(180), "invert": True}, # Invert irrelevant if 0
    # 3: Hombro (R)
    {"type": "R", "d": 0.0, "a": 0.215, "alpha": 0.0, "offset": np.deg2rad(180), "invert": True},
    # 4: Codo (R)
    {"type": "R", "d": 0.0, "a": 0.25, "alpha": np.deg2rad(180), "offset": 0.0, "invert": True},
    # 5: Muñeca (R)
    {"type": "R", "d": 0.0, "a": 0.125, "alpha": np.deg2rad(90), "offset": 0.0, "invert": False}
]

def fk_forward(d0, th1, th2, th3, th4):
    """
    Devuelve posición cartesiana (x,y,z) del efector final.
    """
    # Mapeo de variables a los eslabones
    # Link Fijo (idx 2) es constante 0
    vars_list = [d0, th1, 0.0, th2, th3, th4]
    
    T = np.eye(4)
    
    for i, p in enumerate(DH_PARAMS):
        val = vars_list[i]
        
        # Lógica de inversión y offset
        if p["type"] == "P":
            # Prismática: d es variable + offset_d (aquí 'd' del param es el offset base)
            # Nota: En la tabla 'd' es 0.4. Asumimos d_total = val + p['d']
            d_val = val + p["d"]
            theta_val = p["offset"] # Usualmente 0 para prismática en theta
        else:
            # Rotacional
            d_val = p["d"]
            # Si invert es true, negamos la variable
            if p["invert"]:
                val = -val
            theta_val = val + p["offset"]
            
        T = T @ dh_matrix(theta_val, d_val, p["a"], p["alpha"])
        
    return T[:3,3]

class DirectKinematicsNode(Node):
    def __init__(self):
        super().__init__('cinematica_directa')
        self.sub = self.create_subscription(Float32MultiArray, 'motors_state', self.listener_callback, 10)
        self.pub_can = self.create_publisher(String, 'can_command', 10)
        self.timer = self.create_timer(0.1, self.poll_motors)
        self.get_logger().info("Nodo de Cinematica Directa iniciado. Escuchando 'motors_state' y sondeando motores...")

    def poll_motors(self):
        # Solicitar estado de los 5 motores (A1..A5)
        for i in range(1, 6):
            msg = String()
            msg.data = f"A{i}"
            self.pub_can.publish(msg)

    def listener_callback(self, msg):
        if len(msg.data) < 5:
            return
            
        # Asumiendo orden: [J1, J2, J3, J4, J5(mm)]
        # Pero can_slider.py dice: self.positions = [0.0]*5 # rad, rad, rad, rad, mm
        # Y en control_teclado.py enviamos: C1, C2, C3, C4, C5
        # Normalmente el array mantiene el orden de indices 0..4
        # J1=idx0, J2=idx1, J3=idx2, J4=idx3, J5=idx4
        
        th1 = msg.data[0]
        th2 = msg.data[1]
        th3 = msg.data[2]
        th4 = msg.data[3]
        d0_mm = msg.data[4]
        d0_m = d0_mm / 1000.0
        
        pos = fk_forward(d0_m, th1, th2, th3, th4)
        
        # Imprimir de forma limpia
        self.get_logger().info(
            f"Joints: [{th1:.3f}, {th2:.3f}, {th3:.3f}, {th4:.3f}, {d0_mm:.1f}] -> "
            f"Pos: [{pos[0]:.3f}, {pos[1]:.3f}, {pos[2]:.3f}]"
        )

def main(args=None):
    rclpy.init(args=args)
    node = DirectKinematicsNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
