#!/usr/bin/env python3
import numpy as np
from can_comm_pkg.apps.cinematica_inversa import ik_solve_arm_pitch_constrained, fk_forward

# Pose 2 (Pre-Grab) from Screenshot
# [-71.5, 44.1, -81.6, 37.5] deg
Q_POSE_2_DEG = np.array([-71.5, 44.1, -81.6, 37.5])
Q_POSE_2 = np.radians(Q_POSE_2_DEG)

def calc_pose_4():
    print(f"Pose 2 (Deg): {Q_POSE_2_DEG}")
    
    # 1. Get Cartesian of Pose 2
    # fk_forward returns [x, y, z]
    # We need d0, th1, th2, th3, th4
    # Assuming d0=0 for calculation (arm only)
    pos_2 = fk_forward(0.0, Q_POSE_2[0], Q_POSE_2[1], Q_POSE_2[2], Q_POSE_2[3])
    print(f"Pose 2 (XYZ): {pos_2}")
    
    # 2. Advance 5cm (0.05m) in direction of gripper
    # Since Pitch is ~0 (44.1 - 81.6 + 37.5 = 0), direction is horizontal along J1
    th1 = Q_POSE_2[0]
    dx = 0.05 * np.cos(th1)
    dy = 0.05 * np.sin(th1)
    dz = 0.0 # Pitch 0, so no Z change
    
    pos_4 = pos_2 + np.array([dx, dy, dz])
    print(f"Pose 4 (XYZ): {pos_4}")
    
    # 3. Solve IK for Pose 4
    # Seed with Pose 2
    q_sol, err = ik_solve_arm_pitch_constrained(pos_4, 0.0, 0.0, Q_POSE_2)
    
    q_sol_deg = np.degrees(q_sol[1:5])
    print(f"Pose 4 (Deg): {q_sol_deg}")
    print(f"Error: {err}")

if __name__ == "__main__":
    calc_pose_4()
