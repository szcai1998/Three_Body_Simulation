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
- `[ ]` **Chat 4: Testing and Polish (Phase 4)**
  - `[ ]` Expand backend tests (energy conservation limits)
  - `[ ]` Write frontend tests (Vitest)
  - `[ ]` Integration test full frontend ↔ backend flow
  - `[ ]` Performance profiling and optimization
  - `[ ]` Configure FastAPI to serve Vite production build
- `[ ]` **Chat 5: Extensions (Phase 5)**
  - `[ ]` N-body support (allow >3 bodies)
  - `[ ]` Collision detection
  - `[ ]` Full 3D physics and rendering upgrade
