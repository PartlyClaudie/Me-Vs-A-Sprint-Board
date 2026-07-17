from flask import Flask, jsonify, request, render_template

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
    if task_id not in tasks:
        return jsonify({"error": "task not found"}), 404

    data = request.get_json()
    new_status = data.get("status")

    if new_status not in ("todo", "in_progress", "done"):
        return jsonify({"error": "invalid status"}), 400

    if new_status in WIP_LIMIT:
        current_count = sum(1 for t in tasks.values() if t["status"] == new_status)
        if current_count >= WIP_LIMIT[new_status]:
            return jsonify({"error": f"WIP limit reached for {new_status}"}), 409

    tasks[task_id]["status"] = new_status
    return jsonify(tasks[task_id])


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    if task_id not in tasks:
        return jsonify({"error": "task not found"}), 404

    del tasks[task_id]
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)