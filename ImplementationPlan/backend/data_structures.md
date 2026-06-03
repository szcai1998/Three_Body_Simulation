# Data structures and state management

Efficient data structures simplify both the physics computations and the
communication with the frontend.  This file proposes simple types for
representing bodies, vectors and the simulation state.

## Vector type

Define a `Vector3` type with `x`, `y` and `z` components.  Include helper
methods for addition, subtraction, scalar multiplication, dot product,
norm (magnitude) and normalisation.  Store positions, velocities and
accelerations as `Vector3` objects.

```ts
// Example in TypeScript
interface Vector3 {
  x: number;
  y: number;
  z: number;
  add(other: Vector3): Vector3;
  subtract(other: Vector3): Vector3;
  scale(s: number): Vector3;
  dot(other: Vector3): number;
  norm(): number;
}
```

## Body object

Each body should encapsulate its mass, position, velocity and acceleration:

```ts
interface Body {
  id: string;          // unique identifier (used in UI)
  mass: number;        // kilograms or arbitrary units
  position: Vector3;   // current position
  velocity: Vector3;   // current velocity
  acceleration: Vector3; // acceleration from last force calculation
  trail: Vector3[];    // optional array storing recent positions for drawing trails
}
```

The `id` field lets the UI link sliders and editors to specific bodies.
Trails can be stored as ring buffers to limit memory usage.  Each new
integration step can push the updated position into the trail; older
positions can be removed when the trail reaches a maximum length.

## Simulation state

The state of the simulation includes the collection of bodies and global
parameters:

```ts
interface SimulationState {
  bodies: Body[];
  G: number;           // gravitational constant (can be scaled)
  epsilon: number;     // softening length
  time: number;        // current simulation time in seconds
  timestep: number;    // base time step (Δt)
  integrator: "verlet" | "rk4" | "kepler";
  running: boolean;    // whether the simulation is currently stepping
  chaosMode: boolean;  // whether a perturbed copy is being run
  divergenceHistory: number[]; // divergence values for chaos metric
}
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

These diagnostics can be updated after each integration step and passed to
the UI.

## Simulation step function

The core engine should expose a function like `step(state: SimulationState)`
which performs a single integration step using the chosen integrator and
updates all diagnostic fields.  When running in a Web Worker this function
can be looped to progress the simulation while keeping the UI thread free.
