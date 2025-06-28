from fastapi.testclient import TestClient
from app.api import app 

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200


def test_create_get_delete_task():
    # Create a task
    payload = {
        "title": "Test Task",
        "priority": "high"
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    task_id = data.get("id")
    assert task_id is not None

    # Get the created task
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"

    # Update the task
    update_payload = {"status": "completed", "title": "Updated Task"}
    response = client.put(f"/tasks/{task_id}", json=update_payload)
    assert response.status_code == 200
    updated_data = response.json()
    assert updated_data["status"] == "completed"
    assert updated_data["title"] == "Updated Task"
    
    # Delete the task
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code in (200, 404)
