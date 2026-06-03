## Backend implementation plan

This file outlines the steps needed to build the gravitational simulation
engine.  The backend consists of pure physics logic and optional worker
infrastructure.  The plan assumes a JavaScript/TypeScript implementation in
the browser, but the ideas can be ported to Python or Rust if needed.

### 1. Define constants and types

1. Create the vector and body types described in `data_structures.md`.
2. Choose units.  For educational purposes it can be convenient to set the
   gravitational constant **G** to 1 and measure masses, distances and time in
   arbitrary units.  This avoids extremely small or large values.
3. Set a default softening length **ε** (e.g. 1e‑3).  Expose it via the
   advanced settings panel.

### 2. Implement force and acceleration computation

1. Write a function `computeAccelerations(state: SimulationState)` that
   calculates the acceleration vector for each body.  Use the formula
   described in `math_overview.md` and include the softening parameter
   【658212011942306†L176-L184】.
2. In the two‑body mode, optionally bypass this function and use a Kepler
   solver to compute positions directly【658212011942306†L206-L210】.

### 3. Implement integrators

1. **Velocity Verlet:**  Implement the leapfrog update in the form
   described in `integrator_choices.md`【833745627690946†L414-L450】.  Use
   `computeAccelerations` to obtain new accelerations.
2. **RK4:**  Implement a generic 4th‑order Runge–Kutta integrator that
   accepts a derivative function returning position and velocity
   derivatives.  Use adaptive sub‑stepping when the minimum pairwise
   distance falls below a threshold【547246529604308†L57-L63】.
3. **Euler (optional):**  Implement a simple Euler step for educational
   comparison.
4. **Kepler solver (optional):**  For binary systems, implement an exact
   solver using orbital elements (semi‑major axis *a*, eccentricity *e* and
   argument of pericenter).  Compute the mean anomaly *M* at time *t*, solve
   Kepler’s equation for the eccentric anomaly *E* and then derive the
   position and velocity.  This method ensures zero energy drift and
   perfectly closed orbits【658212011942306†L206-L210】.

### 4. Adaptive time stepping and speed control

1. Compute the minimum pairwise distance after each step.  If it is below
   a chosen distance `r0`, reduce the effective time step by subdividing
   Δt; ensure the sub‑step never falls below 5 % of the base step【547246529604308†L57-L63】.
2. Implement a speed slider in the UI that scales the **number of sub‑steps**
   per frame rather than the length of Δt【547246529604308†L118-L123】.

### 5. Compute diagnostics

1. After each step, compute the total kinetic and potential energy and
   calculate the drift relative to the initial energy【658212011942306†L269-L284】.
2. Compute the total angular momentum vector and the center of mass.
3. If chaos mode is enabled, compute the divergence between the primary and
   perturbed simulations.
4. Package these values into a `Diagnostics` object for the hidden panel.

### 6. Implement chaos divergence mode

1. Allow the user to create a “perturbed copy” of the current initial
   conditions where the position of one body is shifted by a small amount
   (e.g. 1e‑4).  Store both systems separately.
2. Integrate both systems using the same integrator and Δt.  Compute the
   Euclidean distance between corresponding bodies at each step and store
   the norm as the divergence metric.
3. Display the divergence in the hidden panel and optionally show both
   trajectories side by side or overlayed.

### 7. Concurrency (Web Worker)

1. Run the physics engine in a Web Worker to keep the main UI thread
   responsive.  The worker should receive messages with initial
   conditions, parameter updates and control commands (run, pause, step,
   reset).  It should post back body positions, diagnostics and trails
   after each frame.
2. Consider using Transferable objects (typed arrays) for positions and
   velocities to minimize message overhead.

### 8. API design for the frontend

Expose a simple API for the UI to interact with the simulation.  Below is
illustrative TypeScript:

```
// Initialise simulation with N bodies
function init(initialBodies: Body[], params: Partial<SimulationState>): void;

// Control simulation
function start(): void;
function pause(): void;
function reset(): void;
function step(nSteps?: number): void; // optional manual stepping

// Modify parameters
function setIntegrator(name: "verlet" | "rk4" | "kepler"): void;
function setTimeStep(dt: number): void;
function setSoftening(epsilon: number): void;
function setChaosMode(enabled: boolean): void;

// Replace or modify a body
function updateBody(id: string, updates: Partial<Body>): void;
function addBody(body: Body): void;
function removeBody(id: string): void;

// Subscribe to updates (positions, diagnostics, divergence)
function onUpdate(callback: (snapshot: SimulationSnapshot) => void): void;
```

By separating the physics logic from the rendering, this API makes the
backend testable and reusable.  The simulation can also be ported to a
server or other languages if future features (e.g. running very long
trajectories) are required.
