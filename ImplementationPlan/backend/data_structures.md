# Data structures and state management

Efficient data structures simplify both the physics computations and the
communication between the backend server and the frontend.  This file
proposes simple types for representing bodies, vectors and the simulation
state.  All types are defined in Python using Pydantic models for
validation and serialisation.

## Vector type

Define a `VectorN` type backed by a NumPy array.  The vector is generic
over dimensionality: currently 2‑D (x, y) but designed for a future
upgrade to 3‑D (x, y, z).  Include helper methods for addition,
subtraction, scalar multiplication, dot product, norm (magnitude) and
normalisation.  Store positions, velocities and accelerations as `VectorN`
objects.

```python
# Example in Python
import numpy as np
from pydantic import BaseModel

class VectorN(BaseModel):
    """Generic N-dimensional vector backed by a NumPy array.
    Currently 2D (z=0 plane); designed for future 3D upgrade."""
    components: list[float]   # [x, y] now, [x, y, z] later

    def to_array(self) -> np.ndarray:
        return np.array(self.components)

    def add(self, other: "VectorN") -> "VectorN": ...
    def subtract(self, other: "VectorN") -> "VectorN": ...
    def scale(self, s: float) -> "VectorN": ...
    def dot(self, other: "VectorN") -> float: ...
    def norm(self) -> float: ...
    def normalize(self) -> "VectorN": ...
```

Internally the simulation engine should use raw NumPy arrays for
performance.  The Pydantic `VectorN` model is used at API boundaries for
serialisation and validation.

## Body object

Each body should encapsulate its mass, position, velocity and acceleration:

```python
class Body(BaseModel):
    id: str                    # unique identifier (used in UI)
    mass: float                # arbitrary units (G = 1)
    position: VectorN          # current position
    velocity: VectorN          # current velocity
    acceleration: VectorN      # acceleration from last force calculation
    trail: list[VectorN] = []  # recent positions for drawing trails
```

The `id` field lets the UI link sliders and editors to specific bodies.
Trails can be stored as ring buffers to limit memory usage.  Each new
integration step can push the updated position into the trail; older
positions can be removed when the trail reaches a maximum length.

## Simulation state

The state of the simulation includes the collection of bodies and global
parameters:

```python
class SimulationState(BaseModel):
    bodies: list[Body]
    G: float = 1.0             # gravitational constant (can be scaled)
    epsilon: float = 1e-3      # softening length
    time: float = 0.0          # current simulation time
    timestep: float = 0.01     # base time step (Δt)
    integrator: str = "verlet" # "verlet" | "rk4" | "kepler"
    running: bool = False      # whether the simulation is currently stepping
    chaos_mode: bool = False   # whether a perturbed copy is being run
    divergence_history: list[float] = []  # divergence values for chaos metric
```

## Hidden signals / diagnostics

To support the hidden panel, compute and store extra fields:

* `totalEnergy`: sum of kinetic and potential energies (see
  `math_overview.md`).
* `energyDrift`: percentage difference from the initial total energy.  Use
  this as a quality indicator (green/yellow/red) as recommended in the
  N‑body simulator【658212011942306†L269-L284】.
* `angularMomentum`: vector computed from the positions and velocities.
* `centerOfMass`: weighted average position of all bodies.
* `minDistance`: minimum pairwise distance, used for adaptive time stepping.
* `divergence`: current separation between original and perturbed systems
  (when chaos mode is enabled).

These diagnostics can be updated after each integration step and streamed
to the frontend via WebSocket.

## Simulation step function

The core engine should expose a function like `step(state: SimulationState)`
which performs a single integration step using the chosen integrator and
updates all diagnostic fields.  When running in the FastAPI server this
function is called in an asyncio loop to progress the simulation while
streaming state snapshots to the frontend via WebSocket.
