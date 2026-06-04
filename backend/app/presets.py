from app.models import SimulationState, Body, VectorN
import math
import random

def get_one_body() -> SimulationState:
    """A single body moving in a straight line."""
    return SimulationState(
        G=1.0,
        timestep=0.01,
        bodies=[
            Body(
                id="body1",
                mass=1.0,
                position=VectorN(components=[-5.0, 0.0, 0.0]),
                velocity=VectorN(components=[2.0, 0.0, 0.0]),
                acceleration=VectorN(components=[0.0, 0.0, 0.0])
            )
        ]
    )

def get_two_body() -> SimulationState:
    """A stable binary orbit."""
    return SimulationState(
        G=1.0,
        timestep=0.01,
        bodies=[
            Body(
                id="star1",
                mass=1.0,
                position=VectorN(components=[1.0, 0.0, 0.0]),
                velocity=VectorN(components=[0.0, 0.5, 0.0]),
                acceleration=VectorN(components=[0.0, 0.0, 0.0])
            ),
            Body(
                id="star2",
                mass=1.0,
                position=VectorN(components=[-1.0, 0.0, 0.0]),
                velocity=VectorN(components=[0.0, -0.5, 0.0]),
                acceleration=VectorN(components=[0.0, 0.0, 0.0])
            )
        ]
    )

def get_figure_8() -> SimulationState:
    """The classic zero-angular-momentum figure-8 orbit for 3 equal mass bodies."""
    m = 1.0
    p_x = 0.97000436
    p_y = -0.24308753
    v_x = 0.4662036850
    v_y = 0.4323657300

    return SimulationState(
        G=1.0,
        timestep=0.01,
        bodies=[
            Body(
                id="body1",
                mass=m,
                position=VectorN(components=[p_x, p_y, 0.0]),
                velocity=VectorN(components=[v_x, v_y, 0.0]),
                acceleration=VectorN(components=[0.0, 0.0, 0.0])
            ),
            Body(
                id="body2",
                mass=m,
                position=VectorN(components=[-p_x, -p_y, 0.0]),
                velocity=VectorN(components=[v_x, v_y, 0.0]),
                acceleration=VectorN(components=[0.0, 0.0, 0.0])
            ),
            Body(
                id="body3",
                mass=m,
                position=VectorN(components=[0.0, 0.0, 0.0]),
                velocity=VectorN(components=[-2*v_x, -2*v_y, 0.0]),
                acceleration=VectorN(components=[0.0, 0.0, 0.0])
            )
        ]
    )

def get_sun_earth_moon() -> SimulationState:
    """A hierarchical 3-body system resembling a star, planet, and moon."""
    m_s, m_e, m_m = 10000.0, 10.0, 0.1
    r_e, r_m = 100.0, 4.0
    v_e = (m_s / r_e)**0.5
    v_m = v_e + (m_e / r_m)**0.5
    v_s_y = -(m_e * v_e + m_m * v_m) / m_s

    return SimulationState(
        G=1.0,
        timestep=0.05,
        bodies=[
            Body(
                id="sun",
                mass=m_s,
                position=VectorN(components=[0.0, 0.0, 0.0]),
                velocity=VectorN(components=[0.0, v_s_y, 0.0]),
                acceleration=VectorN(components=[0.0, 0.0, 0.0])
            ),
            Body(
                id="earth",
                mass=m_e,
                position=VectorN(components=[r_e, 0.0, 0.0]),
                velocity=VectorN(components=[0.0, v_e, 0.0]),
                acceleration=VectorN(components=[0.0, 0.0, 0.0])
            ),
            Body(
                id="moon",
                mass=m_m,
                position=VectorN(components=[r_e + r_m, 0.0, 0.0]),
                velocity=VectorN(components=[0.0, v_m, 0.0]),
                acceleration=VectorN(components=[0.0, 0.0, 0.0])
            )
        ]
    )

def get_lagrange() -> SimulationState:
    """3 equal masses at vertices of an equilateral triangle."""
    r = 2.0
    v = math.sqrt(1.0 / (math.sqrt(3) * r)) # v for circular orbit of equilateral triangle
    
    bodies = []
    for i in range(3):
        angle = i * 2 * math.pi / 3
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        vx = -v * math.sin(angle)
        vy = v * math.cos(angle)
        bodies.append(Body(
            id=f"body{i+1}",
            mass=1.0,
            position=VectorN(components=[x, y, 0.0]),
            velocity=VectorN(components=[vx, vy, 0.0]),
            acceleration=VectorN(components=[0.0, 0.0, 0.0])
        ))
    return SimulationState(G=1.0, timestep=0.01, bodies=bodies)

def get_3d_swarm() -> SimulationState:
    """A chaotic 4-body system utilizing the Z axis."""
    return SimulationState(
        G=1.0,
        timestep=0.005,
        bodies=[
            Body(id="b1", mass=2.0, position=VectorN(components=[2.0, 0.0, 0.0]), velocity=VectorN(components=[0.0, 0.5, 0.5]), acceleration=VectorN(components=[0.0, 0.0, 0.0])),
            Body(id="b2", mass=2.0, position=VectorN(components=[-2.0, 0.0, 0.0]), velocity=VectorN(components=[0.0, -0.5, -0.5]), acceleration=VectorN(components=[0.0, 0.0, 0.0])),
            Body(id="b3", mass=2.0, position=VectorN(components=[0.0, 2.0, 0.0]), velocity=VectorN(components=[0.5, 0.0, -0.5]), acceleration=VectorN(components=[0.0, 0.0, 0.0])),
            Body(id="b4", mass=2.0, position=VectorN(components=[0.0, -2.0, 0.0]), velocity=VectorN(components=[-0.5, 0.0, 0.5]), acceleration=VectorN(components=[0.0, 0.0, 0.0]))
        ]
    )

PRESETS = {
    "one_body": get_one_body,
    "binary_orbit": get_two_body,
    "figure8": get_figure_8,
    "sun_earth_moon": get_sun_earth_moon,
    "lagrange": get_lagrange,
    "3d_swarm": get_3d_swarm
}
