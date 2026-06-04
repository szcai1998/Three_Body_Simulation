# Frontend design overview

The user interface is the most visible part of the simulation.  It should
communicate the physics intuitively while remaining elegant and easy to
operate.  This section proposes a high‑tech aesthetic inspired by existing
3‑body simulators and outlines the major areas of the UI.

## Visual style

* **Dark high‑tech theme:** Use a dark background with subtle gradients or
  starfield textures to evoke deep space.  The blog author’s simulator
  uses a procedural starfield to provide depth【547246529604308†L91-L96】; a similar
  approach will make the scene feel immersive without distracting from the
  bodies.
* **Glowing bodies:** Each body is rendered as concentric spheres (solid
  core, inner glow and outer halo) with emissive materials and a point
  light.  This layering technique makes the bodies look luminous and
  provides intuitive visual cues【547246529604308†L85-L88】.  Emissive
  intensity should scale with velocity so that fast‑moving bodies glow
  brighter【547246529604308†L88-L90】.
* **Additive blending:** Render trails and halos with additive blending and
  disable depth writing so that overlapping trails appear luminous
  instead of muddy【547246529604308†L91-L94】.
* **Bloom/glare:** Apply a post‑processing bloom (e.g. Three.js’s
  `UnrealBloomPass`) to give everything a soft radiative glow【547246529604308†L91-L94】.

## Layout

The UI is divided into three main regions:

1. **3D simulation canvas**: An interactive Three.js canvas shows the bodies,
   trails and starfield.  Users can rotate the camera with the mouse, pan
   and zoom with scroll.  The canvas should capture all pointer events
   unless a UI control is clicked【547246529604308†L130-L133】.
2. **Control panel:** A translucent overlay or side panel contains sliders
   and buttons.  To maintain a clean look, make the panel semi‑transparent
   and use minimal design with iconography.  Controls include:
   * Mode selector (1‑body, 2‑body, 3‑body) and preset buttons (e.g.
     figure‑eight orbit, Lagrange triangle).
   * Mass sliders for each body and velocity vector editors (drawn as
     arrows in the 3D scene).
   * Integration settings (time step, integrator choice, softening length,
     adaptive stepping toggle) and a speed slider that controls the number
     of sub‑steps【547246529604308†L118-L123】.
   * Play/pause/reset buttons and a “Chaos mode” toggle to start a
     perturbed simulation.
3. **Hidden panel / signals:** An advanced panel can be hidden by default
   and opened by clicking a small icon.  It displays diagnostic signals:
   total energy and energy drift (with green/yellow/red indicators as in
   the N‑body simulator【658212011942306†L269-L284】), angular momentum,
   center of mass, minimum separation, chaos divergence and solver error.

## Interaction design

* **Drag‑and‑drop:** When paused, users can drag bodies within the 3D
  scene to set initial positions.  They can also click a body and drag
  outwards to set an initial velocity vector (represented by an arrow).
* **Smooth camera controls:** Provide orbit controls with inertial
  smoothing.  Use scroll to zoom and right‑click drag to pan; arrow keys
  can also rotate the view【658212011942306†L127-L134】.
* **Mode progression:** Start with the one‑body mode to demonstrate
  straight‑line motion.  Then allow two bodies (orbit) and finally
  three bodies (chaos).  Each mode teaches new concepts and keeps the
  learning curve gentle.
* **Preset library:** Include presets for famous periodic orbits (figure‑8,
  Lagrange triangle, butterfly, etc.)【658212011942306†L221-L227】.  Clicking a
  preset loads appropriate masses, positions and velocities.  Random
  presets can also be generated.
* **Adaptive detail:** Use fade‑in/out to display velocity arrows and
  trails only when relevant.  Provide tooltips for controls.

## Technology stack

* **Three.js with React Three Fiber (R3F):** The blog author used plain
  Three.js with ES modules.  A declarative layer like R3F simplifies
  component composition and state management in React.
* **React:** Use React for UI controls and state management.  Zustand
  manages the local simulation state mirror, updated via WebSocket
  snapshots from the backend server.
* **Tailwind CSS or custom CSS:** For the high‑tech look, consider using
  Tailwind with a custom dark palette.  CSS variables allow dynamic
  theming.
* **GLSL shaders:** Write custom shaders for trails and halos to control
  alpha fading and color.

The frontend performs client‑side interpolation between server snapshots
to ensure smooth rendering even under network jitter.

This overview sets the tone for an elegant yet functional interface.  The
following files describe the components and user flows in more detail.
