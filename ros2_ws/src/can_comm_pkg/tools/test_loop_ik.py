#!/usr/bin/env python3
import numpy as np
from can_comm_pkg.apps.cinematica_inversa import ik_solve_arm_pitch_constrained, fk_forward

# Config
TARGET_ELBOW_UP = np.array([0.606, 0.100, 0.409])
TARGET_PRE_GRAB = np.array([0.246, -0.369, 0.409])

def test_ik(target_name, target_pos):
    print(f"\n--- Testing {target_name} ---")
    print(f"Target: {target_pos}")
    
    # Semilla inicial (simulando estado previo)
    # Probamos con una semilla neutra y una con codo arriba (Positivo ahora)
    seeds = [
        ("Neutral", np.array([0.0, 0.0, 0.0, 0.0])),
        ("ElbowUp_Pos", np.array([0.0, 0.5, 1.0, 0.0])) # J2 pos, J3 pos
    ]
    
    for name, seed in seeds:
        print(f"\nSeed ({name}): {seed}")
        
        # Aplicar lógica de forzado (Probamos forzar positivo)
        ik_seed = seed.copy()
        if ik_seed[2] < 0.1:
             print("  -> Forcing J3 positive in seed")
             ik_seed[2] = 0.5
            
        target_d0 = 0.0
        q_sol, err = ik_solve_arm_pitch_constrained(target_pos, target_d0, 0.0, ik_seed)
        
        # q_sol: [d0, th1, th2, th3, th4]
        j1, j2, j3, j4 = q_sol[1], q_sol[2], q_sol[3], q_sol[4]
        
        print(f"Solution: J1={j1:.3f}, J2={j2:.3f}, J3={j3:.3f}, J4={j4:.3f}")
        print(f"Error: {err:.6f}")
        
        # Verificar Pitch
        pitch = j2 + j3 + j4
        print(f"Pitch: {pitch:.3f} rad")
        
        if j3 > 0.1:
            print("RESULT: J3 POSITIVE")
        else:
            print("RESULT: J3 NEGATIVE")

def main():
    test_ik("ELBOW UP", TARGET_ELBOW_UP)
    test_ik("PRE GRAB", TARGET_PRE_GRAB)

if __name__ == "__main__":
    main()
