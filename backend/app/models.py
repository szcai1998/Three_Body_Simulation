import numpy as np
from pydantic import BaseModel, Field


class VectorN(BaseModel):
    """
    3-dimensional vector [x, y, z] backed by a list.
    Currently used with z=0 for 2D simulations, but structured for future full 3D extension.
    """
    components: list[float] = Field(default_factory=lambda: [0.0, 0.0, 0.0])

    def to_array(self) -> np.ndarray:
        # Ensure it always has length 3 for 3D operations.
        # If components somehow has less or more elements, this enforces standard size or errors.
        return np.array(self.components, dtype=np.float64)

    @classmethod
    def from_array(cls, arr: np.ndarray) -> "VectorN":
        # Convert back to a list of length 3
        # Assuming arr is a 1D numpy array of size 3
        return cls(components=arr.tolist())


class Body(BaseModel):
    """
    Represents a physical body in the simulation.
    """
    id: str
    mass: float
    position: VectorN
    velocity: VectorN
    acceleration: VectorN
    trail: list[VectorN] = Field(default_factory=list)


class SimulationState(BaseModel):
    """
    Represents the full state of the simulation.
    """
    bodies: list[Body]
    G: float = 1.0               # Gravitational constant
    epsilon: float = 1e-3        # Softening length to prevent singularities
    time: float = 0.0            # Current simulation time
    timestep: float = 0.01       # Base time step (Δt)
    integrator: str = "verlet"   # "verlet" | "rk4" | "euler" | "kepler"
    current_preset: str = "figure8"
    running: bool = False
    chaos_mode: bool = False
    shadow_bodies: list[Body] | None = Field(default=None)
    playback_speed: int = 1
    
    # Diagnostic Signals
    initial_energy: float | None = None
    total_energy: float = 0.0
    kinetic_energy: float = 0.0
    potential_energy: float = 0.0
    energy_drift: float = 0.0
    angular_momentum: VectorN = Field(default_factory=lambda: VectorN())
    center_of_mass: VectorN = Field(default_factory=lambda: VectorN())
    min_distance: float = 0.0
    
    divergence_history: list[float] = Field(default_factory=list)
