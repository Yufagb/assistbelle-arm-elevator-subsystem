#!/usr/bin/env python3
import time
import struct
import threading
import rclpy
from rclpy.node import Node
from can_comm_pkg.core.driver import CANDriver
from can_comm_pkg.core.message import CANMessage

class DebugAxBxNode(Node):
    def __init__(self):
        super().__init__('debug_ax_bx')
        
        # Intentar conectar al driver CAN
        try:
            self.driver = CANDriver('can0')
            self.get_logger().info("Driver CAN conectado en can0")
        except Exception as e:
            self.get_logger().error(f"No se pudo conectar al driver CAN: {e}")
            self.driver = None
            return

        # Contadores
        # Keys: 1..5 (Motor ID)
        self.tx_count = {i: 0 for i in range(1, 6)}
        self.rx_count = {i: 0 for i in range(1, 6)}
        
        self.running = True
        
        # Thread para enviar (TX)
        self.thread_tx = threading.Thread(target=self.tx_loop)
        self.thread_tx.start()
        
        # Thread para recibir (RX)
        self.thread_rx = threading.Thread(target=self.rx_loop)
        self.thread_rx.start()
        
        # Timer para imprimir stats (1 Hz)
        self.timer_stats = self.create_timer(1.0, self.print_stats)
        
        self.get_logger().info("Iniciando debug AX -> BX...")

    def tx_loop(self):
        """Envía comandos A1..A5 periódicamente."""
        while self.running and rclpy.ok():
            if self.driver:
                for motor_id in range(1, 6):
                    # Construir ID: 0xA0 | motor_id
                    can_id = 0xA0 | motor_id
                    # Payload vacío para 'A'
                    msg = CANMessage(can_id, b'')
                    try:
                        self.driver.send(msg)
                        self.tx_count[motor_id] += 1
                    except Exception as e:
                        self.get_logger().warn(f"Error TX motor {motor_id}: {e}")
            
            # Frecuencia de envío: ~10Hz por motor (ajustable)
            time.sleep(0.1)

    def rx_loop(self):
        """Lee mensajes del bus y cuenta los BX."""
        while self.running and rclpy.ok():
            if self.driver:
                try:
                    msg = self.driver.receive()
                    mid = msg.can_id
                    action = (mid >> 4) & 0xF
                    motor = mid & 0xF
                    
                    # Si es respuesta de estado (0xB) y motor válido
                    if action == 0xB and 1 <= motor <= 5:
                        self.rx_count[motor] += 1
                        
                except BlockingIOError:
                    # No hay datos, esperar un poco
                    time.sleep(0.001)
                except Exception as e:
                    self.get_logger().warn(f"Error RX: {e}")
                    time.sleep(0.1)
            else:
                time.sleep(1.0)

    def print_stats(self):
        """Imprime tabla de contadores."""
        lines = []
        lines.append("\n--- ESTADISTICAS CAN (AX -> BX) ---")
        lines.append(f"{'MOTOR':<10} | {'TX (A)':<10} | {'RX (B)':<10} | {'RATIO %':<10}")
        lines.append("-" * 50)
        
        for i in range(1, 6):
            tx = self.tx_count[i]
            rx = self.rx_count[i]
            ratio = (rx / tx * 100.0) if tx > 0 else 0.0
            lines.append(f"Motor {i:<4} | {tx:<10} | {rx:<10} | {ratio:.1f}%")
            
        print("\n".join(lines))

    def stop(self):
        self.running = False
        if self.thread_tx.is_alive():
            self.thread_tx.join()
        if self.thread_rx.is_alive():
            self.thread_rx.join()

def main(args=None):
    rclpy.init(args=args)
    node = DebugAxBxNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.stop()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
