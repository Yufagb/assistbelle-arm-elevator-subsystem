
import numpy as np
from can_comm_pkg.apps.cinematica_inversa import fk_forward, dh_matrix, DH_PARAMS

def get_rotation_matrix(d0, th1, th2, th3, th4):
    vars_list = [d0, th1, 0.0, th2, th3, th4]
    T = np.eye(4)
    
    for i, p in enumerate(DH_PARAMS):
        val = vars_list[i]
        if p["type"] == "P":
            d_val = val + p["d"]
            theta_val = p["offset"]
        else:
            d_val = p["d"]
            if p["invert"]: val = -val
            theta_val = val + p["offset"]
            
        T = T @ dh_matrix(theta_val, d_val, p["a"], p["alpha"])
    return T[:3, :3]

def test_pitch():
    # Test configuration: All zeros
    # th1=0, th2=0, th3=0, th4=0
    # Expected Pitch?
    # J2 (Shoulder) is -90 deg alpha from Base? No, Base is -90 alpha.
    # Let's trace the Z axes.
    
    print("Testing Pitch Calculation...")
    
    configs = [
        [0.0, 0.0, 0.0, 0.0],
        [0.0, np.deg2rad(10), 0.0, 0.0],
        [0.0, 0.0, np.deg2rad(10), 0.0],
        [0.0, 0.0, 0.0, np.deg2rad(10)],
        [0.0, np.deg2rad(10), np.deg2rad(10), np.deg2rad(10)],
    ]
    
    for q in configs:
        th1, th2, th3, th4 = q
        R = get_rotation_matrix(0.0, th1, th2, th3, th4)
        
        # Extract pitch from Rotation Matrix
        # Assuming R is Rot(Z, yaw) * Rot(Y, pitch) * Rot(X, roll)
        # Pitch is usually -asin(R[2,0]) or similar depending on convention
        # But here we care about the angle of the end-effector Z axis relative to global Z?
        # Or the angle of the end-effector X axis relative to global XY plane?
        
        # Vector X del end effector
        x_ee = R[:, 0]
        # Vector Z del end effector
        z_ee = R[:, 2]
        
        # Pitch formula in code: -th2 - th3 - th4
        pitch_code = -th2 - th3 - th4
        
        print(f"Config: th2={np.rad2deg(th2):.1f}, th3={np.rad2deg(th3):.1f}, th4={np.rad2deg(th4):.1f}")
        print(f"  Code Pitch: {np.rad2deg(pitch_code):.1f} deg")
        print(f"  EE X-axis: {x_ee}")
        print(f"  EE Z-axis: {z_ee}")
        
        # Calculate pitch from Z-axis tilt?
        # If pitch is 0, Z-axis should be vertical? Or horizontal?
        # Depends on definition.
        # Usually "Parallel to floor" means the end-effector link (X axis?) is horizontal.
        
        # Let's see what happens when we change th4
        
if __name__ == "__main__":
    test_pitch()
