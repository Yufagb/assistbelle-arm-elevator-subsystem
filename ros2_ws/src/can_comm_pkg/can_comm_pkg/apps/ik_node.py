#!/usr/bin/env python3
import time
import threading
import numpy as np

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray, String

from can_comm_pkg.utils.ik import ik_solve_position, fk_forward

class IKNode(Node):
    def __init__(self):
        super().__init__('ik_node')

        # Parámetros
        self.declare_parameter('seed', None)            # semilla [d0,th1,th2,th3,th4]
        self.declare_parameter('d0_units', 'mm')        # unidades del prismático LEÍDO (mm|m)
        self.declare_parameter('state_topic', 'motors_state')
        self.declare_parameter('show_fk_on_startup', True)

        # Movimiento
        self.declare_parameter('apply_solution', True)  # si resolver IK => mover
        self.declare_parameter('move_time_s', 0.0)      # si >0, interpolación lineal
        self.declare_parameter('traj_rate_hz', 50)      # Hz para trayectoria
        self.declare_parameter('default_vel', 0.0)      # vel rotacional para C1..C4 si move_time_s==0

        # Lee parámetros
        seed = self.get_parameter('seed').get_parameter_value().double_array_value
        self.seed = list(seed) if seed else None
        self.d0_units = self.get_parameter('d0_units').get_parameter_value().string_value or 'mm'
        self.state_topic = self.get_parameter('state_topic').get_parameter_value().string_value or 'motors_state'
        self.show_fk = self.get_parameter('show_fk_on_startup').get_parameter_value().bool_value

        self.apply_solution = self.get_parameter('apply_solution').get_parameter_value().bool_value
        self.move_time_s    = float(self.get_parameter('move_time_s').get_parameter_value().double_value)
        self.traj_rate_hz   = int(self.get_parameter('traj_rate_hz').get_parameter_value().integer_value)
        self.default_vel    = float(self.get_parameter('default_vel').get_parameter_value().double_value)

        # IO
        self.sub_target = self.create_subscription(Float32MultiArray, 'ik_target', self.on_target, 10)
        self.pub_sol    = self.create_publisher(Float32MultiArray, 'ik_solution', 10)
        self.sub_state  = self.create_subscription(Float32MultiArray, self.state_topic, self.on_state, 10)
        self.pub_cmd    = self.create_publisher(String, 'can_command', 10)  # 👉 mover con C1..C5

        self.last_q = None       # [d0,th1,th2,th3,th4]
        self._printed_fk = False

        # Timer de cortesía: avisa si no llega estado
        self.timer_warn = self.create_timer(2.0, self._maybe_warn_state)

        self.get_logger().info(
            "IKNode listo. Envíame /ik_target (Float32MultiArray [x,y,z]). "
            "Publico /ik_solution y (si apply_solution=true) mando C1..C5 a /can_command."
        )

    # ---------------- Estado articular ----------------
    def on_state(self, msg: Float32MultiArray):
        data = list(msg.data)
        if len(data) < 10:
            return
        pos = data[:5]  # J1..J5
        th1, th2, th3, th4 = pos[0], pos[1], pos[2], pos[3]
        d0 = pos[4]
        if self.d0_units.lower() == 'mm':
            d0 = d0 / 1000.0  # mm -> m
        self.last_q = [d0, th1, th2, th3, th4]

        if self.show_fk and not self._printed_fk:
            xyz = fk_forward(*self.last_q)
            self.get_logger().info(
                "FK inicial: "
                f"q=[d0={d0:.3f} m, th1={th1:.3f}, th2={th2:.3f}, th3={th3:.3f}, th4={th4:.3f}] "
                f"-> p=[x={xyz[0]:.3f} m, y={xyz[1]:.3f} m, z={xyz[2]:.3f} m]"
            )
            self._printed_fk = True

    def _maybe_warn_state(self):
        if self.show_fk and not self._printed_fk:
            self.get_logger().warn(
                f"Aún no recibo estado en '{self.state_topic}' (no puedo mostrar FK inicial)."
            )
            self.timer_warn.cancel()

    # ---------------- Objetivo IK ----------------
    def on_target(self, msg: Float32MultiArray):
        data = list(msg.data)
        if len(data) < 3:
            self.get_logger().error("ik_target requiere [x,y,z]")
            return

        x, y, z = data[:3]
        q0 = self.seed if self.seed is not None else self.last_q
        q, err = ik_solve_position(np.array([x, y, z]), q0=q0)

        out = Float32MultiArray()
        out.data = [float(v) for v in q]
        self.pub_sol.publish(out)
        self.get_logger().info(
            f"IK -> q={list(out.data)} | err={err:.4e} | seed="
            f"{'custom' if self.seed is not None else ('last_state' if self.last_q is not None else 'geom')}"
        )

        if self.apply_solution:
            if self.move_time_s > 0.0:
                # trayectoria en otro hilo para no bloquear
                threading.Thread(target=self._apply_traj, args=(q,), daemon=True).start()
            else:
                self._apply_instant(q)

    # ---------------- Aplicadores ----------------
    def _apply_instant(self, q):
        """Manda un setpoint por joint: C1..C4 (rad, vel) y C5 (mm)."""
        d0_m, th1, th2, th3, th4 = q
        d0_mm = d0_m * 1000.0
        vel = self.default_vel  # rad/s para C1..C4

        cmds = [
            f"C1:{th1},{vel}",
            f"C2:{th2},{vel}",
            f"C3:{th3},{vel}",
            f"C4:{th4},{vel}",
            f"C5:{d0_mm}",
        ]
        for c in cmds:
            self.pub_cmd.publish(String(data=c))
        self.get_logger().info("Comandos instantáneos enviados (C1..C5).")

    def _apply_traj(self, q_goal):
        """Trayectoria lineal en move_time_s, rate=traj_rate_hz, usando C1..C5."""
        if self.last_q is None:
            # si no tengo q actual, uso instantáneo
            self._apply_instant(q_goal)
            return

        d0_m0, th10, th20, th30, th40 = self.last_q
        d0_m1, th11, th21, th31, th41 = q_goal

        T  = max(0.05, float(self.move_time_s))
        hz = max(5, int(self.traj_rate_hz))
        N  = int(T * hz)
        dt = 1.0 / hz

        for k in range(1, N+1):
            a = k / N
            d0_m = (1-a)*d0_m0 + a*d0_m1
            th1  = (1-a)*th10   + a*th11
            th2  = (1-a)*th20   + a*th21
            th3  = (1-a)*th30   + a*th31
            th4  = (1-a)*th40   + a*th41

            # vel aprox por diferencia (rad/s)
            if k == 1:
                v1=v2=v3=v4=0.0
            else:
                v1 = (th1 - th1_prev)/dt
                v2 = (th2 - th2_prev)/dt
                v3 = (th3 - th3_prev)/dt
                v4 = (th4 - th4_prev)/dt

            self.pub_cmd.publish(String(data=f"C1:{th1},{v1}"))
            self.pub_cmd.publish(String(data=f"C2:{th2},{v2}"))
            self.pub_cmd.publish(String(data=f"C3:{th3},{v3}"))
            self.pub_cmd.publish(String(data=f"C4:{th4},{v4}"))
            self.pub_cmd.publish(String(data=f"C5:{d0_m*1000.0}"))

            th1_prev, th2_prev, th3_prev, th4_prev = th1, th2, th3, th4
            time.sleep(dt)

        self.get_logger().info(f"Trayectoria aplicada en {T:.2f}s ({N} pasos).")

def main():
    rclpy.init()
    node = IKNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
