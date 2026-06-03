# Framework and technology recommendations

Although the simulation can be built with plain JavaScript and WebGL, using
modern frameworks accelerates development and improves maintainability.  This
file summarises recommended tools for the frontend.

## React + React Three Fiber (R3F)

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

The physics state should not reside in React component state because it is
updated at high frequency.  Options include:

* **Zustand:** A small, hook‑based state manager that is ideal for
  simulations.  The simulation worker can post snapshots to Zustand
  stores, and components can subscribe to updates.
* **Redux Toolkit:** If the application grows larger, Redux provides
  predictable state flows.  However it may be overkill for this project.

## Styling

* **Tailwind CSS:** A utility‑first CSS framework that accelerates
  prototyping.  Define a custom dark theme with accent colours.  Use
  transparency (`bg-opacity-60`) to create translucent panels.
* **CSS variables:** Define variables for colours and sizes so that users
  can switch themes (e.g. light vs dark) if desired.

## Web Worker communication

The physics engine will run in a Web Worker.  Use the `comlink` library to
wrap the worker in a proxy so that you can call its methods directly
without serialising function arguments manually.  Alternatively, use
message channels with typed messages.

## Testing and storybook

* **Storybook:** Use Storybook to develop UI components in isolation.  It
  helps refine the design before connecting to the backend.
* **Jest + React Testing Library:** Write tests for components and worker
  interactions.  Simulate user actions (dragging, clicking) to ensure the
  UI behaves correctly.

## Deployment

The entire application can be hosted statically.  Tools like Vite or
Create‑React‑App can bundle the code.  A CI pipeline (GitHub Actions)
should run tests and deploy to GitHub Pages or a similar static host.

## Optional: Alternative languages

If performance becomes a concern, consider writing the simulation engine in
Rust, compiling it to WebAssembly and exposing it to JavaScript.  Rust’s
type safety and performance are well‑suited to numerical integration.  This
approach would require additional tooling (e.g. `wasm-bindgen`) but could
offer improved speed for larger systems.
