def test_create_task_returns_201_and_task_data(client):
    response = client.post("/api/tasks", json={"title": "Write tests"})
    assert response.status_code == 201

    body = response.get_json()
    assert body["title"] == "Write tests"
    assert body["status"] == "todo"


def test_create_task_without_title_returns_400(client):
    response = client.post("/api/tasks", json={})
    assert response.status_code == 400


def test_get_tasks_returns_created_tasks(client):
    client.post("/api/tasks", json={"title": "Task A"})
    client.post("/api/tasks", json={"title": "Task B"})

    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert len(response.get_json()) == 2


def test_move_task_to_valid_status(client):
    create_response = client.post("/api/tasks", json={"title": "Task A"})
    task_id = create_response.get_json()["id"]

    move_response = client.put(f"/api/tasks/{task_id}/move", json={"status": "in_progress"})
    assert move_response.status_code == 200
    assert move_response.get_json()["status"] == "in_progress"


def test_wip_limit_enforced_via_api(client):
    # fill in_progress to the limit (3)
    for i in range(3):
        task = client.post("/api/tasks", json={"title": f"Task {i}"}).get_json()
        client.put(f"/api/tasks/{task['id']}/move", json={"status": "in_progress"})

    # 4th task should be rejected
    fourth = client.post("/api/tasks", json={"title": "Task 4"}).get_json()
    response = client.put(f"/api/tasks/{fourth['id']}/move", json={"status": "in_progress"})

    assert response.status_code == 409
    assert "WIP limit" in response.get_json()["error"]


def test_move_nonexistent_task_returns_404(client):
    response = client.put("/api/tasks/999/move", json={"status": "in_progress"})
    assert response.status_code == 404


def test_delete_task_removes_it(client):
    task = client.post("/api/tasks", json={"title": "Task A"}).get_json()

    delete_response = client.delete(f"/api/tasks/{task['id']}")
    assert delete_response.status_code == 204

    get_response = client.get("/api/tasks")
    assert get_response.get_json() == []


def test_delete_nonexistent_task_returns_404(client):
    response = client.delete("/api/tasks/999")
    assert response.status_code == 404