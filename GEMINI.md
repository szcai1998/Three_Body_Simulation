# Three Body Simulation

## Project Overview

Interactive 2D gravitational simulation (Two/Three-Body Problem) rendered in 3D
space. Educational tool with a high-tech sci-fi aesthetic, designed to visualize
gravitational dynamics, compare numerical integrators, and explore chaotic
orbital mechanics. Built as a portfolio piece targeting physics enthusiasts,
casual science explorers, and recruiters.

## Architecture

Monorepo with separate frontend and backend:

- **Frontend** (`/frontend`): React + TypeScript + Vite. Renders the simulation
  using Three.js via React Three Fiber. Pure renderer with client-side
  interpolation between server frames.
- **Backend** (`/backend`): Python 3.11+ / FastAPI. Runs the physics simulation
  engine. Serves the built frontend in production.
- **Communication**: WebSocket for real-time simulation streaming (~60 FPS),
  REST API for configuration, presets, and state management.
- **State Authority**: Backend owns all simulation state. Frontend interpolates
  between server snapshots for smooth rendering.
- **Concurrency**: Single-user (one simulation instance at a time).

## Tech Stack

### Frontend
- **Language**: TypeScript
- **Framework**: React
- **3D Rendering**: Three.js via React Three Fiber (R3F)
- **Camera/Helpers**: @react-three/drei
- **Post-processing**: @react-three/postprocessing (UnrealBloomPass)
- **State Management**: Zustand
- **Styling**: Tailwind CSS (custom dark sci-fi theme)
- **Build Tool**: Vite
- **Testing**: Vitest
- **Component Dev**: Storybook
- **Package Manager**: npm

### Backend
- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Physics**: NumPy, SciPy (ODE validation)
- **Data Validation**: Pydantic
- **Server**: uvicorn
- **WebSocket**: FastAPI WebSocket support
- **Testing**: pytest
- **Linting/Formatting**: Ruff
- **Package Manager**: uv (local .venv inside /backend, never global)

### Shared
- **Vector Math**: Generic VectorN (2D physics now, 3D-ready)
- **Communication**: WebSocket (simulation stream) + REST (config/presets)

## Coding Standards

### General
- Follow KISS and DRY principles.
- Use descriptive variable names. No single-letter variables except loop
  counters (`i`, `j`, `k`) and mathematical formulas (`r`, `v`, `a`, `F`, `G`).
- Keep components and functions small. Extract when over 100 lines.
- Use Conventional Commits: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`.

### TypeScript (Frontend)
- Use TypeScript with standard strictness settings.
- Use functional React components only. No class components.
- Use ES Modules only. No CommonJS `require`.
- Prefer named exports over default exports.
- Prefer `const` over `let`. Never use `var`.
- Use Tailwind CSS classes for styling. Never use inline styles.

### Python (Backend)
- Target Python 3.11+.
- Use type hints on all function signatures.
- Use Pydantic models for all API request/response schemas.
- Use Ruff for linting and formatting.
- Keep the virtual environment local to `/backend/.venv`.

## Agent Configuration

### Active Skills
- modern-web-guidance (HTML/CSS/JS best practices)
- fupan (project retrospective)
- init-agy (project bootstrapping)
- workflow-skill-creator (save reusable workflows)

### Disabled Skills
Disable ALL science/bioinformatics skills for this project. They are irrelevant:
alphafold, alphagenome, chembl, clinical-trials, clinvar, dbsnp, embl-ebi-ols,
encode-ccres, ensembl, foldseek, gnomad, gtex, human-protein-atlas, interpro,
jaspar, literature-search-arxiv, literature-search-biorxiv,
literature-search-europepmc, literature-search-openalex, ncbi-sequence-fetch,
openfda, opentargets, pdb, protein-sequence-msa,
protein-sequence-similarity-search, pubchem, pubmed, pymol, quickgo, reactome,
science-skills-common, string, ucsc-conservation-and-tfbs, unibind, uniprot, uv.

### Safety Policy
Standard: Allow file reads freely. Confirm before running commands.

### Subagent Policy
Subagents are allowed to write files for faster parallel work.

### Skill Distillation
Automatic. Offer to create skills after complex multi-step workflows.

### Uncertainty Handling
Use /grill-me style questioning for complex or ambiguous decisions.
Make quick reasonable choices for simple decisions and explain reasoning.

## Never Do (Hard Rules)

- Never use the `any` type in TypeScript. Always use proper typing.
- Never modify lock files (package-lock.json, uv.lock) manually.
- Never use inline styles. Use Tailwind classes or CSS.
- Never commit `.env` files with real secrets.
- Never use the `var` keyword in TypeScript/JavaScript.
- Never leave commented-out code in commits.
- Never use magic numbers without named constants.

## Always Do (Mandatory Practices)

- Always add JSDoc/TSDoc comments on exported functions and types.
- Always write unit tests for physics and math functions.
- Always check that TypeScript compiles cleanly before committing.
- Always maintain energy conservation diagnostics in the simulation.
- Always use semantic HTML where applicable.
- Always handle edge cases (division by zero, NaN, Infinity, etc.).
