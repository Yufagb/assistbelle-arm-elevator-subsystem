#!/usr/bin/env python3
import numpy as np
import time
import matplotlib.pyplot as plt
from can_comm_pkg.apps.cinematica_inversa import ik_solve_position, ik_solve_arm_only
from can_comm_pkg.apps.visualize_dh import RobotVisualizer
from can_comm_pkg.apps.sequence_executor import vel_trapezoidal

# Mock Logger
class Logger:
    def info(self, msg): print(f"[INFO] {msg}")
    def warn(self, msg): print(f"[WARN] {msg}")

class SequenceVisualizer:
    def __init__(self):
        self.viz = RobotVisualizer()
        self.logger = Logger()
        self.current_joints = np.zeros(5) # [d0, th1, th2, th3, th4]
        
        # Initial Position (Home)
        self.viz.update_plot(*self.current_joints)
        plt.pause(0.5)

    def get_logger(self):
        return self.logger

    def send_gripper(self, pct):
        self.logger.info(f"Gripper: {pct}%")
        time.sleep(0.5)

    def _execute_trajectory(self, start_q, end_q, duration):
        # Speed up visualization (2x real time)
        sim_duration = duration / 2.0
        steps = int(sim_duration * 30) # 30 FPS
        dt = sim_duration / steps
        tb = sim_duration * 0.2
        
        for i in range(steps + 1):
            t = i * dt
            q_cmd = np.zeros(5)
            for j in range(5):
                q, _, _ = vel_trapezoidal(start_q[j], end_q[j], sim_duration, tb, t)
                q_cmd[j] = q
            
            # Update Plot
            # q_cmd is [d0, th1, th2, th3, th4]
            self.viz.update_plot(*q_cmd)
            # time.sleep(dt) # plt.pause handles timing
            
        self.current_joints = end_q
        self.viz.update_plot(*end_q)
        time.sleep(0.2)

    def move_arm(self, target_arm_joints, duration=2.0):
        start_joints = self.current_joints.copy()
        target_full = start_joints.copy()
        target_full[1:5] = target_arm_joints
        
        self.logger.info(f"Moviendo BRAZO a: {target_arm_joints}")
        self._execute_trajectory(start_joints, target_full, duration)

    def move_elevator(self, target_d0, duration=2.0):
        start_joints = self.current_joints.copy()
        target_full = start_joints.copy()
        target_full[0] = target_d0
        
        self.logger.info(f"Moviendo ASCENSOR a: {target_d0:.3f}m")
        self._execute_trajectory(start_joints, target_full, duration)

    def move_smart(self, target_joints, total_duration=4.0):
        current_d0 = self.current_joints[0]
        target_d0 = target_joints[0]
        target_arm = target_joints[1:5]
        
        duration_phase = total_duration / 2.0
        
        if target_d0 > current_d0 + 0.005: # Subiendo
            self.logger.info("ESTRATEGIA: SUBIR -> Primero Ascensor, luego Brazo")
            self.move_elevator(target_d0, duration=duration_phase)
            self.move_arm(target_arm, duration=duration_phase)
        else: # Bajando o igual
            self.logger.info("ESTRATEGIA: BAJAR/IGUAL -> Primero Brazo, luego Ascensor")
            self.move_arm(target_arm, duration=duration_phase)
            self.move_elevator(target_d0, duration=duration_phase)

    def run_sequence(self):
        self.logger.info("INICIANDO SIMULACIÓN DE SECUENCIA...")
        
        # 1. HOME
        self.logger.info("PASO 1: HOME")
        home_joints = np.zeros(5)
        self.move_smart(home_joints, total_duration=4.0)
        time.sleep(0.5)
        
        p_pre_agarre = (0.311, -0.455, 0.454)
        p_agarre     = (0.311, -0.452, 0.429)
        p_final      = (-0.286, -0.427, 0.737)
        p_vision     = (-0.250, -0.391, 0.681)
        
        # 2. PRE-AGARRE
        self.logger.info(f"PASO 2: PRE-AGARRE {p_pre_agarre} (J5 Fijo)")
        d0_fixed = 0.0
        q_pre_full, err = ik_solve_arm_only(p_pre_agarre, d0_fixed, q0_arm=None)
        # ik_solve_arm_only retorna [d0, th1, th2, th3, th4]
        # move_arm espera [th1, th2, th3, th4]
        self.move_arm(q_pre_full[1:5], duration=3.0)
        self.send_gripper(100.0)
        
        # 3. AGARRE
        self.logger.info(f"PASO 3: AGARRE {p_agarre} (J5 Fijo)")
        q_agarre_full, err = ik_solve_arm_only(p_agarre, d0_fixed, q0_arm=q_pre_full[1:5])
        self.move_arm(q_agarre_full[1:5], duration=2.0)
        self.send_gripper(0.0)
        
        # 4. FINAL
        self.logger.info(f"PASO 4: FINAL {p_final}")
        q_final, err = ik_solve_position(p_final, q0=None)
        self.move_elevator(q_final[0], duration=2.0)
        self.move_arm(q_final[1:5], duration=3.0)
        self.send_gripper(100.0)
        
        # 5. VISION
        self.logger.info(f"PASO 5: VISION {p_vision}")
        q_vision, err = ik_solve_position(p_vision, q0=q_final)
        self.move_smart(q_vision, total_duration=4.0)
        
        # 6. HOME
        self.logger.info("PASO 6: REGRESO A HOME")
        self.move_smart(home_joints, total_duration=4.0)
        
        self.logger.info("SIMULACIÓN COMPLETADA.")
        plt.show()

def main():
    sim = SequenceVisualizer()
    sim.run_sequence()

if __name__ == "__main__":
    main()
