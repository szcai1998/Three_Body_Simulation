# Three-Body Simulation Frontend

This is the frontend for the Three-Body Simulation project, built with React, TypeScript, Vite, and Three.js (via React Three Fiber).

## Running the Frontend

To start the local development server:

1. Ensure the Python backend is running first (it handles the simulation physics over WebSockets).
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the Vite server:
   ```bash
   npm run dev
   ```
4. Open [http://localhost:5173](http://localhost:5173) in your browser.

## Architecture & Communication
The frontend is a pure renderer. It does not compute physics.
- **WebSocket (`/ws/simulation`)**: Receives the physics state at ~60Hz from the Python backend and updates the `useSimulationStore`.
- **REST API (`/api/config`, `/api/state`)**: Used to fetch the initial state and send user configuration changes (playback speed, chaos mode toggles, etc.).
- **Zustand (`useSimulationStore.ts`)**: Serves as the central state management for React components, ensuring high-performance reactive updates without prop-drilling.

## Recent Bug Fixes & Post-Mortem

### 1. The "Black Screen" WebGL Crash
**Issue:** The website would show a completely black screen or freeze instantly after loading.
**Cause:** The `@react-three/postprocessing` `Bloom` effect was configured with `mipmapBlur`. On certain Linux drivers or WebGL implementations without full `OES_texture_float_linear` support, generating mipmaps for floating-point HDR textures causes a hard crash in the WebGL context, resulting in a black canvas.
**Fix:** Removed `mipmapBlur` from the Bloom pass. The renderer now safely outputs glowing effects without hardware-crashing mipmap generation.

### 2. Disappearing Stars (Clipping)
**Issue:** When zooming out the camera to view large orbital presets (like Sun-Earth-Moon), the background stars and celestial bodies would suddenly vanish.
**Cause:**
- The `OrbitControls` had a `maxDistance` of `100`, preventing users from zooming out far enough to see the system.
- The background `<Stars>` component was hardcoded to a radius of `100`. When the camera zoomed out near that distance, it clipped *through* the stars, making them disappear.
- Massive bodies (like the Sun) had their visual radius capped at `0.5`, making them smaller than a single pixel when viewed from a large distance.
**Fix:**
- Increased camera `far` plane to `10000` and `OrbitControls` `maxDistance` to `5000`.
- Expanded the background `<Stars>` radius to `5000` and increased their `factor` so they remain visible from any practical zoom level.
- Scaled up the visual radius cap for massive stars to `3.0` so they remain highly visible from afar.

### 3. Frozen Simulation (Backend Desync)
**Issue:** The simulation bodies were visible but frozen in place, and trails were not drawing.
**Cause:** A type error in the Python backend's physics loop caused the background simulation task to crash silently. Because the `uvicorn` server was stuck, the frontend WebSocket connected successfully but never received any data updates, leaving the UI frozen at the starting coordinates.
**Fix:** Restarted the backend server with the proper types and added a robust `try/except` handler in the backend physics loop to prevent silent failures in the future.
