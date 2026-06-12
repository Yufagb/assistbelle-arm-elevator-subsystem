import sys
import os
from unittest.mock import MagicMock

# Mock socket module to bypass CAN hardware requirement
mock_socket = MagicMock()
sys.modules['socket'] = mock_socket
mock_socket.AF_CAN = 0
mock_socket.SOCK_RAW = 0
mock_socket.CAN_RAW = 0

# Add package to path
sys.path.append('/home/rosario/robot-project/ros2_ws/src/can_comm_pkg')

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

# Import the node class
try:
    from can_comm_pkg.can_node import CANNode
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

def test():
    rclpy.init()
    try:
        print("Instantiating CANNode...")
        node = CANNode()
        # Mock the driver instance to prevent any calls
        node.driver = MagicMock()
        
        print("Creating test listener...")
        test_node = Node('test_listener')
        received = []
        def cb(msg):
            received.append(msg)
        
        test_node.create_subscription(JointState, 'joint_states', cb, 10)
        
        # Wait for pub/sub connection (simulated)
        # In local process, it might need a bit of spinning
        
        print("Triggering publish...")
        # Manually trigger the publish method
        node._publish_state_now()
        
        print("Spinning...")
        # Spin a few times to process callbacks
        for _ in range(20):
            rclpy.spin_once(node, timeout_sec=0.01)
            rclpy.spin_once(test_node, timeout_sec=0.01)
            
        if received:
            print("\nVERIFICATION SUCCESS: JointState message received!")
            msg = received[0]
            print(f"Header Stamp: {msg.header.stamp}")
            print(f"Names: {msg.name}")
            print(f"Position: {msg.position}")
            print(f"Velocity: {msg.velocity}")
        else:
            print("\nVERIFICATION FAILED: No message received.")
            
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        rclpy.shutdown()

if __name__ == '__main__':
    test()
