import numpy as np

# ------------------ FK / IK helpers ------------------

def dh_matrix(theta, d, a, alpha):
    ct, st = np.cos(theta), np.sin(theta)
    ca, sa = np.cos(alpha), np.sin(alpha)
    return np.array([
        [ ct, -st*ca,  st*sa, a*ct],
        [ st,  ct*ca, -ct*sa, a*st],
        [  0,     sa,     ca,    d ],
        [  0,      0,      0,    1 ],
    ], dtype=float)

# Geometría / offsets del robot (coincide con tu tabla DH)
DH = {
    "d_list":     [0.065, 0.10, 0.0,   0.0,   0.0],               # d1..d5
    "a_list":     [0.025, 0.0,  0.215, 0.250, 0.125],             # a1..a5
    "alpha_list": [np.deg2rad(-90), 0.0, 0.0, np.deg2rad(180), 0.0],
    "d_fix": 0.80
}

def fk_forward(d0, th1, th2, th3, th4, params=DH):
    """Devuelve posición cartesiana (x,y,z) del efector."""
    d0_eff = d0 + params["d_fix"]
    theta_list = [th1 + np.pi, 0.0, th2 + np.pi, th3, -th4]
    d_list, a_list, alpha_list = params["d_list"], params["a_list"], params["alpha_list"]

    T = np.eye(4)
    T = T @ dh_matrix(0.0, d0_eff, 0.0, 0.0)  # ascensor
    for th, d_i, a_i, alpha in zip(theta_list, d_list, a_list, alpha_list):
        T = T @ dh_matrix(th, d_i, a_i, alpha)
    return T[:3,3]

def jacobian_numeric(q, eps=1e-6):
    """Jacobiano numérico 3x5 (solo posición). q = [d0, th1, th2, th3, th4]."""
    q = np.array(q, dtype=float)
    p0 = fk_forward(*q)
    J = np.zeros((3,5), dtype=float)
    for i in range(5):
        dq = np.zeros_like(q); dq[i] = eps
        p1 = fk_forward(*(q + dq))
        J[:, i] = (p1 - p0) / eps
    return J

def ik_seed_geom(px, py, pz, params=DH):
    """
    Semilla geométrica simple (sin orientación, sólo posición). Devuelve [d0, th1, th2, th3, th4].
    """
    a2, a3, a4 = params["a_list"][2], params["a_list"][3], params["a_list"][4]
    d_fix = params["d_fix"]

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

    for _ in range(iters):
        pe = fk_forward(*q)
        e  = pd - pe                   # error 3x1
        if np.linalg.norm(e) < 1e-4:
            break
        J = jacobian_numeric(q)        # 3x5
        # DLS: q += J^T (J J^T + lam^2 I)^{-1} e
        A = J @ J.T + (lam**2) * np.eye(3)
        q += J.T @ np.linalg.solve(A, e)

    return q, float(np.linalg.norm(pd - fk_forward(*q)))
