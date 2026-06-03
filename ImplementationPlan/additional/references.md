# Research references and citations

This file collects the citations used throughout the implementation plan.
Each entry includes a description of the source and the key points extracted
from it.  Citations appear in the other files using the format
`【source†Lstart-Lend】`.

## Sources

1. **N‑Body Simulator documentation (trisolarchaos.com)** – This online
   simulator provides detailed explanations of how it computes forces,
   supports multiple integration methods and explains why velocity Verlet is
   the default.  Key points extracted:
   * The three‑body problem has no general closed‑form solution; numerical
     simulation is essential【658212011942306†L164-L171】.
   * Newton’s law of gravitation with a softening term prevents singular
     forces when bodies approach each other【658212011942306†L176-L184】.
   * Velocity Verlet is a symplectic integrator that conserves energy
     better than Euler and is ideal for long‑term simulations【658212011942306†L191-L203】.
   * RK4 offers higher local accuracy but accumulates phase errors and
     should be used for short/medium runs【658212011942306†L197-L204】.
   * An exact Kepler solver yields perfect orbits in the two‑body case
     【658212011942306†L206-L210】.
   * Total energy and energy drift should be displayed; drift below 1 %
     indicates excellent accuracy【658212011942306†L269-L284】.

2. **Velocity Verlet article (Wikipedia)** – The article on Verlet
   integration describes the velocity Verlet algorithm and its properties.
   It provides the full update scheme, notes that it is symplectic and
   compares error orders with Euler methods【833745627690946†L414-L472】.

3. **Three‑body problem article (Wikipedia)** – This entry explains the
   three‑body problem in classical mechanics and states that there is no
   general analytic solution.  It lists the equations of motion for the
   three bodies and highlights the system’s chaotic nature【409595364031059†L177-L189】
   【409595364031059†L202-L218】.

4. **Kepler’s laws of planetary motion (Wikipedia)** – These laws
   summarise the exact solution of the two‑body problem: planets move on
   ellipses, sweep equal areas in equal times and obey the period–radius
   relation【991178461770662†L369-L374】.  They justify the inclusion of a
   Kepler solver.

5. **Blog: “I built an interactive 3D three‑body problem simulator in the
   browser” (waldium.com)** – An engineer describes building a 3D
   simulator and shares practical advice.  Highlights include:
   * RK4 integration reduces energy drift but still requires adaptive
     time‑stepping【547246529604308†L51-L63】.
   * Gravitational softening uses (r³ + ε³) in the denominator to avoid
     infinite acceleration【547246529604308†L65-L68】.
   * Rendering tricks: concentric spheres with glows and additive blending
     make bodies look luminous【547246529604308†L85-L94】; a 2 500‑point
     starfield provides depth【547246529604308†L91-L96】; emissive intensity
     scales with velocity【547246529604308†L88-L90】.
   * Speed control should increase the number of integration steps rather
     than enlarge Δt to preserve accuracy【547246529604308†L118-L123】.
   * UI overlays should be translucent and avoid intercepting pointer
     events so that the 3D scene remains interactive【547246529604308†L130-L133】.

These references ground the design choices in established theory and
practical experience.
