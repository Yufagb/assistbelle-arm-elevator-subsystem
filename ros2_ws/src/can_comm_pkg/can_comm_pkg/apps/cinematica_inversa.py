#!/usr/bin/env python3
import numpy as np

# ------------------ Forward Kinematics ------------------

def dh_matrix(theta, d, a, alpha):
    """
    Calcula la matriz de transformación homogénea para un eslabón usando parámetros DH.
    """
    ct, st = np.cos(theta), np.sin(theta)
    ca, sa = np.cos(alpha), np.sin(alpha)
    return np.array([
        [ ct, -st*ca,  st*sa, a*ct],
        [ st,  ct*ca, -ct*sa, a*st],
        [  0,     sa,     ca,    d ],
        [  0,      0,      0,    1 ],
    ], dtype=float)

# Geometría / offsets del robot (Actualizado)
DH_PARAMS = [
    # 0: Ascensor (P)
    {"type": "P", "d": 0.4, "a": 0.0, "alpha": 0.0, "offset": 0.0, "invert": False},
    # 1: Base (R)
    {"type": "R", "d": 0.0, "a": 0.0, "alpha": np.deg2rad(-90), "offset": np.deg2rad(360), "invert": False},
    # 2: Link Fijo (R) - Fijo
    {"type": "R", "d": 0.1, "a": -0.02, "alpha": 0.0, "offset": np.deg2rad(180), "invert": True},
    # 3: Hombro (R)
    {"type": "R", "d": 0.0, "a": 0.215, "alpha": 0.0, "offset": np.deg2rad(180), "invert": True},
    # 4: Codo (R)
    {"type": "R", "d": 0.0, "a": 0.25, "alpha": np.deg2rad(180), "offset": 0.0, "invert": True},
    # 5: Muñeca (R)
    {"type": "R", "d": 0.0, "a": 0.125, "alpha": np.deg2rad(90), "offset": 0.0, "invert": False}
]

def fk_forward(d0, th1, th2, th3, th4):
    """
    Devuelve posición cartesiana (x,y,z) del efector final.
    """
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
        
    return T[:3,3]

# ------------------ Inverse Kinematics ------------------

def jacobian_numeric(q, eps=1e-6):
    """
    Jacobiano numérico 3x5 (solo posición). 
    q = [d0, th1, th2, th3, th4].
    """
    q = np.array(q, dtype=float)
    p0 = fk_forward(*q)
    J = np.zeros((3,5), dtype=float)
    for i in range(5):
        dq = np.zeros_like(q); dq[i] = eps
        p1 = fk_forward(*(q + dq))
        J[:, i] = (p1 - p0) / eps
    return J

def ik_seed_geom(px, py, pz):
    """
    Semilla geométrica simple (sin orientación, sólo posición). 
    Devuelve [d0, th1, th2, th3, th4].
    """
    # Extraer longitudes de la tabla DH_PARAMS
    # Indices: 0=Asc, 1=Base, 2=LinkFijo, 3=Hombro, 4=Codo, 5=Muñeca
    a2 = DH_PARAMS[3]["a"] # Hombro
    a3 = DH_PARAMS[4]["a"] # Codo
    a4 = DH_PARAMS[5]["a"] # Muñeca
    
    # d_fix del ascensor es DH_PARAMS[0]["d"]
    d_fix = DH_PARAMS[0]["d"]

    d0 = pz - d_fix                            # prismática
    th1 = np.arctan2(py, px)                   # base
    r = np.hypot(px, py)
    rw = max(1e-6, r - a4)                     # “muñeca” simplificada

    c3 = (rw**2 - a2**2 - a3**2) / (2*a2*a3)
    c3 = np.clip(c3, -1.0, 1.0)
    s3 = np.sqrt(max(0.0, 1 - c3**2))
    th3 = np.arctan2(s3, c3)

    phi = np.arctan2(a3*np.sin(th3), a2 + a3*np.cos(th3))
    th2 = -phi
    th4 = 0.0

    return np.array([d0, th1, th2, th3, th4], dtype=float)

def ik_solve_position(pd, q0=None, iters=80, lam=1e-3):
    """
    IK por Damped Least Squares (solo posición):
      pd  : np.array([x,y,z])
      q0  : semilla (si None, usa ik_seed_geom)
      iters, lam : iteraciones y amortiguación
    Devuelve (q, err_norm)
    """
    pd = np.asarray(pd, dtype=float).reshape(3)
    if q0 is None:
        q = ik_seed_geom(pd[0], pd[1], pd[2])
    else:
        q = np.array(q0, dtype=float).copy()

    # Límites articulares (según usuario)
    # J1: [-135, 34] deg
    # J2: [-45, 70] deg
    # J3: [-140, 120] deg
    # J4: [-180, 180] deg
    # J5: [0, 350] mm -> [0.0, 0.35] m
    
    LIMITS = [
        (0.0, 0.35),                  # d0 (m)
        (np.deg2rad(-135), np.deg2rad(34)),  # th1
        (np.deg2rad(-45), np.deg2rad(70)),   # th2
        (np.deg2rad(-140), np.deg2rad(120)), # th3
        (np.deg2rad(-180), np.deg2rad(180))  # th4
    ]

    for _ in range(iters):
        pe = fk_forward(*q)
        e  = pd - pe                   # error 3x1
        if np.linalg.norm(e) < 1e-4:
            break
        J = jacobian_numeric(q)        # 3x5
        # DLS: q += J^T (J J^T + lam^2 I)^{-1} e
        A = J @ J.T + (lam**2) * np.eye(3)
        dq = J.T @ np.linalg.solve(A, e)
        
        # Clamp update to prevent huge jumps (Singularity robustness)
        dq = np.clip(dq, -0.1, 0.1)
        
        q += dq
        
        # Enforce limits (Clamping simple)
        for i in range(5):
            q[i] = np.clip(q[i], LIMITS[i][0], LIMITS[i][1])

    return q, float(np.linalg.norm(pd - fk_forward(*q)))

def jacobian_numeric_arm(d0_fixed, q_arm, eps=1e-6):
    """
    Jacobiano numérico 3x4 (solo brazo J1-J4).
    q_arm = [th1, th2, th3, th4]
    d0_fixed = valor fijo del ascensor
    """
    q_arm = np.array(q_arm, dtype=float)
    # Construir q completo: [d0, th1, th2, th3, th4]
    q_full = np.concatenate(([d0_fixed], q_arm))
    
    p0 = fk_forward(*q_full)
    J = np.zeros((3,4), dtype=float)
    
    for i in range(4): # 4 variables del brazo
        dq_arm = np.zeros_like(q_arm)
        dq_arm[i] = eps
        q_new = np.concatenate(([d0_fixed], q_arm + dq_arm))
        p1 = fk_forward(*q_new)
        J[:, i] = (p1 - p0) / eps
    return J

def ik_solve_arm_only(pd, d0_fixed, q0_arm=None, iters=80, lam=1e-3):
    """
    IK para 4 GDL (J1-J4), manteniendo J5 (d0) fijo.
    pd: [x,y,z] target
    d0_fixed: altura actual del ascensor (metros)
    q0_arm: [th1, th2, th3, th4] semilla
    """
    pd = np.asarray(pd, dtype=float).reshape(3)
    
    if q0_arm is None:
        # Usar la semilla geométrica completa y extraer la parte del brazo
        full_seed = ik_seed_geom(pd[0], pd[1], pd[2])
        q_arm = full_seed[1:] # th1..th4
    else:
        q_arm = np.array(q0_arm, dtype=float).copy()

    # Límites para J1-J4 (indices 1..4 de la lista global LIMITS)
    # LIMITS global debe estar definido o redefinido aquí
    # Copiamos los limites de la funcion anterior por seguridad
    ARM_LIMITS = [
        (np.deg2rad(-135), np.deg2rad(34)),  # th1
        (np.deg2rad(-45), np.deg2rad(70)),   # th2
        (np.deg2rad(-140), np.deg2rad(120)), # th3
        (np.deg2rad(-180), np.deg2rad(180))  # th4
    ]

    for _ in range(iters):
        # Construir q completo para FK
        q_full = np.concatenate(([d0_fixed], q_arm))
        pe = fk_forward(*q_full)
        e  = pd - pe
        
        if np.linalg.norm(e) < 1e-4:
            break
            
        J = jacobian_numeric_arm(d0_fixed, q_arm) # 3x4
        
        # DLS 3x4
        A = J @ J.T + (lam**2) * np.eye(3)
        dq = J.T @ np.linalg.solve(A, e)
        
        # Clamp
        dq = np.clip(dq, -0.1, 0.1)
        
        q_arm += dq
        
        # Enforce limits
        for i in range(4):
            q_arm[i] = np.clip(q_arm[i], ARM_LIMITS[i][0], ARM_LIMITS[i][1])
            
    # Retornar q completo [d0, th1, th2, th3, th4] para compatibilidad
    q_final = np.concatenate(([d0_fixed], q_arm))
    return q_final, float(np.linalg.norm(pd - fk_forward(*q_final)))

def jacobian_numeric_arm_locked_j4(d0_fixed, j4_fixed, q_3dof, eps=1e-6):
    """
    Jacobiano numérico 3x3 (solo J1, J2, J3).
    q_3dof = [th1, th2, th3]
    d0_fixed, j4_fixed = valores fijos
    """
    q_3dof = np.array(q_3dof, dtype=float)
    # Construir q completo: [d0, th1, th2, th3, th4]
    q_full = np.concatenate(([d0_fixed], q_3dof, [j4_fixed]))
    
    p0 = fk_forward(*q_full)
    J = np.zeros((3,3), dtype=float)
    
    for i in range(3): # 3 variables
        dq = np.zeros_like(q_3dof)
        dq[i] = eps
        q_new = np.concatenate(([d0_fixed], q_3dof + dq, [j4_fixed]))
        p1 = fk_forward(*q_new)
        J[:, i] = (p1 - p0) / eps
    return J

def ik_solve_arm_locked_j4(pd, d0_fixed, j4_fixed, q0_arm=None, iters=80, lam=1e-3):
    """
    IK para 3 GDL (J1-J3), manteniendo J5 (d0) y J4 fijos.
    pd: [x,y,z] target
    d0_fixed: altura actual del ascensor (metros)
    j4_fixed: angulo J4 fijo (rad)
    q0_arm: [th1, th2, th3, th4] semilla (se usará th1-th3)
    """
    pd = np.asarray(pd, dtype=float).reshape(3)
    
    if q0_arm is None:
        full_seed = ik_seed_geom(pd[0], pd[1], pd[2])
        q_3dof = full_seed[1:4] # th1, th2, th3
    else:
        q_3dof = np.array(q0_arm[0:3], dtype=float).copy() # th1, th2, th3

    # Límites J1-J3
    LIMITS_3DOF = [
        (np.deg2rad(-135), np.deg2rad(34)),  # th1
        (np.deg2rad(-45), np.deg2rad(70)),   # th2
        (np.deg2rad(-140), np.deg2rad(120)), # th3
    ]

    for _ in range(iters):
        # Construir q completo
        q_full = np.concatenate(([d0_fixed], q_3dof, [j4_fixed]))
        pe = fk_forward(*q_full)
        e  = pd - pe
        
        if np.linalg.norm(e) < 1e-4:
            break
            
        J = jacobian_numeric_arm_locked_j4(d0_fixed, j4_fixed, q_3dof) # 3x3
        
        # DLS 3x3 (J es cuadrada si 3DOF para 3D pos, pero DLS es seguro)
        # A = J J^T + lam^2 I
        A = J @ J.T + (lam**2) * np.eye(3)
        dq = J.T @ np.linalg.solve(A, e)
        
        # Clamp
        dq = np.clip(dq, -0.1, 0.1)
        
        q_3dof += dq
        
        # Enforce limits
        for i in range(3):
            q_3dof[i] = np.clip(q_3dof[i], LIMITS_3DOF[i][0], LIMITS_3DOF[i][1])
            
    q_final = np.concatenate(([d0_fixed], q_3dof, [j4_fixed]))
    return q_final, float(np.linalg.norm(pd - fk_forward(*q_final)))

    q_final = np.concatenate(([d0_fixed], q_3dof, [j4_fixed]))
    return q_final, float(np.linalg.norm(pd - fk_forward(*q_final)))

def jacobian_numeric_arm_pitch(d0_fixed, q_arm, eps=1e-6):
    """
    Jacobiano 4x4: 3 filas de posición (x,y,z) + 1 fila de pitch.
    q_arm = [th1, th2, th3, th4]
    """
    q_arm = np.array(q_arm, dtype=float)
    q_full = np.concatenate(([d0_fixed], q_arm))
    p0 = fk_forward(*q_full)
    
    # Pitch actual aproximado: -th2 - th3 - th4 (según DH params invertidos)
    # Verificamos signos: J2(-), J3(-), J4(-)
    # phi = (-th2 + pi) + (-th3 + pi) + (-th4) = -th2 - th3 - th4 + 2pi
    # dphi/dth = -1
    phi0 = -q_arm[1] - q_arm[2] - q_arm[3]
    
    J = np.zeros((4,4), dtype=float)
    
    for i in range(4):
        dq = np.zeros_like(q_arm)
        dq[i] = eps
        q_new = np.concatenate(([d0_fixed], q_arm + dq))
        p1 = fk_forward(*q_new)
        
        # Derivada Posición
        J[:3, i] = (p1 - p0) / eps
        
        # Derivada Pitch
        # Si i=0 (th1), dphi = 0
        # Si i=1,2,3, dphi = -1
        if i == 0:
            J[3, i] = 0
        else:
            J[3, i] = 1.0
            
    return J

def ik_solve_arm_pitch_constrained(pd, d0_fixed, pitch_goal=0.0, q0_arm=None, iters=80, lam=1e-3):
    """
    IK para 4 GDL (J1-J4) con restricción de Pitch global.
    pd: [x,y,z] target
    pitch_goal: ángulo de pitch deseado (rad), 0 = paralelo al suelo
    """
    pd = np.asarray(pd, dtype=float).reshape(3)
    
    if q0_arm is None:
        full_seed = ik_seed_geom(pd[0], pd[1], pd[2])
        q_arm = full_seed[1:5]
    else:
        q_arm = np.array(q0_arm, dtype=float).copy()

    # Límites J1-J4
    ARM_LIMITS = [
        (np.deg2rad(-135), np.deg2rad(34)),  # th1
        (np.deg2rad(-45), np.deg2rad(70)),   # th2
        (np.deg2rad(-140), np.deg2rad(120)), # th3
        (np.deg2rad(-180), np.deg2rad(180))  # th4
    ]

    for _ in range(iters):
        q_full = np.concatenate(([d0_fixed], q_arm))
        pe = fk_forward(*q_full)
        
        # Error Posición
        e_pos = pd - pe
        
        # Error Pitch
        # phi = th2 + th3 + th4
        current_pitch = q_arm[1] + q_arm[2] + q_arm[3]
        # Normalizar a -pi, pi si fuera necesario, pero aquí trabajamos localmente
        e_pitch = pitch_goal - current_pitch
        
        # Vector error 4x1
        e = np.hstack((e_pos, [e_pitch]))
        
        if np.linalg.norm(e) < 1e-4:
            break
            
        J = jacobian_numeric_arm_pitch(d0_fixed, q_arm) # 4x4
        
        # DLS 4x4
        A = J @ J.T + (lam**2) * np.eye(4)
        dq = J.T @ np.linalg.solve(A, e)
        
        # Clamp
        dq = np.clip(dq, -0.1, 0.1)
        
        q_arm += dq
        
        # Enforce limits
        for i in range(4):
            q_arm[i] = np.clip(q_arm[i], ARM_LIMITS[i][0], ARM_LIMITS[i][1])
            
    q_final = np.concatenate(([d0_fixed], q_arm))
    return q_final, float(np.linalg.norm(pd - fk_forward(*q_final)))

def main():
    print("--- Cinematica Inversa (y Directa) ---")
    
    # 1. Definir una posición objetivo
    target_pos = [0.4, 0.2, 0.5]
    print(f"Posición objetivo: {target_pos}")
    
    # 2. Resolver IK
    q_sol, err = ik_solve_position(target_pos)
    print(f"Solución articular encontrada (d0, th1, th2, th3, th4): {q_sol}")
    print(f"Error de posición: {err:.6f}")
    
    # 3. Verificar con FK
    pos_check = fk_forward(*q_sol)
    print(f"Verificación FK de la solución: {pos_check}")

if __name__ == "__main__":
    main()
