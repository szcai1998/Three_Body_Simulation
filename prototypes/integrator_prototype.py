import numpy as np
import time

G = 1.0  # Gravitational constant for prototype

def compute_accelerations(positions, masses, softening=0.0):
    # O(N^2) naive approach for small N
    N = len(masses)
    acc = np.zeros_like(positions)
    for i in range(N):
        for j in range(N):
            if i != j:
                r_vec = positions[j] - positions[i]
                r_mag = np.linalg.norm(r_vec)
                # a = (G * m2 / r^3) * r_vec
                acc[i] += G * masses[j] * r_vec / (r_mag**3 + softening**3)
    return acc

def compute_energy(positions, velocities, masses):
    N = len(masses)
    kinetic = 0.5 * np.sum(masses * np.linalg.norm(velocities, axis=1)**2)
    potential = 0.0
    for i in range(N):
        for j in range(i + 1, N):
            r_mag = np.linalg.norm(positions[i] - positions[j])
            potential -= G * masses[i] * masses[j] / r_mag
    return kinetic + potential

def euler_step(pos, vel, mass, dt):
    acc = compute_accelerations(pos, mass)
    new_pos = pos + vel * dt
    new_vel = vel + acc * dt
    return new_pos, new_vel

def velocity_verlet_step(pos, vel, mass, dt, current_acc=None):
    if current_acc is None:
        current_acc = compute_accelerations(pos, mass)
    
    new_pos = pos + vel * dt + 0.5 * current_acc * dt**2
    new_acc = compute_accelerations(new_pos, mass)
    new_vel = vel + 0.5 * (current_acc + new_acc) * dt
    return new_pos, new_vel, new_acc

def rk4_step(pos, vel, mass, dt):
    v1 = vel
    a1 = compute_accelerations(pos, mass)
    
    pos2 = pos + 0.5 * v1 * dt
    v2 = vel + 0.5 * a1 * dt
    a2 = compute_accelerations(pos2, mass)
    
    pos3 = pos + 0.5 * v2 * dt
    v3 = vel + 0.5 * a2 * dt
    a3 = compute_accelerations(pos3, mass)
    
    pos4 = pos + v3 * dt
    v4 = vel + a3 * dt
    a4 = compute_accelerations(pos4, mass)
    
    new_pos = pos + (dt / 6.0) * (v1 + 2*v2 + 2*v3 + v4)
    new_vel = vel + (dt / 6.0) * (a1 + 2*a2 + 2*a3 + a4)
    return new_pos, new_vel

def run_simulation(method, steps, dt):
    # Famous Figure-8 stable orbit for 3 equal masses
    masses = np.array([1.0, 1.0, 1.0])
    positions = np.array([
        [0.97000436, -0.24308753],
        [-0.97000436, 0.24308753],
        [0.0, 0.0]
    ])
    
    v3 = np.array([-0.93240737, -0.86473146])
    velocities = np.array([
        -0.5 * v3,
        -0.5 * v3,
        v3
    ])
    
    initial_energy = compute_energy(positions, velocities, masses)
    
    start_time = time.time()
    
    if method == 'verlet':
        acc = compute_accelerations(positions, masses)
    
    for _ in range(steps):
        if method == 'euler':
            positions, velocities = euler_step(positions, velocities, masses, dt)
        elif method == 'verlet':
            positions, velocities, acc = velocity_verlet_step(positions, velocities, masses, dt, acc)
        elif method == 'rk4':
            positions, velocities = rk4_step(positions, velocities, masses, dt)
            
    end_time = time.time()
    final_energy = compute_energy(positions, velocities, masses)
    
    energy_drift = abs((final_energy - initial_energy) / initial_energy) * 100
    
    print(f"{method.upper():<8} | {(end_time - start_time)*1000:6.1f} ms | Drift: {energy_drift:10.6f}%")

if __name__ == '__main__':
    steps = 50000
    dt = 0.001
    print(f"Running 3-body Figure-8 simulation for {steps} steps (dt={dt})\\n")
    print("Method   | Time (ms)  | Energy Drift (%)")
    print("-" * 45)
    run_simulation('euler', steps, dt)
    run_simulation('verlet', steps, dt)
    run_simulation('rk4', steps, dt)
    print("-" * 45)
