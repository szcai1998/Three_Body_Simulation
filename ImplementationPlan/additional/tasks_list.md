# Development task list

This list summarises the concrete tasks required to realise the simulation.
It is organised roughly in the order they should be tackled, though
front‑ and back‑end work can proceed concurrently once interfaces are
defined.

## Phase 1: Research and prototyping

1. **Study gravitational physics:** Review the formulas for Newtonian gravity,
   energy conservation and Kepler’s laws (see `math_overview.md`).
2. **Experiment with integrators:** Build small prototypes in Python or
   TypeScript to verify the velocity Verlet and RK4 implementations.  Check
   energy drift and compare performance.
3. **Design UI mock‑ups:** Sketch the layout of the simulation canvas,
   control panel and hidden panel.  Use Figma or another design tool to
   iterate on the high‑tech aesthetic.

## Phase 2: Backend implementation

1. **Define types and constants:** Implement vector and body classes and
   the `SimulationState` interface (see `data_structures.md`).
2. **Write `computeAccelerations`:** Sum gravitational forces with softening
   parameter ε【658212011942306†L176-L184】.
3. **Implement integrators:** Write velocity Verlet, RK4 and Euler
   functions (see `integrator_choices.md`).  Implement the optional Kepler
   solver for the two‑body mode【658212011942306†L206-L210】.
4. **Adaptive stepping:** Add logic to compute the minimum pairwise distance
   and subdivide the time step accordingly【547246529604308†L57-L63】.
5. **Diagnostics:** Compute total energy, energy drift, angular momentum and
   other signals.  Implement the chaos divergence metric.
6. **Web Worker:** Wrap the simulation in a worker and design a message
   protocol or use comlink.
7. **API surface:** Expose functions for init, start, pause, reset, step and
   parameter updates (see `backend_plan.md`).

## Phase 3: Frontend implementation

1. **Setup project:** Initialise a React + Vite project with TypeScript.
2. **Install dependencies:** Three.js, React Three Fiber, Zustand, Tailwind,
   @react-three/drei for camera controls, and comlink.
3. **Implement components:** Build `SimulationCanvas`, `ModeSelector`,
   `PresetSelector`, `BodyList`, `SimulationControls`, `HiddenPanel`, and
   supporting components (see `components.md`).
4. **Connect to worker:** Use the API to initialise and update the
   simulation.  Subscribe to updates and update R3F meshes accordingly.
5. **Render design:** Implement the visual style: starfield, glows,
   additive trails, bloom and high‑tech panels【547246529604308†L85-L96】.
6. **User interactions:** Implement dragging, velocity arrow drawing,
   sliders and toggles.  Ensure the speed slider scales sub‑steps rather
   than Δt【547246529604308†L118-L123】.
7. **Hidden panel:** Display diagnostics with appropriate units and
   colour‑coded status bars【658212011942306†L269-L284】.
8. **Chaos mode:** Provide a toggle and visualise divergence.  Optionally
   overlay ghost trails or split the screen for side‑by‑side comparison.

## Phase 4: Testing and polish

1. **Unit tests:** Write tests for physics functions (acceleration,
   integrators, energy computation).  Compare the two‑body mode against the
   Kepler solver.
2. **Component tests:** Use React Testing Library to test user interactions.
3. **Performance:** Profile the simulation and adjust the number of
   integration steps or implement WebAssembly if necessary.
4. **Accessibility:** Ensure the UI works with keyboard navigation and
   screen readers where possible.
5. **Deployment:** Configure a CI pipeline to build, test and deploy the
   static site.

## Phase 5: Extensions (optional)

1. **Multiple bodies:** Allow the user to add more than three bodies; this
   requires more computational power but the integrators generalize.
2. **Collision detection:** Add optional elastic collisions or merging.
3. **Parameter export/import:** Save and load system configurations as JSON.
4. **Audio:** Sonify the orbital frequencies or energy to provide an audio
   dimension to the simulation.
