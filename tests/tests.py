import requests

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    r = requests.get(f"{BASE_URL}/health")
    assert r.status_code == 200
    print("Health check:", r.json())

def test_create_task():
    payload = {"title": "Test Task", "priority": "high"}
    r = requests.post(f"{BASE_URL}/tasks", json=payload)
    assert r.status_code == 201
    print("Create task:", r.json())
    return r.json()["id"]

def test_get_task(task_id):
    r = requests.get(f"{BASE_URL}/tasks/{task_id}")
    assert r.status_code == 200
    print("Get task:", r.json())

def test_delete_task(task_id):
    r = requests.delete(f"{BASE_URL}/tasks/{task_id}")
    assert r.status_code in (200, 404)
    print("Delete task:", r.json())

if __name__ == "__main__":
    try:
        test_health()
        task_id = test_create_task()
        test_get_task(task_id)
        test_delete_task(task_id)
    except AssertionError as e:
        print("Test failed:", e)
        exit(1)
    print("\033[92mAll tests run successfully.\033[0m") # Green successful message
