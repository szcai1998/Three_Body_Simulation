# User flow and interactions

This document describes typical user journeys through the simulation.  A
well‑designed user flow ensures that novices can learn gradually while
experts can explore advanced features.

## Mode selection

1. **First launch:** The simulation starts in one‑body mode with a single
   glowing body moving in a straight line.  A tooltip invites the user to
   drag the body to set an initial velocity.
2. **Switch to two‑body mode:** The user clicks the 2‑body button in the
   mode selector.  Two bodies appear with default masses and velocities
   chosen to produce a circular orbit.  A modal explains Kepler’s laws and
   notes that the orbits are exact when the Kepler solver is enabled【658212011942306†L206-L210】.
3. **Switch to three‑body mode:** Clicking the 3‑body button adds a third
   body.  The system loads a preset (figure‑8) and shows a short
   explanation that the three‑body problem has no general analytic
   solution and is chaotic【409595364031059†L177-L189】.  The user is encouraged
   to toggle chaos mode later to see divergence.

## Editing initial conditions

1. **Drag bodies:** While the simulation is paused, the user can click and
   drag bodies in the 3D view to change their positions.  A small arrow
   appears when dragging away from a body to set its initial velocity.
2. **Use sliders:** In the body editor panel, mass sliders and numeric
   inputs allow precise control of masses, positions and velocities.  For
   2‑body mode, the user can toggle the exact solver to compare numeric
   and analytic behaviour.

## Running the simulation

1. **Play/pause:** The play button starts the physics engine; the bodies
   begin to move and trails grow.  The pause button stops the engine
   without resetting positions.
2. **Adjust speed:** The user moves the speed slider to slow down or speed
   up the motion.  Internally this changes the number of integration
   sub‑steps per frame【547246529604308†L118-L123】.  A tooltip explains that
   accuracy is preserved by keeping Δt constant.
3. **Reset:** The reset button returns bodies to their initial positions
   and clears trails.  A random preset button loads a new system.

## Exploring chaos

1. **Enable chaos mode:** The user clicks the chaos toggle; a second
   simulation runs alongside the first with one body perturbed by 0.1 %.
   The divergence metric appears in the hidden panel and grows over time.
2. **Compare trajectories:** Optionally show ghost trails for the perturbed
   system or draw two sets of trails side by side.  The divergence
   graph helps users see exponential separation.

## Advanced diagnostics

1. **Open hidden panel:** The advanced/signal panel is collapsed by
   default.  Clicking a small icon slides it in.  It shows total energy
   and drift with traffic‑light colours【658212011942306†L269-L284】, angular
   momentum, centre of mass and minimum separation.  Users can watch how
   energy drift correlates with large Δt or high speeds.
2. **Adjust integrator:** In the control panel’s advanced section the user
   can switch integrators.  Selecting RK4 yields smaller short‑term errors
   but, as the N‑body simulator warns, accumulates phase errors over long
   runs【658212011942306†L197-L204】.  Users can see energy drift change in
   real time.
3. **Tune softening and adaptive stepping:** Sliders for the softening
   parameter ε and a checkbox for adaptive time stepping let users manage
   numerical stability.  The minimum distance signal aids in choosing
   appropriate ε and r₀.

This user flow emphasises discovery: novices start simple and build
intuition, while advanced users can dig into chaos, energy conservation and
numerical methods.
