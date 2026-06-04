# Development task list

This list summarises the concrete tasks required to realise the simulation.
It is organised roughly in the order they should be tackled, though
front‑ and back‑end work can proceed concurrently once interfaces are
defined.  The backend is a Python FastAPI server; the frontend is a React
application built with Vite.

## Phase 1: Research and prototyping

1. **Study gravitational physics:** Review the formulas for Newtonian gravity,
   energy conservation and Kepler's laws (see `math_overview.md`).
2. **Experiment with integrators:** Build small prototypes in Python to verify
   the velocity Verlet and RK4 implementations using NumPy.  Check energy
   drift and compare performance.
3. **Design UI mock‑ups:** Sketch the layout of the simulation canvas,
   control panel and hidden panel.  Use Figma or another design tool to
   iterate on the high‑tech aesthetic.

## Phase 2: Backend implementation (Python + FastAPI)

1. **Set up project:** Initialise a Python project in `/backend` using `uv`.
   Create a local `.venv` inside `/backend`.  Install FastAPI, uvicorn,
   NumPy, SciPy, Pydantic, and pytest.
2. **Define types and constants:** Implement `VectorN` (generic
   dimensionality, currently 2‑D), `Body`, and `SimulationState` using
   Pydantic models (see `data_structures.md`).
3. **Write `compute_accelerations`:** Sum gravitational forces with softening
   parameter ε using NumPy arrays for performance【658212011942306†L176-L184】.
4. **Implement integrators:** Write velocity Verlet, RK4 and Euler
   functions (see `integrator_choices.md`).  Implement the optional Kepler
   solver for the two‑body mode【658212011942306†L206-L210】.
5. **Adaptive stepping:** Add logic to compute the minimum pairwise distance
   and subdivide the time step accordingly【547246529604308†L57-L63】.
6. **Diagnostics:** Compute total energy, energy drift, angular momentum and
   other signals.  Implement the chaos divergence metric.
7. **FastAPI server:** Create the FastAPI application with:
   * **WebSocket endpoint** (`/ws/simulation`): Streams state snapshots at
     ~60 FPS; receives control commands (start, pause, step, set_speed).
   * **REST endpoints** for configuration, presets, body CRUD:
     POST /api/init, POST /api/reset, PUT /api/config,
     PUT /api/body/{id}, POST /api/body, DELETE /api/body/{id},
     GET /api/presets, GET /api/presets/{name}.
   * Use asyncio for the simulation loop.
8. **Backend testing:** Write pytest tests for physics functions
   (acceleration, integrators, energy computation).  Compare the two‑body
   mode against the Kepler solver.  Set up Ruff for linting.

## Phase 3: Frontend implementation (React + Vite + TypeScript)

1. **Setup project:** Initialise a React + Vite project with TypeScript in
   `/frontend`.
2. **Install dependencies:** Three.js, React Three Fiber, @react-three/drei,
   @react-three/postprocessing, Zustand, Tailwind CSS.
3. **WebSocket + REST client:** Create a service layer that connects to the
   backend via WebSocket for simulation streaming and REST for configuration.
   Write received snapshots into a Zustand store.
4. **Implement components:** Build `SimulationCanvas`, `ModeSelector`,
   `PresetSelector`, `BodyList`, `SimulationControls`, `HiddenPanel`, and
   supporting components (see `components.md`).
5. **Render design:** Implement the visual style: starfield, glows,
   additive trails, bloom and high‑tech panels【547246529604308†L85-L96】.
   Client‑side interpolation between server snapshots ensures smooth
   rendering.
6. **User interactions:** Implement dragging, velocity arrow drawing,
   sliders and toggles.  Ensure the speed slider scales sub‑steps rather
   than Δt【547246529604308†L118-L123】.  Send user edits to the backend via REST.
7. **Hidden panel:** Display diagnostics with appropriate units and
   colour‑coded status bars【658212011942306†L269-L284】.
8. **Chaos mode:** Provide a toggle and visualise divergence.  Optionally
   overlay ghost trails or split the screen for side‑by‑side comparison.
9. **Storybook:** Set up Storybook for isolated component development.

## Phase 4: Testing and polish

1. **Backend tests:** Expand pytest suite for physics functions.  Validate
   energy conservation within 0.01 % for two‑body Kepler orbits.
2. **Frontend tests:** Use Vitest + React Testing Library to test user
   interactions and WebSocket state handling.
3. **Integration tests:** Test full frontend ↔ backend flow (WebSocket
   connection, REST calls, state updates).
4. **Performance:** Profile the backend simulation loop and optimise NumPy
   computations.  Consider WebAssembly if needed.
5. **Accessibility:** Ensure the UI works with keyboard navigation and
   screen readers where possible.
6. **Production build:** Configure FastAPI to serve the Vite production
   bundle as static files.

## Phase 5: Extensions (optional)

1. **Multiple bodies:** Allow the user to add more than three bodies; this
   requires more computational power but the integrators generalize.
2. **Collision detection:** Add optional elastic collisions or merging.
3. **Parameter export/import:** Save and load system configurations as JSON.
4. **Audio:** Sonify the orbital frequencies or energy to provide an audio
   dimension to the simulation.
5. **Full 3D physics:** Upgrade VectorN from 2‑D to 3‑D, update all
   integrator and force calculations, and enable full 3D orbits in the
   Three.js renderer.
