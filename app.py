from flask import Flask, jsonify, request, render_template
from logic import can_move_task

app = Flask(__name__)

# In-memory "database" — resets every time the app restarts
tasks = {}
next_id = 1

WIP_LIMIT = {"in_progress": 3}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    return jsonify(list(tasks.values()))


@app.route("/api/tasks", methods=["POST"])
def create_task():
    global next_id
    data = request.get_json()

    if not data or not data.get("title"):
        return jsonify({"error": "title is required"}), 400

    task = {
        "id": next_id,
        "title": data["title"],
        "status": "todo"
    }
    tasks[next_id] = task
    next_id += 1
    return jsonify(task), 201


@app.route("/api/tasks/<int:task_id>/move", methods=["PUT"])
def move_task(task_id):
    data = request.get_json()
    new_status = data.get("status")

    allowed, error = can_move_task(tasks, task_id, new_status)
    if not allowed:
        status_code = 404 if error == "task not found" else (409 if "WIP limit" in error else 400)
        return jsonify({"error": error}), status_code

    tasks[task_id]["status"] = new_status
    return jsonify(tasks[task_id])


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    if task_id not in tasks:
        return jsonify({"error": "task not found"}), 404

    del tasks[task_id]
    return "", 204

@app.route("/api/reset", methods=["POST"])
def reset():
    tasks.clear()
    global next_id
    next_id = 1
    return "", 204

if __name__ == "__main__":
    app.run(debug=True)


