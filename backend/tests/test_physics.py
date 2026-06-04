import pytest
import numpy as np
from app.models import SimulationState, Body, VectorN
from app.physics import compute_accelerations, compute_energy, step_simulation
from app.presets import PRESETS

def test_compute_accelerations():
    # 2 bodies, 1 at origin, 1 at x=1. Mass = 1. G=1. eps=0
    positions = np.array([
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0]
    ])
    masses = np.array([1.0, 1.0])
    accels = compute_accelerations(positions, masses, G=1.0, epsilon=0.0)
    
    # Force on body 0 is towards body 1: +x direction
    # a0 = G * m1 / r^2 = 1 * 1 / 1^2 = 1
    assert np.allclose(accels[0], [1.0, 0.0, 0.0])
    
    # Force on body 1 is towards body 0: -x direction
    assert np.allclose(accels[1], [-1.0, 0.0, 0.0])

def test_verlet_energy_conservation_2_body():
    state = PRESETS["sun_earth_moon"]()
    # Remove moon for 2-body pure test
    state.bodies = [b for b in state.bodies if b.id != "moon"]
    state.timestep = 0.01
    state.integrator = "verlet"
    
    # Initial energy
    positions = np.array([b.position.to_array() for b in state.bodies])
    velocities = np.array([b.velocity.to_array() for b in state.bodies])
    masses = np.array([b.mass for b in state.bodies])
    e0 = compute_energy(positions, velocities, masses, state.G)
    
    # Step simulation
    for _ in range(100):
        step_simulation(state)
        
    positions = np.array([b.position.to_array() for b in state.bodies])
    velocities = np.array([b.velocity.to_array() for b in state.bodies])
    e1 = compute_energy(positions, velocities, masses, state.G)
    
    # Energy should be conserved to within 0.1% or better
    drift = abs(e1 - e0) / abs(e0)
    assert drift < 1e-3

def test_3_body_physics_figure_8():
    state = PRESETS["figure8"]()
    state.timestep = 0.01
    state.integrator = "rk4" # Use RK4 for accuracy test on 3 body
    
    positions = np.array([b.position.to_array() for b in state.bodies])
    velocities = np.array([b.velocity.to_array() for b in state.bodies])
    masses = np.array([b.mass for b in state.bodies])
    e0 = compute_energy(positions, velocities, masses, state.G)
    
    for _ in range(100):
        step_simulation(state)
        
    positions = np.array([b.position.to_array() for b in state.bodies])
    velocities = np.array([b.velocity.to_array() for b in state.bodies])
    e1 = compute_energy(positions, velocities, masses, state.G)
    
    # 3-body energy should be relatively stable
    drift = abs(e1 - e0) / abs(e0)
    assert drift < 1e-2

def test_3d_z_coordinate_is_handled():
    # Ensure z=0 stays 0, but is still size 3
    state = PRESETS["figure8"]()
    step_simulation(state)
    for b in state.bodies:
        assert len(b.position.components) == 3
        assert b.position.components[2] == 0.0

def test_diagnostics_conservation():
    """
    Intensive test to ensure Center of Mass stays stationary and Angular Momentum is strictly conserved.
    We test this over a large number of steps using RK4 for precision on the sun_earth_moon system.
    """
    state = PRESETS["sun_earth_moon"]()
    state.integrator = "rk4"
    state.timestep = 0.01

    # Take one step to initialize the diagnostic signals
    step_simulation(state)
    
    initial_com = state.center_of_mass.to_array()
    initial_angular_momentum = state.angular_momentum.to_array()
    
    for _ in range(500):
        step_simulation(state)
        
    final_com = state.center_of_mass.to_array()
    final_angular_momentum = state.angular_momentum.to_array()
    
    # Center of mass should not drift (Conservation of Linear Momentum)
    # The sun_earth_moon preset is explicitly designed to have 0 total momentum.
    np.testing.assert_allclose(final_com, initial_com, atol=1e-5)
    
    # Angular Momentum should be conserved
    np.testing.assert_allclose(final_angular_momentum, initial_angular_momentum, rtol=1e-3)

def test_performance_20_bodies():
    # Set up 20 random bodies to ensure vectorized implementation handles it seamlessly
    bodies = []
    np.random.seed(42)
    for i in range(20):
        p = np.random.uniform(-10, 10, 3)
        p[2] = 0.0 # Keep z=0
        v = np.random.uniform(-1, 1, 3)
        v[2] = 0.0
        bodies.append(Body(
            id=f"body_{i}",
            mass=float(np.random.uniform(0.1, 10.0)),
            position=VectorN(components=p.tolist()),
            velocity=VectorN(components=v.tolist()),
            acceleration=VectorN()
        ))
    state = SimulationState(bodies=bodies, G=1.0, timestep=0.01)
    
    for _ in range(10):
        step_simulation(state)
        
    assert len(state.bodies) == 20
    # Make sure total energy is calculated and doesn't explode wildly in 10 steps
    assert state.total_energy != 0.0

def test_chaos_mode_divergence():
    state = PRESETS["figure8"]()
    state.chaos_mode = True
    
    for _ in range(50):
        step_simulation(state)
        
    assert state.shadow_bodies is not None
    assert len(state.divergence_history) == 50
    assert state.divergence_history[-1] > 0.0  # Divergence should be positive

def test_kepler_vs_rk4():
    state_kepler = PRESETS["sun_earth_moon"]()
    state_kepler.bodies = [b for b in state_kepler.bodies if b.id != "moon"]
    state_kepler.integrator = "kepler"
    
    import copy
    state_rk4 = copy.deepcopy(state_kepler)
    state_rk4.integrator = "rk4"
    state_rk4.timestep = 0.001  # small timestep for high precision
    
    # Kepler takes 1 large analytical step
    state_kepler.timestep = 1.0
    step_simulation(state_kepler)
    
    # RK4 takes 1000 small numerical steps
    for _ in range(1000):
        step_simulation(state_rk4)
        
    p_k = state_kepler.bodies[1].position.to_array()
    p_r = state_rk4.bodies[1].position.to_array()
    
    # They should produce very similar resulting positions
    np.testing.assert_allclose(p_k, p_r, rtol=1e-2, atol=1e-2)
