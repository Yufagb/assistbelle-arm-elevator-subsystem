#!/usr/bin/env python3
import time
import numpy as np
import math
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class CLINode(Node):
    """CLI para publicar comandos en /can_command con entrada en rad o grados (deg)"""

    def __init__(self):
        super().__init__('can_cli')
        self.pub = self.create_publisher(String, 'can_command', 10)
        self.pa = np.zeros(5)     # estado para trayectoria
        self.input_mode = 'rad'   # 'rad' | 'deg' (sexagesimales)
        self.get_logger().info("CLI iniciado. Pulsa Q para salir.")
        self._spin_menu()

    # --- helpers de conversión ------------------------------------------------
    def _p_to_rad(self, x):
        return x if self.input_mode == 'rad' else math.radians(x)

    def _v_to_rad(self, x):
        return x if self.input_mode == 'rad' else math.radians(x)  # deg/s -> rad/s

    # --- publish --------------------------------------------------------------
    def _publish(self, data: str):
        msg = String(data=data)
        self.pub.publish(msg)
        self.get_logger().info(f"Publicado: {data}")

    # --- menú -----------------------------------------------------------------
    def _spin_menu(self):
        while rclpy.ok():
            print("\n=== Menú CAN (ROS2) ===")
            print(f"[U]  Unidades de entrada: {self.input_mode.upper()}  (rad/deg)")
            print("A1-A6 : Solicitar información")
            print("C1-C4 : Set-point pos y vel")
            print("C5    : Set-point lineal (mm, 0-450)")
            print("D1    : Modo de control (0: Trayectoria [q, q']  1: Diferencial [q'])")
            print("D2    : Control del Gripper (%, 0-100)")
            print("T     : Trayectoria [p1,p2,p3,p4,mm] en tiempo(s)")
            print("Q     : Salir")
            choice = input("Opción: ").strip().upper()

            if choice == 'Q':
                break

            if choice == 'U':
                self.input_mode = 'deg' if self.input_mode == 'rad' else 'rad'
                print(f"  → Ahora las entradas se piden en {self.input_mode.upper()} (pero se envían en radianes).")
                continue

            if choice.startswith('A'):
                self._publish(choice)

            elif choice in ('C1', 'C2', 'C3', 'C4'):
                try:
                    p_in  = float(input(f"  Posición ({self.input_mode}): "))
                    v_in  = float(input(f"  Velocidad ({self.input_mode}/s): "))
                    p = self._p_to_rad(p_in)
                    v = self._v_to_rad(v_in)
                except ValueError:
                    print("  ¡Entrada inválida!")
                    continue
                self._publish(f"{choice}:{p},{v}")

            elif choice == 'C5':
                try:
                    mm = float(input("  Distancia (mm, 0-450): "))
                except ValueError:
                    print("  ¡Entrada inválida!")
                    continue
                if not (0.0 <= mm <= 450.0):
                    print("  Fuera de rango (0-450).")
                    continue
                self._publish(f"{choice}:{mm}")

            elif choice == 'D1':
                try:
                    control_mode = int(input("  Modo de control (0: trayectoria, 1: diferencial):"))
                except ValueError:
                    print("  ¡Entrada inválida!")
                    continue
                if not (0 <= control_mode <= 1):
                    print("  Fuera de rango (0-1).")
                    continue
                self._publish(f"{choice}:{control_mode}")

            elif choice == 'D2':
                try:
                    pct = float(input("  Apertura del Gripper (%, 0-100): "))
                except ValueError:
                    print("  ¡Entrada inválida!")
                    continue
                if not (0.0 <= pct <= 100.0):
                    print("  Fuera de rango (0-100).")
                    continue
                self._publish(f"{choice}:{pct}")

            elif choice == 'T':
                try:
                    entrada = input(f"  Objetivo [{self.input_mode},{self.input_mode},{self.input_mode},{self.input_mode},mm]: ")
                    t = float(input("  Tiempo total (s): "))
                    sps = [float(x) for x in entrada.split(',')]
                    if len(sps) != 5:
                        raise ValueError("Se requieren 5 valores.")
                    # convierte 4 primeras a rad si hace falta (C5 mm se deja igual)
                    goal = np.array([self._p_to_rad(sps[i]) if i < 4 else sps[i] for i in range(5)], dtype=float)
                    dt = 0.1
                    n = max(1, int(t / dt))
                    deltas = (goal - self.pa) / n
                    vels = (goal - self.pa) / max(t, dt)

                    for _ in range(n):
                        self.pa += deltas
                        for idx in range(4):  # C1..C4 p, v
                            self._publish(f"C{idx+1}:{float(self.pa[idx])},{float(vels[idx])}")
                        self._publish(f"C5:{float(self.pa[4])}")  # mm
                        time.sleep(dt)

                    # finaliza con vel=0 en rotacionales
                    for idx in range(4):
                        self._publish(f"C{idx+1}:{float(self.pa[idx])},0.0")
                    self._publish(f"C5:{float(self.pa[4])}")

                except ValueError as e:
                    print(f"  ¡Entrada inválida! {e}")

            else:
                print("Opción inválida.")

def main(args=None):
    rclpy.init(args=args)
    node = CLINode()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
