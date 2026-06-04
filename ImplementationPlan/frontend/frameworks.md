# Framework and technology recommendations

This file summarises the chosen tools for both the frontend and the backend.
The simulation uses a client‑server architecture: a Python FastAPI backend
runs the physics engine and streams results to a React frontend over
WebSocket.

## Frontend: React + React Three Fiber (R3F)

React provides a declarative way to build user interfaces.  The R3F library
is a renderer for Three.js that allows you to write 3D scenes as React
components.  Benefits include:

* **Declarative 3D scenes:** Instead of manually managing scene graph
  objects, you describe meshes, lights and cameras as JSX components.  This
  makes it easy to link UI state to 3D objects.
* **Hooks and context:** Use `useFrame` to update positions each frame,
  `useThree` to access the renderer and camera, and React context or
  Zustand for state management.
* **Compatibility:** R3F works with standard Three.js, so you can import
  post‑processing passes (e.g. bloom) and write custom shaders.

## State management

The physics state lives on the backend server.  The frontend maintains a
local mirror in Zustand that is updated from WebSocket snapshots.
Components subscribe to Zustand stores for rendering.

* **Zustand:** A small, hook‑based state manager that is ideal for
  high‑frequency simulation updates.  The WebSocket handler writes
  snapshots to the Zustand store, and R3F components subscribe to updates.
* **Redux Toolkit:** If the application grows larger, Redux provides
  predictable state flows.  However it may be overkill for this project.

## Styling

* **Tailwind CSS:** A utility‑first CSS framework that accelerates
  prototyping.  Define a custom dark theme with accent colours.  Use
  transparency (`bg-opacity-60`) to create translucent panels.
* **CSS variables:** Define variables for colours and sizes so that users
  can switch themes (e.g. light vs dark) if desired.

## Frontend ↔ Backend communication

The frontend communicates with the Python FastAPI backend over two
channels:

* **WebSocket** (`/ws/simulation`): Real‑time bidirectional channel for
  simulation streaming.  The backend pushes state snapshots at ~60 FPS;
  the frontend sends control commands (start, pause, step, set_speed).
* **REST API** (`/api/...`): Request/response endpoints for configuration,
  presets, body CRUD, and parameter updates.

Client‑side interpolation between server snapshots ensures smooth rendering
even if network jitter causes brief delays.

## Testing

* **Storybook:** Use Storybook to develop UI components in isolation.  It
  helps refine the design before connecting to the backend.
* **Vitest + React Testing Library:** Write tests for components and
  WebSocket interactions.  Simulate user actions (dragging, clicking) to
  ensure the UI behaves correctly.

## Deployment

The FastAPI backend serves the built frontend (Vite production bundle) as
static files in production.  During development, Vite's dev server runs on
`:5173` and the FastAPI server runs on `:8000` with CORS enabled.

## Optional: Alternative languages

If performance becomes a concern, consider writing the simulation engine in
Rust, compiling it to WebAssembly and exposing it to JavaScript or calling
it from Python via PyO3.  Rust's type safety and performance are
well‑suited to numerical integration.  This approach would require
additional tooling but could offer improved speed for larger systems.
