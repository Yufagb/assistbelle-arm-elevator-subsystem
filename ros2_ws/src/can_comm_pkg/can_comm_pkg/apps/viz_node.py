#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import String
import threading
import time

class VizNode(Node):
    def __init__(self):
        super().__init__('viz_node')
        
        # Publica joint_states para que robot_state_publisher mueva el robot en RViz
        self.pub_js = self.create_publisher(JointState, 'joint_states', 10)
        
        # Suscribe a can_command para interceptar las órdenes de los otros nodos
        self.sub_cmd = self.create_subscription(String, 'can_command', self.on_command, 10)
        
        # Estado actual (J1..J5)
        # J5 es prismático (m), J1-J4 revolute (rad)
        self.joints = {'J1': 0.0, 'J2': 0.0, 'J3': 0.0, 'J4': 0.0, 'J5': 0.0}
        
        self.get_logger().info("Viz Node Started. Listening to /can_command...")

        # Timer para publicar joint_states continuamente (necesario para RViz)
        self.timer = self.create_timer(0.1, self.publish_state)

    def on_command(self, msg):
        data = msg.data
        # Parsear comandos:
        # "C{idx}:{pos},{vel}" -> Rotacional
        # "C5:{pos}" -> Prismático
        
        try:
            if data.startswith('C'):
                parts = data.split(':')
                idx = int(parts[0][1:]) # C1 -> 1
                vals = parts[1].split(',')
                pos = float(vals[0])
                
                key = f"J{idx}"
                if key in self.joints:
                    # J5 viene en mm, convertir a metros para URDF
                    if idx == 5:
                        self.joints[key] = pos / 1000.0 
                    else:
                        self.joints[key] = pos # Radianes
                        
                    self.get_logger().info(f"Updated {key} to {self.joints[key]:.3f}")
                    
        except Exception as e:
            self.get_logger().error(f"Error parsing command: {e}")

    def publish_state(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = ['J1', 'J2', 'J3', 'J4', 'J5']
        msg.position = [
            self.joints['J1'],
            self.joints['J2'],
            self.joints['J3'],
            self.joints['J4'],
            self.joints['J5']
        ]
        self.pub_js.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = VizNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
