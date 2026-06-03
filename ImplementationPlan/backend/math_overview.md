# Mathematical foundations

Understanding the gravitational few‑body problem is essential before writing
code.  This section summarizes the physics for one, two and three bodies and
explains why different numerical approaches are necessary.

## Newtonian gravity

The simulation uses **Newton's law of universal gravitation**.  The force
between two point masses *m₁* and *m₂* separated by a vector **r** is

```
F = G · m₁ · m₂ / (|r|² + ε²)
```

where **G** is the gravitational constant and **ε** is a small softening
parameter that prevents singularities when bodies approach very closely.  The
N‑body simulator used for reference explains that each body experiences the
sum of all pairwise forces and that softening avoids numerical blow‑ups【658212011942306†L176-L184】.  Without softening the acceleration would diverge at
near‑zero separation; the blog article on building a 3‑body simulator notes
that adding softening (using *r³+ε³* in the denominator) prevents the system
from “flying apart in one frame”【547246529604308†L65-L68】.

The acceleration of body *i* due to all other bodies is

```
a_i = Σ_{j ≠ i} G·m_j · (r_j − r_i) / (|r_j − r_i|² + ε²)^{3/2}
```

where the exponent 3/2 arises because force is proportional to 1/|r|² and
acceleration is force divided by mass.

## One‑ and two‑body problems

For **one body** under no external forces the motion is trivial: a body with
initial velocity moves in a straight line at constant speed.  The simulation
should support this mode to introduce users to the concept of inertia.

For **two bodies** the problem is exactly solvable.  The N‑body
reference notes that, unlike the three‑body case, the two‑body problem has
an exact analytic solution【658212011942306†L169-L170】.  Kepler’s laws of
planetary motion summarize these solutions: a planet moves on an ellipse
with the central body at one focus, equal areas are swept out in equal
times, and the square of the orbital period is proportional to the cube of
the semi‑major axis【991178461770662†L369-L374】.  Implementing an exact
Kepler solver for the two‑body mode ensures that orbits are closed and
energy is perfectly conserved【658212011942306†L206-L210】.  However, a
general numeric integrator can also be used to keep the code uniform across
1‑, 2‑ and 3‑body modes.

## The three‑body problem

The **three‑body problem** asks for the motion of three point masses under
mutual gravity.  It differs fundamentally from the two‑body problem because
there is **no general closed‑form analytic solution**【409595364031059†L177-L189】.
The equations of motion consist of three coupled second‑order differential
equations (or 18 first‑order equations) for the positions and momenta
【409595364031059†L202-L218】.  For most initial conditions the system is
chaotic: tiny perturbations in initial positions lead to exponentially
divergent trajectories【409595364031059†L177-L189】.  Because of this
chaos, the only way to predict the motion is through numerical integration.

## Energy and diagnostics

The total mechanical energy of an N‑body system is

```
E = Σ_i ½·m_i·|v_i|²  +  Σ_{i<j} -G·m_i·m_j / |r_i − r_j|
```

An ideal gravitational system conserves total energy.  Numerical integrators
introduce small errors; monitoring energy drift is therefore a good measure
of simulation quality.  The N‑body simulator’s documentation recommends
displaying the total energy and the percentage change from the initial state
【658212011942306†L269-L284】.  Energy drift below 1 % is considered excellent
【658212011942306†L269-L284】.

Other useful diagnostics include angular momentum, center‑of‑mass position,
pairwise distances and a **chaos divergence metric** that measures how
rapidly two nearly identical simulations diverge.
