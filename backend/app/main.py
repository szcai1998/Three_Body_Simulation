import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List

from .models import SimulationState, Body
from .physics import step_simulation
from .presets import PRESETS

app = FastAPI(title="Three Body Simulation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global singleton simulation state
global_state = PRESETS["figure8"]()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast_state(self):
        if not self.active_connections:
            return
            
        state_dict = global_state.model_dump()
        
        # A list to collect disconnected websockets
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(state_dict)
            except Exception:
                disconnected.append(connection)
                
        for d in disconnected:
            self.disconnect(d)

manager = ConnectionManager()


import time

async def physics_loop():
    """
    Background task that continuously advances the physics simulation
    and broadcasts the state at ~60 FPS.
    """
    target_dt = 1 / 60.0
    while True:
        try:
            start_time = time.perf_counter()
            print("physics_loop tick:", global_state.time)
            if global_state.running:
                # Advance simulation
                for _ in range(int(global_state.playback_speed)):
                    step_simulation(global_state)
                # Broadcast state
                await manager.broadcast_state()
                # Throttle to approximately 60 FPS accurately
                elapsed = time.perf_counter() - start_time
                sleep_time = max(0.0, target_dt - elapsed)
                await asyncio.sleep(sleep_time)
            else:
                # When paused, broadcast occasionally so UI stays in sync with any REST updates
                await manager.broadcast_state()
                await asyncio.sleep(0.1)
        except Exception as e:
            import traceback
            with open("physics_error.log", "a") as f:
                f.write(traceback.format_exc() + "\n")
            await asyncio.sleep(1)


@app.on_event("startup")
async def startup_event():
    # Start the background physics loop when the FastAPI app starts
    asyncio.create_task(physics_loop())


@app.websocket("/ws/simulation")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Listen for client commands via websocket
            data = await websocket.receive_json()
            command = data.get("command")
            
            if command == "start":
                global_state.running = True
            elif command == "pause":
                global_state.running = False
            elif command == "step":
                global_state.running = False
                step_simulation(global_state)
                await manager.broadcast_state()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# --- REST Endpoints ---

@app.get("/api/state", response_model=SimulationState)
def get_state():
    return global_state

@app.post("/api/init")
def init_simulation(preset: str = "figure8"):
    global global_state
    if preset in PRESETS:
        global_state = PRESETS[preset]()
        return {"status": "ok", "preset": preset}
    return {"status": "error", "message": "Preset not found"}

@app.post("/api/reset")
def reset_simulation():
    global global_state
    global_state = PRESETS["figure8"]()
    return {"status": "ok"}

@app.put("/api/config")
def update_config(config: Dict[str, Any]):
    if config.get("integrator") == "kepler" and len(global_state.bodies) > 2:
        return {"status": "error", "message": "Cannot use Kepler integrator with more than 2 bodies."}
        
    for k, v in config.items():
        if hasattr(global_state, k):
            setattr(global_state, k, v)
    return {"status": "ok"}

@app.get("/api/presets")
def list_presets():
    return {"presets": list(PRESETS.keys())}

@app.post("/api/body")
def add_body(body: Body):
    if global_state.integrator == "kepler" and len(global_state.bodies) >= 2:
        return {"status": "error", "message": "Cannot add >2 bodies when using Kepler integrator."}
    global_state.bodies.append(body)
    return {"status": "ok"}

@app.put("/api/body/{body_id}")
def update_body(body_id: str, updates: Dict[str, Any]):
    from .models import VectorN
    for b in global_state.bodies:
        if b.id == body_id:
            for k, v in updates.items():
                if hasattr(b, k):
                    if k in ["position", "velocity", "acceleration"]:
                        setattr(b, k, VectorN(**v))
                    else:
                        setattr(b, k, v)
            return {"status": "ok"}
    return {"status": "error", "message": "Body not found"}

@app.delete("/api/body/{body_id}")
def delete_body(body_id: str):
    global global_state
    global_state.bodies = [b for b in global_state.bodies if b.id != body_id]
    return {"status": "ok"}

# --- Static Files ---
import os
from fastapi.staticfiles import StaticFiles

frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend/dist"))
if os.path.isdir(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="static")
else:
    print(f"Warning: Frontend dist folder not found at {frontend_dist}. Run `npm run build` in frontend.")
