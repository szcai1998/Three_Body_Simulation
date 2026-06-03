# UI components

This file enumerates the core UI components needed for the simulation.  Each
component should be encapsulated so that it can be developed and tested
independently.  The examples assume a React/React Three Fiber environment.

## SimulationCanvas

* Renders the 3D scene using Three.js.  Contains cameras, lights and the
  starfield.
* Uses R3F hooks (`useFrame`) to update positions and animate the bodies.
* Handles pointer events for dragging bodies and drawing velocity arrows.  It
  should forward events only when the user is not interacting with the UI
  (e.g. controls have `pointer-events: none`)【547246529604308†L130-L133】.
* Receives position and trail data from the physics engine and draws them as
  `mesh` and `line` objects.  Also draws halos and glows using
  post‑processing passes.

## ModeSelector

* A simple button group that lets users choose between 1‑body, 2‑body and
  3‑body modes.  This sets the number of active bodies and resets the
  simulation.
* Optionally show a short description when switching modes to indicate what
  users should look for (inertia, orbital motion, chaos).

## PresetSelector

* Presents a list of predefined systems (figure‑8, Lagrange triangle,
  butterfly orbit, helix, random)【658212011942306†L221-L227】【547246529604308†L106-L115】.
* Clicking a preset sends the initial conditions to the backend.
* Include a random button that generates bodies with random masses,
  positions and velocities and recenters the centre of mass.

## BodyList and BodyEditor

* Shows a card for each body with controls for mass, radius (visual),
  colour and initial velocity.  Each body can be selected to highlight it
  in the 3D view.
* When a body card is selected, allow manual entry of its position and
  velocity or enable dragging of the velocity arrow in the scene.
* In two‑body mode, allow toggling the use of the exact Kepler solver.

## SimulationControls

* Contains play/pause, reset, speed slider and integrator choice
  dropdown.  The speed slider scales the number of sub‑steps per frame
  instead of the time step【547246529604308†L118-L123】.
* Provide a toggle for adaptive time stepping and another for chaos mode.
* Expose a step button for single‑step debugging.

## HiddenPanel (Signals)

* A collapsible panel that displays diagnostic signals in real time:
  * **Total energy** and **energy drift** with coloured status (green/yellow/red)
    as suggested by the N‑body simulator【658212011942306†L269-L284】.
  * **Angular momentum** magnitude.
  * **Center of mass** coordinates and system drift.
  * **Minimum distance** between bodies (useful for understanding adaptive
    time‑step subdivisions).
  * **Chaos divergence metric** when chaos mode is enabled, perhaps plotted
    as a small graph showing how two trajectories diverge exponentially over
    time.
* Optionally display solver statistics such as cumulative integration steps
  and current Δt.

## NotificationToast

* A small toast component to show transient messages (e.g. “Energy drift
  exceeds 5 %, consider decreasing Δt” or “Perturbation created”).

## LayoutContainer

* Responsible for arranging the above components.  On large screens, place
  the control panel on the right and keep the hidden panel collapsed until
  activated.  On smaller screens, overlay controls on the canvas with
  modals or drawers.

These components provide a modular architecture for building the interface.
Developers can implement them incrementally while hooking them up to the
backend API described in `backend_plan.md`.
