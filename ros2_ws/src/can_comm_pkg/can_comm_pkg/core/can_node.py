#!/usr/bin/env python3
import struct
from datetime import datetime

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from std_msgs.msg import String, Float32MultiArray
from sensor_msgs.msg import JointState

from .driver import CANDriver
from .message import CANMessage


class CANNode(Node):
    def __init__(self):
        super().__init__('can_node')
        self.driver = CANDriver('can0')

        # QoS un poco más holgado para tramas rápidas
        q_state = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=50
        )

        self.pub_state = self.create_publisher(Float32MultiArray, 'motors_state', q_state)
        self.pub_js    = self.create_publisher(JointState,        'joint_states', q_state)
        self.sub_cmd   = self.create_subscription(String, 'can_command', self.on_command, 10)

        # Bucle RX más rápido; dentro drenamos la cola
        self.timer_recv  = self.create_timer(0.01, self.receive_loop)   # 100 Hz
        # Publicación de respaldo por si no llegan frames durante un rato (opcional)
        self.timer_backup = self.create_timer(0.5, self.publish_state)

        # último estado conocido (pos, vel) por motor
        self.motor_states = {i: (0.0, 0.0) for i in range(1, 6)}
        self.joint_names  = ['joint1', 'joint2', 'joint3', 'joint4', 'prismatic']

        # Control de verbosidad para evitar frenar el bucle
        self.verbose_rx = False  # pon True si quieres ver cada trama

        self.get_logger().info('CANNode iniciado y suscrito a /can_command')

    # ------------------ TX ------------------
    def on_command(self, msg: String):
        raw = msg.data.strip()
        if ':' in raw:
            key, payload_txt = raw.split(':', 1)
        else:
            key, payload_txt = raw, ''

        if not key:
            self.get_logger().error("Comando vacío")
            return

        prefix = key[0].upper()  # 'A', 'B', 'C', 'D'
        motor  = int(key[1]) if len(key) > 1 and key[1].isdigit() else 0

        base_ids = {'A': 0xA0, 'B': 0xB0, 'C': 0xC0, 'D': 0xD0}
        
        if prefix not in base_ids:
            self.get_logger().error(f"Prefijo inválido en comando: {key}")
            return
        can_id = base_ids[prefix] | (motor & 0xF)

        payload = b''
        try:
            if prefix == 'B' and payload_txt:
                p, v = map(float, payload_txt.split(',', 1))
                payload = struct.pack('<ff', p, v)

            elif prefix == 'C':
                if motor == 5:
                    mm = float(payload_txt) if payload_txt else 0.0
                    payload = struct.pack('<f', mm)
                elif motor == 6:
                    if payload_txt.strip() == '':
                        payload = b'\x00'
                    else:
                        val = int(float(payload_txt))
                        if not (0 <= val <= 255):
                            raise ValueError("C6 requiere byte 0..255")
                        payload = bytes([val])
                else:
                    p, v = map(float, payload_txt.split(',', 1))
                    payload = struct.pack('<ff', p, v)
            elif prefix == 'D':
                pct = float(payload_txt) if payload_txt else 0.0
                payload = struct.pack('<f', pct)
            

            # 'A' no lleva payload

        except ValueError:
            self.get_logger().error(f"Payload inválido para {key}: '{payload_txt}'")
            return

        # Nota: log corto para no frenar IO
        self.get_logger().info(f"TX 0x{can_id:02X} DLC={len(payload)}")
        self.driver.send(CANMessage(can_id, payload))

    # ------------------ RX + publicación inmediata ------------------
    def receive_loop(self):
        """Lee todos los frames disponibles y publica al instante si llegan lecturas (0xB)."""
        while True:
            try:
                msg = self.driver.receive()
            except BlockingIOError:
                break  # no hay más en el buffer

            mid    = msg.can_id
            action = (mid >> 4) & 0xF
            motor  = mid & 0xF
            raw    = msg.payload

            if self.verbose_rx:
                now = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                self.get_logger().info(f"{now} | RX ID=0x{mid:02X} act=0x{action:X} m={motor} dlc={msg.dlc}")

            if action == 0xB and 1 <= motor <= 5:
                if len(raw) >= 8:
                    pos, vel = struct.unpack('<ff', raw[:8])
                    self.motor_states[motor] = (pos, vel)
                    # Publica inmediatamente para minimizar latencia
                    self._publish_state_now()
                # si len<8 lo ignoramos (ACK corto)

            elif action == 0xC:
                # mensajes de setpoint/ACK, no actualizan estado
                pass

            else:
                # otros tipos, opcional
                pass

    # ------------------ Publicación ------------------
    def _publish_state_now(self):
        data = [self.motor_states[i][0] for i in range(1, 6)] + \
               [self.motor_states[i][1] for i in range(1, 6)]
        self.pub_state.publish(Float32MultiArray(data=data))

        js = JointState()
        js.header.stamp = self.get_clock().now().to_msg()
        js.name     = self.joint_names
        js.position = [self.motor_states[i][0] for i in range(1, 6)]
        js.velocity = [self.motor_states[i][1] for i in range(1, 6)]
        self.pub_js.publish(js)

    def publish_state(self):
        """Respaldo periódico (por si no hubo RX recientemente)."""
        self._publish_state_now()


def main(args=None):
    rclpy.init(args=args)
    node = CANNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
