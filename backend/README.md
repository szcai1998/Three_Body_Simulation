# Three-Body Simulation Backend

This directory contains the highly optimized Python physics engine and FastAPI server powering the Three-Body Simulation. It serves as the single source of truth for the entire simulation, computing orbital dynamics and streaming state snapshots to the frontend via WebSockets at 60 FPS.

---

## 🧮 Mathematical Foundations

### Newtonian Gravity & N-Body Vectorization
The engine calculates the gravitational forces between $N$ bodies using Newton's law of universal gravitation. To avoid singularities (division by zero when bodies collide), a softening parameter $\epsilon$ is introduced. 

The acceleration $\vec{a}_i$ on body $i$ from all other bodies $j$ is given by:

$$ \vec{a}_i = \sum_{j \neq i} G \frac{m_j}{(|\vec{r}_{ij}|^2 + \epsilon^2)^{3/2}} \vec{r}_{ij} $$

where $\vec{r}_{ij} = \vec{r}_j - \vec{r}_i$ is the vector pointing from body $i$ to body $j$.

To handle large $N$-body systems efficiently, the entire acceleration calculation is **fully vectorized** using NumPy broadcasting. A 3D $N \times N \times 3$ distance matrix is generated in a single C-optimized pass, entirely eliminating slow Python `for` loops.

### Numerical Integrators
The engine provides several integration schemes to step the simulation forward:

#### 1. Velocity Verlet (Default, Symplectic)
Velocity Verlet is the default integrator because it is a **symplectic integrator**. This means it preserves the phase-space volume and nearly perfectly conserves the total energy of the system over extremely long periods.
1. $\vec{v}_{t + 0.5\Delta t} = \vec{v}_t + 0.5 \vec{a}_t \Delta t$
2. $\vec{r}_{t + \Delta t} = \vec{r}_t + \vec{v}_{t + 0.5\Delta t} \Delta t$
3. Compute new acceleration $\vec{a}_{t+\Delta t}$ from $\vec{r}_{t+\Delta t}$
4. $\vec{v}_{t + \Delta t} = \vec{v}_{t + 0.5\Delta t} + 0.5 \vec{a}_{t+\Delta t} \Delta t$

#### 2. Runge-Kutta 4th Order (RK4)
RK4 evaluates the derivatives at 4 points across the timestep and takes a weighted average. It offers incredibly high short-term precision (local error $O(\Delta t^5)$) but is *not symplectic*, meaning it will slowly accumulate phase errors and energy drift over long durations.

#### 3. Exact Kepler Solver (Analytical)
For exactly 2 bodies, the engine offers an analytical Kepler solver. It converts the state into Keplerian orbital elements (semi-major axis $a$, eccentricity $e$, mean anomaly $M$) and solves Kepler's Equation at time $t$:

$$ M = E - e \sin(E) $$

Using the Newton-Raphson method (`scipy.optimize.newton`), the engine finds the Eccentric Anomaly $E$, applies the $f$ and $g$ series transformation, and perfectly predicts the new positions without any numerical drift.

### Adaptive Time-Stepping
To prevent numerical explosion during close chaotic encounters, the engine dynamically monitors the minimum pairwise distance $d_{min}$ between bodies. If $d_{min}$ falls below a threshold, the engine automatically subdivides the physical timestep ($\Delta t$) up to 20x.

---

## 🚀 Practical Usage & API

### Setup and Running
Ensure you have `uv` installed, then run:

```bash
cd backend
uv run uvicorn app.main:app --reload
```
The server will start on `http://127.0.0.1:8000`. You can view the full Swagger OpenAPI documentation at `http://127.0.0.1:8000/docs`.

### WebSocket Streaming
**Endpoint:** `ws://127.0.0.1:8000/ws/simulation`

Connect to this WebSocket to receive continuous, 60 FPS state updates. 
Send JSON commands to control the background simulation task:
- `{"command": "start"}`: Starts the physics loop.
- `{"command": "pause"}`: Pauses the physics loop.
- `{"command": "step"}`: Advances the simulation by exactly one frame and pauses.

### REST Endpoints
- **GET `/api/state`**: Retrieve the current `SimulationState`.
- **GET `/api/presets`**: View available scenarios (e.g., `figure8`, `sun_earth_moon`).
- **POST `/api/init?preset=figure8`**: Initialize a preset system.
- **POST `/api/reset`**: Reset the current state.
- **PUT `/api/config`**: Update global variables.
  - Body: `{"G": 2.0, "integrator": "rk4", "timestep": 0.05}`
- **POST `/api/body`**: Add a new celestial body.
  - *Note: Fails if the `kepler` integrator is active and the system already has 2 bodies.*
- **PUT `/api/body/{id}`**: Update an existing body's properties.
- **DELETE `/api/body/{id}`**: Remove a body from the system.
