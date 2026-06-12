
import numpy as np
import matplotlib.pyplot as plt

def lspb_traj(q0, qf, dqmax_user, tf, tb, t):
    q_diff = qf - q0
    a_sign = np.sign(q_diff)
    q_abs = abs(q_diff)
    dqmax_abs = abs(dqmax_user)
    
    if tf < 1e-6:
        return np.ones_like(t)*q0, np.zeros_like(t), np.zeros_like(t)

    if tb > tf / 2.0:
        tb = tf / 2.0

    T_flat = tf - tb
    v_req = q_abs / T_flat
    
    v_cruise = v_req
    a_val = v_cruise / tb if tb > 1e-6 else 0.0
    
    disp_accel = 0.5 * v_cruise * tb

    q  = np.zeros_like(t, dtype=float)
    dq = np.zeros_like(t, dtype=float)
    ddq = np.zeros_like(t, dtype=float)
    
    for i, tt in enumerate(t):
        D_t = 0.0
        
        if tt <= tb:
            # Phase 1: Accel
            D_t = 0.5 * a_val * tt**2
            dq[i] = a_sign * a_val * tt
            ddq[i] = a_sign * a_val
            
        elif tt <= tf - tb:
            # Phase 2: Constant Vel
            D_t = disp_accel + v_cruise * (tt - tb)
            dq[i] = a_sign * v_cruise
            ddq[i] = 0.0
            
        else:
            # Phase 3: Decel
            t_rem = tf - tt
            if t_rem < 0: t_rem = 0
            D_t = q_abs - 0.5 * a_val * t_rem**2
            dq[i] = a_sign * a_val * t_rem
            ddq[i] = -a_sign * a_val
            
        q[i] = q0 + a_sign * D_t

    return q, dq, ddq

# Test Parameters
q0 = 0.0
qf = 45.0 * (np.pi/180.0) # 45 deg in rad
tf = 3.0
tb = 0.5
dt = 0.01

t = np.arange(0, tf + dt, dt)
q, dq, ddq = lspb_traj(q0, qf, 10.0, tf, tb, t)

print(f"Start: {q[0]:.4f}, End: {q[-1]:.4f}, Target: {qf:.4f}")
print(f"Vel Start: {dq[0]:.4f}, Vel Mid: {dq[len(dq)//2]:.4f}, Vel End: {dq[-1]:.4f}")

# Check for discontinuity
for i in range(1, len(dq)):
    diff = abs(dq[i] - dq[i-1])
    if diff > 0.5: # Large jump
        print(f"JUMP DETECTED at t={t[i]:.2f}: {dq[i-1]:.3f} -> {dq[i]:.3f}")

# Plot
plt.figure()
plt.subplot(3,1,1)
plt.plot(t, q, label='Pos')
plt.legend()
plt.subplot(3,1,2)
plt.plot(t, dq, label='Vel')
plt.legend()
plt.subplot(3,1,3)
plt.plot(t, ddq, label='Accel')
plt.legend()
plt.savefig('debug_lspb.png')
print("Plot saved to debug_lspb.png")
