# Three Body Simulation Roadmap

This roadmap organizes our development into discrete chat sessions based on our implementation plan. This ensures we keep our chat contexts focused and avoid mixing unrelated tasks.

- `[/]` **Chat 1: Research and Prototyping (Phase 1 & Initialization)**
  - `[x]` Study gravitational physics and finalize mathematical approach
  - `[x]` Design project architecture and write implementation plans
  - `[x]` Initialize project repository (GEMINI.md, .gitignore)
  - `[x]` (Optional) Build small Python integrator prototypes or UI mockups
- `[x]` **Chat 2: Backend Implementation (Phase 2)**
  - `[x]` Initialize Python project (`/backend`) using `uv`
  - `[x]` Define Pydantic models for data structures
  - `[x]` Implement core physics math (accelerations, integrators)
  - `[x]` Setup FastAPI server (REST + WebSocket endpoints)
  - `[x]` Write pytest suite for physics validation
- `[x]` **Chat 3: Frontend Implementation (Phase 3)**
  - `[x]` Initialize React + Vite project (`/frontend`) with TypeScript
  - `[x]` Setup Three.js, React Three Fiber, Zustand, and Tailwind
  - `[x]` Build WebSocket + REST client service for state syncing
  - `[x]` Implement `SimulationCanvas` and visual aesthetics (glows, trails)
  - `[x]` Build React UI components (`SimulationControls`, `HiddenPanel`, etc.)
- `[x]` **Chat 4: Testing and Polish (Phase 4)**
  - `[x]` Implement new metrics: Kinetic/Potential Energy split and Chaos Divergence
  - `[x]` Update `HiddenPanel` to display the new metrics
  - `[x]` Expand backend tests (all presets, rigorous energy conservation)
  - `[x]` Write frontend tests (Vitest setup and component testing)
  - `[x]` Integration test full frontend ↔ backend flow
  - `[x]` Performance profiling and optimization of NumPy hot loops
  - `[x]` Ensure UI accessibility (ARIA tags)
  - `[x]` Configure FastAPI to serve Vite production build
- `[x]` **Chat 5: Extensions & UI Improvements (Phase 5)**
  - `[x]` **Telemetry**: Add Angular Momentum graph and Phase Space (X vs Vx) scatter plot to `HiddenPanel.tsx`
  - `[x]` **Inspector Sidebar**: Create `BodyInspector.tsx` for viewing and editing selected body mass, position, and velocity
  - `[x]` **Edit Mode**: Add "Design Mode" toggle that changes camera to top-down 2D grid
  - `[x]` **3D Interaction**: Add click-to-select and `TransformControls` for dragging bodies in Design Mode
  - `[x]` **Backend Sync**: Ensure UI edits map correctly to the `PUT /api/body/{body_id}` endpoint
