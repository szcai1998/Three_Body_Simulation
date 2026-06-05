<div align="center">
  <h1>🌌 Three Body Simulation</h1>
  <p><strong>Interactive Gravitational Dynamics in High-Tech Sci-Fi 3D</strong></p>
  <video src="scratch/figure8_simulation.webm" autoplay loop muted playsinline width="80%"></video>
  <p><i>Figure-8 Orbital Configuration — A stable 3-body choreography.</i></p>

  <video src="scratch/lagrange_simulation.webm" autoplay loop muted playsinline width="80%"></video>
  <p><i>Lagrange Triangle — Exploring stability in multi-body systems.</i></p>

  <p>
    <a href="#features">Features</a> •
    <a href="#architecture">Architecture</a> •
    <a href="#tech-stack">Tech Stack</a> •
    <a href="#getting-started">Getting Started</a> •
    <a href="#physics--math">Physics & Math</a>
  </p>
</div>

---

An interactive gravitational simulation visualizing the Two-Body and Three-Body problems. Bodies orbit in 2D on a plane rendered within an immersive 3D space, with an architecture designed for a future upgrade to full 3D physics. Built as an educational tool to visualize gravitational dynamics, compare numerical integrators, and explore chaotic orbital mechanics.

## ✨ Features

- **1 / 2 / 3-Body Modes:** Progressive learning flow from simple orbits to chaotic dynamics.
- **Multiple Numerical Integrators:** Velocity Verlet (default), RK4, and Euler.
- **Adaptive Time Stepping:** Maintains precision during close encounters.
- **Chaos Mode:** Perturbed copy with divergence tracking (butterfly effect).
- **Real-Time Diagnostics:** Live monitoring of energy drift, angular momentum, and center of mass.
- **Preset Library:** Instantly load famous configurations like Figure-8, Lagrange triangle, and Butterfly.
- **High-Tech Sci-Fi Aesthetic:** Glowing bodies, additive-blend trails, bloom post-processing, and an immersive starfield.

## 🏗 Architecture

The project is structured as a Monorepo containing a decoupled frontend and backend:

```text
Three_Body_Simulation/
├── backend/             # Python 3.11+ / FastAPI — Physics Engine
│   ├── app/             # Application logic (routers, models, logic)
│   ├── tests/           # pytest suite
│   └── .venv/           # Local virtual environment
├── frontend/            # React + TypeScript + Vite — 3D Renderer
│   ├── src/             # React components, R3F scenes, store
│   └── tests/           # Vitest suite
├── scratch/             # Demo assets and screenshots
├── GEMINI.md            # AI agent configuration guidelines
└── README.md            # You are here
```

- **Backend (Python + FastAPI):** Acts as the authoritative state owner. It runs the physics simulation, streams state snapshots over WebSockets at ~60 FPS, and serves REST endpoints for configuration.
- **Frontend (React + React Three Fiber):** A pure renderer. It interpolates between server snapshots for smooth visuals, provides the sci-fi UI via Tailwind CSS, and manages local state via Zustand.

## 🛠 Tech Stack

| Layer           | Technologies                                                                 |
|-----------------|------------------------------------------------------------------------------|
| **Frontend**    | React, TypeScript, Vite, Three.js (R3F), Zustand, Tailwind CSS, @react-three/drei, @react-three/postprocessing |
| **Backend**     | Python 3.11+, FastAPI, NumPy, SciPy, Pydantic, uvicorn                        |
| **Networking**  | WebSockets (Real-time stream) + REST API (Configs)                           |
| **Testing**     | Vitest (Frontend), pytest (Backend)                                          |
| **Tooling**     | `uv` (Python pkg manager), `npm`, Ruff (Linting)                             |

## 🚀 Getting Started

### Prerequisites

- Node.js (v18+)
- Python (3.11+)
- [uv](https://github.com/astral-sh/uv) (Extremely fast Python package manager)

### 1. Clone the repository

```bash
git clone https://github.com/szcai1998/Three_Body_Simulation.git
cd Three_Body_Simulation
```

### 2. Start the Backend

Open a terminal and start the FastAPI physics engine:

```bash
cd backend
uv venv
source .venv/bin/activate  # Or `.venv\Scripts\activate` on Windows
uv pip install -r requirements.txt
uvicorn app.main:app --reload
```
*The backend will be available at `http://localhost:8000`.*

### 3. Start the Frontend

Open a second terminal and start the Vite dev server:

```bash
cd frontend
npm install
npm run dev
```
*The frontend will be available at `http://localhost:5173`.*

## 🧮 Physics & Math

The backend simulates the $N$-body problem using Newton's law of universal gravitation:

$$ \mathbf{F}_i = \sum_{j \neq i} \frac{G m_i m_j}{|\mathbf{r}_j - \mathbf{r}_i|^3} (\mathbf{r}_j - \mathbf{r}_i) $$

To handle the differential equations numerically, the simulation supports multiple integrators:
1. **Euler Method:** Simple but unstable, highlighting energy drift.
2. **Velocity Verlet:** Symplectic integrator, highly stable for orbital mechanics, conserves energy well.
3. **Runge-Kutta 4 (RK4):** High precision, but computationally heavier.

All physics states are evaluated in Python using `NumPy` vectorization for performance.

## 📜 License

[MIT License](LICENSE)