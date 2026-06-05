import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_api_presets():
    response = client.get("/api/presets")
    assert response.status_code == 200
    data = response.json()
    assert "presets" in data
    assert "figure8" in data["presets"]

def test_api_init_and_state():
    # Initialize a preset
    response = client.post("/api/init?preset=binary_orbit")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    
    # Fetch state and verify
    response = client.get("/api/state")
    assert response.status_code == 200
    state = response.json()
    assert len(state["bodies"]) == 2
    
def test_api_config_update():
    # Update config
    response = client.put("/api/config", json={"G": 2.5, "chaos_mode": True})
    assert response.status_code == 200
    
    # Fetch state and verify
    response = client.get("/api/state")
    assert response.status_code == 200
    state = response.json()
    assert state["G"] == 2.5
    assert state["chaos_mode"] is True

def test_api_body_crud():
    # Add body
    new_body = {
        "id": "test_body",
        "mass": 5.0,
        "position": {"components": [1.0, 2.0, 3.0]},
        "velocity": {"components": [0.0, 0.0, 0.0]},
        "acceleration": {"components": [0.0, 0.0, 0.0]},
        "trail": []
    }
    response = client.post("/api/body", json=new_body)
    assert response.status_code == 200
    
    # Verify body exists
    state = client.get("/api/state").json()
    body_ids = [b["id"] for b in state["bodies"]]
    assert "test_body" in body_ids
    
    # Update body
    response = client.put("/api/body/test_body", json={"mass": 10.0})
    assert response.status_code == 200
    
    state = client.get("/api/state").json()
    updated_body = next(b for b in state["bodies"] if b["id"] == "test_body")
    assert updated_body["mass"] == 10.0
    
    # Delete body
    response = client.delete("/api/body/test_body")
    assert response.status_code == 200
    
    state = client.get("/api/state").json()
    body_ids = [b["id"] for b in state["bodies"]]
    assert "test_body" not in body_ids
