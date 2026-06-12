
import numpy as np
from can_comm_pkg.apps.cinematica_inversa import ik_solve_arm_only, ik_solve_arm_pitch_constrained, fk_forward

def test_ik():
    print("Testing IK Arm Only...")
    target_pos = [0.4, 0.0, 0.5]
    d0_fixed = 0.0
    
    # Test 1: Arm Only (Unconstrained)
    q_sol, err = ik_solve_arm_only(target_pos, d0_fixed)
    print(f"Arm Only Target: {target_pos}")
    print(f"  Sol: {q_sol}")
    print(f"  Err: {err:.6f}")
    
    # Check Pitch of solution
    # q_sol = [d0, th1, th2, th3, th4]
    pitch = q_sol[2] + q_sol[3] + q_sol[4] # th2+th3+th4
    print(f"  Resulting Pitch: {np.rad2deg(pitch):.2f} deg")
    
    print("\nTesting IK Arm Pitch Constrained (Pitch=0)...")
    # Test 2: Arm Pitch Constrained
    q_sol_c, err_c = ik_solve_arm_pitch_constrained(target_pos, d0_fixed, pitch_goal=0.0)
    print(f"Constrained Target: {target_pos}")
    print(f"  Sol: {q_sol_c}")
    print(f"  Err: {err_c:.6f}")
    
    pitch_c = q_sol_c[2] + q_sol_c[3] + q_sol_c[4]
    print(f"  Resulting Pitch: {np.rad2deg(pitch_c):.2f} deg")
    
    # Test 3: Unreachable?
    print("\nTesting Edge Case (Far away)...")
    target_far = [0.8, 0.0, 0.5]
    q_sol_f, err_f = ik_solve_arm_only(target_far, d0_fixed)
    print(f"Far Target: {target_far}")
    print(f"  Err: {err_f:.6f}")

    print("\nTesting Vertical Trajectory (Constrained)...")
    curr_pos = [0.4, 0.0, 0.5]
    q_curr = q_sol_c
    
    for i in range(10):
        curr_pos[2] += 0.02 # Up 2cm
        q_next, err = ik_solve_arm_pitch_constrained(curr_pos, d0_fixed, pitch_goal=0.0, q0_arm=q_curr[1:5])
        if err > 1e-2:
            print(f"Step {i}: Failed at {curr_pos}, Err: {err:.4f}")
            break
        else:
            print(f"Step {i}: Reached {curr_pos}, Pitch: {np.rad2deg(np.sum(q_next[1:5])):.2f}")
            q_curr = q_next

if __name__ == "__main__":
    test_ik()
