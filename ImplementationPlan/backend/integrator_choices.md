# Numerical integrators

To move the bodies through time, the simulator must integrate the ordinary
differential equations for positions and velocities.  This file summarizes
several integrators, their advantages and disadvantages, and
implementation recommendations.  All integrators are implemented in Python
using NumPy arrays for vector operations.

## Euler integrator (for illustration only)

The simplest method updates positions using the current velocity and
acceleration directly:

```
v(t + Δt) = v(t) + a(t)·Δt
x(t + Δt) = x(t) + v(t)·Δt
```

The Euler method is easy to implement but suffers from severe energy drift.
Orbits gradually spiral inward or outward because the global error is
first‑order; the blog author notes that Euler integration “accumulates energy
error linearly – your orbits will spiral inward or outward over time”【547246529604308†L51-L54】.  This method should only be implemented as a teaching tool to
highlight the need for better integrators.

## Velocity Verlet / leapfrog (symplectic)

The **velocity Verlet** (or leapfrog) method is a **symplectic integrator**.
It updates velocity in two half‑steps around a position update:

1. `v_half = v + 0.5·a(t)·Δt`
2. `x_next = x + v_half·Δt`
3. Compute `a_next` from `x_next` (summing pairwise gravitational forces)
4. `v_next = v_half + 0.5·a_next·Δt`

The velocity Verlet algorithm is widely used because it preserves the
geometric structure of Hamiltonian systems; its error is of order two and
it nearly conserves energy and angular momentum.  The reference page on
Verlet integration states that velocity and position are evaluated at the
same time variable and presents the algorithmic steps above【833745627690946†L414-L450】.  The N‑body simulator uses velocity Verlet by default and explains that
it is a **symplectic** integrator with superior energy conservation
【658212011942306†L191-L203】.  The long‑term error is smaller than that of
semi‑implicit Euler methods【833745627690946†L457-L472】.

Velocity Verlet should be the default integrator for this project because
long‑term orbit stability is more important than minimizing instantaneous
error.  It is straightforward to implement and has low computational cost.

## 4th‑order Runge–Kutta (RK4)

The **RK4** integrator computes weighted averages of four derivative
evaluations per step.  It has a local error of order *h*⁵ and global
error of order *h*⁴.  In practice this means that for a fixed time step
RK4 gives smaller position errors than velocity Verlet.  However, RK4 is not
symplectic; the N‑body simulator notes that RK4 “accumulates systematic
phase errors over long simulation times”【658212011942306†L197-L204】.  The blog
author reports that using RK4 keeps energy drift below 0.01 % for
well‑behaved orbits【547246529604308†L51-L54】 but emphasises that an
adaptive time‑stepping scheme is essential: when two bodies approach
closely the time step must be subdivided to avoid blow‑ups【547246529604308†L57-L63】.

RK4 is recommended as an optional integrator that users can select from
the advanced settings.  It is useful for comparing accuracy but should not
replace velocity Verlet for very long simulations.

### Adaptive time stepping

Chaotic systems can undergo close encounters that require smaller time
steps.  A simple adaptive scheme computes the minimum pairwise distance
between bodies at each frame.  If that distance is below a threshold *r₀*
(e.g. 0.1), subdivide the step proportionally (down to 5 % of the nominal
Δt)【547246529604308†L57-L63】.  This helps prevent numerical instabilities.  The
speed control in the UI should adjust the number of integration steps per
frame rather than increasing the time step itself【547246529604308†L118-L123】.

### Kepler solver (two‑body exact)

For the two‑body mode an exact Kepler solver can compute positions and
velocities directly from orbital elements.  The N‑body simulator uses
Kepler’s laws to obtain perfect energy conservation for binary systems
【658212011942306†L206-L210】.  Implementing such a solver can showcase the
beauty of analytic solutions and provide a benchmark for the numeric
integrators.  The solver should take masses, initial position and velocity
vectors, compute orbital elements (semi‑major axis, eccentricity, etc.), and
then evaluate the position at time *t* via Kepler’s equation.  This solver
is optional but recommended for completeness.

### Chaos divergence metric

To visualise sensitivity to initial conditions, the simulator can run a
second copy of the system with a tiny perturbation and compute the norm of
the difference between corresponding bodies at each step.  Plotting or
displaying this divergence quantifies how chaotic the system is.  The N‑body
plan suggests including such a metric in the hidden panel under
“Simulation signals”.
