# Three Body Simulation

An interactive gravitational simulation visualizing the Two-Body and
Three-Body problems. Bodies orbit in 2D on a plane rendered within an
immersive 3D space, with the architecture designed for a future upgrade to
full 3D physics.

## Features (Planned)

- **1 / 2 / 3-body modes** with progressive learning flow
- **Multiple numerical integrators**: Velocity Verlet (default), RK4, Euler,
  and an exact Kepler solver for two-body orbits
- **Adaptive time stepping** for close encounters
- **Chaos mode**: perturbed copy with divergence tracking
- **Real-time diagnostics**: energy drift, angular momentum, center of mass
- **Preset library**: figure-8, Lagrange triangle, butterfly, and more
- **High-tech sci-fi aesthetic**: glowing bodies, additive-blend trails,
  bloom post-processing, starfield background

## Architecture

```
Three_Body_Simulation/
├── backend/          # Python 3.11+ / FastAPI — physics engine
│   └── .venv/        # Local virtual environment (uv)
├── frontend/         # React + TypeScript + Vite — 3D renderer
├── ImplementationPlan/  # Detailed design documents
├── skills/           # Project-specific agent skills
├── GEMINI.md         # AI agent configuration
└── .env.example      # Environment variable template
```

**Backend** (Python + FastAPI): Runs the physics simulation, serves REST
endpoints for configuration and presets, streams state snapshots over
WebSocket at ~60 FPS.

**Frontend** (React + React Three Fiber): Renders the simulation in an
interactive Three.js scene, connects to the backend via WebSocket for
real-time updates and REST for configuration.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React, TypeScript, Vite, Three.js (R3F), Zustand, Tailwind CSS |
| Backend | Python 3.11+, FastAPI, NumPy, SciPy, Pydantic, uvicorn |
| Communication | WebSocket (simulation stream) + REST (config/presets) |
| Testing | Vitest (frontend), pytest (backend) |
| Tooling | uv (Python), npm (Node), Ruff (Python linting), Storybook |

## Getting Started

> **Note**: This project is under active development.

```bash
# Clone the repository
git clone https://github.com/szcai1998/Three_Body_Simulation.git
cd Three_Body_Simulation

# Backend setup
cd backend
uv venv
uv pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend setup (in another terminal)
cd frontend
npm install
npm run dev
```

## License

TBD