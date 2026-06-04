import numpy as np
from typing import Tuple
from .models import SimulationState, VectorN


def compute_accelerations(positions: np.ndarray, masses: np.ndarray, G: float, epsilon: float) -> np.ndarray:
    """
    Compute gravitational accelerations for all bodies using NumPy broadcasting.
    positions: (N, 3) array
    masses: (N,) array
    returns: (N, 3) array of accelerations
    """
    N = len(masses)
    if N == 0:
        return np.zeros((0, 3), dtype=np.float64)
        
    # delta[i, j] = positions[j] - positions[i] (Vector from i to j)
    delta = positions[np.newaxis, :, :] - positions[:, np.newaxis, :]
    r_sq = np.sum(delta**2, axis=-1)
    
    # factor[i, j] = G * m_j / (r^2 + eps^2)^(3/2)
    # We add a small identity matrix to avoid self-interaction division by zero
    # though r_sq + eps^2 is usually > 0. If eps=0, diagonal is 0, so avoid warning.
    with np.errstate(divide='ignore', invalid='ignore'):
        factor = G * masses[np.newaxis, :] / (r_sq + epsilon**2)**1.5
    
    # zero out self-interaction
    np.fill_diagonal(factor, 0.0)
    
    # a_i = sum_j factor[i, j] * delta[i, j]
    accelerations = np.sum(factor[:, :, np.newaxis] * delta, axis=1)
    return accelerations


def compute_energy(positions: np.ndarray, velocities: np.ndarray, masses: np.ndarray, G: float) -> float:
    """
    Compute total energy (kinetic + potential) using NumPy broadcasting.
    """
    N = len(masses)
    if N == 0:
        return 0.0
    kinetic = 0.5 * np.sum(masses * np.sum(velocities**2, axis=1))
    
    delta = positions[np.newaxis, :, :] - positions[:, np.newaxis, :]
    r_sq = np.sum(delta**2, axis=-1)
    r = np.sqrt(r_sq)
    
    m_prod = masses[:, np.newaxis] * masses[np.newaxis, :]
    with np.errstate(divide='ignore', invalid='ignore'):
        U_mat = -G * m_prod / r
        
    np.fill_diagonal(U_mat, 0.0)
    # The matrix counts every pair twice, so divide by 2
    potential = np.nansum(U_mat) / 2.0
    
    return float(kinetic + potential)

def compute_angular_momentum(positions: np.ndarray, velocities: np.ndarray, masses: np.ndarray) -> np.ndarray:
    """
    Compute total angular momentum vector of the system.
    L = sum(m_i * (r_i x v_i))
    """
    N = len(masses)
    L = np.zeros(3, dtype=np.float64)
    for i in range(N):
        L += masses[i] * np.cross(positions[i], velocities[i])
    return L

def compute_center_of_mass(positions: np.ndarray, masses: np.ndarray) -> np.ndarray:
    """
    Compute center of mass vector of the system.
    """
    total_mass = np.sum(masses)
    if total_mass == 0:
        return np.zeros(3, dtype=np.float64)
    com = np.sum(positions * masses[:, np.newaxis], axis=0) / total_mass
    return com


def euler_step(positions: np.ndarray, velocities: np.ndarray, accelerations: np.ndarray, dt: float) -> Tuple[np.ndarray, np.ndarray]:
    v_next = velocities + accelerations * dt
    p_next = positions + velocities * dt
    return p_next, v_next


def verlet_step(positions: np.ndarray, velocities: np.ndarray, accelerations: np.ndarray, masses: np.ndarray, G: float, epsilon: float, dt: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    v_half = velocities + 0.5 * accelerations * dt
    p_next = positions + v_half * dt
    a_next = compute_accelerations(p_next, masses, G, epsilon)
    v_next = v_half + 0.5 * a_next * dt
    return p_next, v_next, a_next


def rk4_step(positions: np.ndarray, velocities: np.ndarray, masses: np.ndarray, G: float, epsilon: float, dt: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    # k1
    kv1 = compute_accelerations(positions, masses, G, epsilon)
    kp1 = velocities
    
    # k2
    kv2 = compute_accelerations(positions + kp1 * dt * 0.5, masses, G, epsilon)
    kp2 = velocities + kv1 * dt * 0.5
    
    # k3
    kv3 = compute_accelerations(positions + kp2 * dt * 0.5, masses, G, epsilon)
    kp3 = velocities + kv2 * dt * 0.5
    
    # k4
    kv4 = compute_accelerations(positions + kp3 * dt, masses, G, epsilon)
    kp4 = velocities + kv3 * dt
    
    p_next = positions + (dt / 6.0) * (kp1 + 2 * kp2 + 2 * kp3 + kp4)
    v_next = velocities + (dt / 6.0) * (kv1 + 2 * kv2 + 2 * kv3 + kv4)
    a_next = compute_accelerations(p_next, masses, G, epsilon)
    return p_next, v_next, a_next


import scipy.optimize

def kepler_step(positions: np.ndarray, velocities: np.ndarray, masses: np.ndarray, G: float, dt: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Exact analytical Kepler solver for 2 bodies using orbital elements and solving Kepler's Equation.
    """
    mu = G * (masses[0] + masses[1])
    # Relative state
    r_vec = positions[1] - positions[0]
    v_vec = velocities[1] - velocities[0]
    r = np.linalg.norm(r_vec)
    v_sq = np.sum(v_vec**2)
    
    # Specific energy and semi-major axis
    epsilon = 0.5 * v_sq - mu / r
    
    # If not elliptical, fallback to RK4 for simplicity
    if epsilon >= 0:
        return rk4_step(positions, velocities, masses, G, 1e-3, dt)
        
    a = -mu / (2 * epsilon)
    n = np.sqrt(mu / a**3)
    
    # Eccentricity vector
    h_vec = np.cross(r_vec, v_vec)
    e_vec = np.cross(v_vec, h_vec) / mu - r_vec / r
    ecc = np.linalg.norm(e_vec)
    
    # Eccentric anomaly E_0
    e_dot_r = np.sum(r_vec * v_vec)
    sin_E0 = e_dot_r / (ecc * np.sqrt(mu * a))
    cos_E0 = (1 - r / a) / ecc
    E0 = np.arctan2(sin_E0, cos_E0)
    
    # Mean anomaly M_0
    M0 = E0 - ecc * np.sin(E0)
    
    # New Mean anomaly
    M_t = M0 + n * dt
    
    # Solve Kepler's Equation M_t = E - e * sin(E) for E
    def kepler_eq(E):
        return E - ecc * np.sin(E) - M_t
    def kepler_prime(E):
        return 1 - ecc * np.cos(E)
        
    E_t = scipy.optimize.newton(kepler_eq, M_t, fprime=kepler_prime, tol=1e-10)
    
    # f and g series for universal variables or just standard transform
    # Using f and g functions is cleaner to avoid rotation matrices
    delta_E = E_t - E0
    f = a / r * (np.cos(delta_E) - 1) + 1
    g = dt + (np.sin(delta_E) - delta_E) / n
    
    r_new = f * r_vec + g * v_vec
    r_new_norm = np.linalg.norm(r_new)
    
    f_dot = - (a * n * np.sin(delta_E)) / (r * r_new_norm)
    g_dot = a / r_new_norm * (np.cos(delta_E) - 1) + 1
    
    v_new = f_dot * r_vec + g_dot * v_vec
    
    # Center of mass remains stationary, so we split the new relative vector
    # back into individual positions based on mass ratio.
    m_tot = masses[0] + masses[1]
    com_pos = (masses[0] * positions[0] + masses[1] * positions[1]) / m_tot
    com_vel = (masses[0] * velocities[0] + masses[1] * velocities[1]) / m_tot
    
    new_com_pos = com_pos + com_vel * dt
    
    p_next = np.zeros_like(positions)
    v_next = np.zeros_like(velocities)
    
    # r_new = p1 - p0
    # m0 * p0 + m1 * p1 = m_tot * com
    # p1 = com + (m0/m_tot) * r_new
    # p0 = com - (m1/m_tot) * r_new
    p_next[1] = new_com_pos + (masses[0] / m_tot) * r_new
    p_next[0] = new_com_pos - (masses[1] / m_tot) * r_new
    
    v_next[1] = com_vel + (masses[0] / m_tot) * v_new
    v_next[0] = com_vel - (masses[1] / m_tot) * v_new
    
    # Accelerations
    a_next = compute_accelerations(p_next, masses, G, 1e-3)
    
    return p_next, v_next, a_next


def _step_arrays(positions: np.ndarray, velocities: np.ndarray, accelerations: np.ndarray, masses: np.ndarray, G: float, epsilon: float, dt: float, integrator: str, substeps: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    N = len(masses)
    for _ in range(substeps):
        if integrator == "euler":
            positions, velocities = euler_step(positions, velocities, accelerations, dt)
            accelerations = compute_accelerations(positions, masses, G, epsilon)
        elif integrator == "rk4":
            positions, velocities, accelerations = rk4_step(positions, velocities, masses, G, epsilon, dt)
        elif integrator == "kepler" and N == 2:
            positions, velocities, accelerations = kepler_step(positions, velocities, masses, G, dt)
        else: # "verlet" is default
            positions, velocities, accelerations = verlet_step(positions, velocities, accelerations, masses, G, epsilon, dt)
    return positions, velocities, accelerations

def step_simulation(state: SimulationState) -> SimulationState:
    """
    Advances the simulation state by one timestep (`state.timestep`).
    """
    N = len(state.bodies)
    if N == 0:
        return state
        
    positions = np.array([b.position.to_array() for b in state.bodies])
    velocities = np.array([b.velocity.to_array() for b in state.bodies])
    accelerations = np.array([b.acceleration.to_array() for b in state.bodies])
    masses = np.array([b.mass for b in state.bodies])
    
    # Initialize accelerations if zero (first step)
    if np.all(accelerations == 0.0):
        accelerations = compute_accelerations(positions, masses, state.G, state.epsilon)

    # Adaptive time stepping
    if N > 1:
        delta = positions[np.newaxis, :, :] - positions[:, np.newaxis, :]
        r_sq = np.sum(delta**2, axis=-1)
        # fill diagonal with infinity
        np.fill_diagonal(r_sq, np.inf)
        min_dist = np.sqrt(np.min(r_sq))
    else:
        min_dist = float('inf')
                
    threshold = 0.1
    substeps = 1
    if min_dist < threshold and min_dist > 0:
        substeps = min(20, max(1, int(threshold / min_dist)))
        
    # If kepler is chosen but we have != 2 bodies, fallback to verlet
    # We don't strictly forbid adding a 3rd body, the engine just safely uses verlet
    # Actually user requested to forbid 3rd body if kepler. We will handle that in the REST API.
    # Here we just execute the integrator.
    
    dt = state.timestep / substeps
    
    positions, velocities, accelerations = _step_arrays(
        positions, velocities, accelerations, masses, state.G, state.epsilon, dt, state.integrator, substeps
    )
    
    # Handle chaos mode
    if state.chaos_mode:
        import copy
        if state.shadow_bodies is None:
            # Initialize shadow bodies
            state.shadow_bodies = [b.model_copy(deep=True) for b in state.bodies]
            # Perturb the first body's position slightly
            if len(state.shadow_bodies) > 0:
                p = state.shadow_bodies[0].position.components
                state.shadow_bodies[0].position = VectorN(components=[p[0] + 1e-2, p[1], p[2]])
                
        spositions = np.array([b.position.to_array() for b in state.shadow_bodies])
        svelocities = np.array([b.velocity.to_array() for b in state.shadow_bodies])
        saccelerations = np.array([b.acceleration.to_array() for b in state.shadow_bodies])
        
        spositions, svelocities, saccelerations = _step_arrays(
            spositions, svelocities, saccelerations, masses, state.G, state.epsilon, dt, state.integrator, substeps
        )
        
        # Calculate divergence (sum of Euclidean distances)
        divergence = np.sum(np.linalg.norm(positions - spositions, axis=1))
        state.divergence_history.append(float(divergence))
        if len(state.divergence_history) > 1000:
            state.divergence_history.pop(0)
            
        for i, b in enumerate(state.shadow_bodies):
            b.position = VectorN.from_array(spositions[i])
            b.velocity = VectorN.from_array(svelocities[i])
            b.acceleration = VectorN.from_array(saccelerations[i])
            b.trail.append(b.position)
            if len(b.trail) > 100:
                b.trail.pop(0)
    else:
        state.shadow_bodies = None
        state.divergence_history.clear()

    # Diagnostic signals
    current_energy = compute_energy(positions, velocities, masses, state.G)
    if state.initial_energy is None:
        state.initial_energy = current_energy
        
    state.total_energy = current_energy
    if state.initial_energy != 0.0:
        state.energy_drift = (current_energy - state.initial_energy) / abs(state.initial_energy)
    else:
        state.energy_drift = 0.0
        
    state.angular_momentum = VectorN.from_array(compute_angular_momentum(positions, velocities, masses))
    state.center_of_mass = VectorN.from_array(compute_center_of_mass(positions, masses))
    state.min_distance = float(min_dist) if min_dist != float('inf') else 0.0

    state.time += state.timestep
    for i, b in enumerate(state.bodies):
        b.position = VectorN.from_array(positions[i])
        b.velocity = VectorN.from_array(velocities[i])
        b.acceleration = VectorN.from_array(accelerations[i])
        b.trail.append(b.position)
        if len(b.trail) > 100:  # Ring buffer for trails
            b.trail.pop(0)

    # Collision detection
    if len(state.bodies) > 1:
        new_positions = np.array([b.position.to_array() for b in state.bodies])
        delta = new_positions[np.newaxis, :, :] - new_positions[:, np.newaxis, :]
        r_sq = np.sum(delta**2, axis=-1)
        np.fill_diagonal(r_sq, np.inf)
        
        # Calculate dynamic collision radii based on mass (matching frontend visual radius roughly)
        masses_arr = np.array([b.mass for b in state.bodies])
        radii = np.maximum(0.1, np.minimum(0.5, (masses_arr**(1/3)) * 0.2))
        radii_sum_sq = (radii[:, np.newaxis] + radii[np.newaxis, :])**2
        
        collided_pairs = np.argwhere(r_sq < radii_sum_sq)
        if len(collided_pairs) > 0:
            i, j = collided_pairs[0]
            b1 = state.bodies[i]
            b2 = state.bodies[j]
            new_mass = b1.mass + b2.mass
            new_pos = (b1.mass * new_positions[i] + b2.mass * new_positions[j]) / new_mass
            # Get original velocities to conserve momentum
            v1 = b1.velocity.to_array()
            v2 = b2.velocity.to_array()
            new_vel = (b1.mass * v1 + b2.mass * v2) / new_mass
            
            merged_body = Body(
                id=f"{b1.id}_{b2.id}",
                mass=new_mass,
                position=VectorN.from_array(new_pos),
                velocity=VectorN.from_array(new_vel),
                acceleration=VectorN(components=[0, 0, 0])
            )
            
            for idx in sorted([i, j], reverse=True):
                state.bodies.pop(idx)
            state.bodies.append(merged_body)
            
            # Reset chaos mode on collision to simplify state
            state.chaos_mode = False
            state.shadow_bodies = None
            state.divergence_history.clear()

    return state
