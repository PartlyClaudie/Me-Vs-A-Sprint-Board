async function loadTasks() {
    const res = await fetch("/api/tasks");
    const tasks = await res.json();

    document.querySelectorAll(".tasks").forEach(col => col.innerHTML = "");

    tasks.forEach(task => {
        const el = document.createElement("div");
        el.className = "task";
        el.dataset.id = task.id;

        const label = document.createElement("span");
        label.textContent = task.title;
        el.appendChild(label);

        // Move buttons — only show valid next steps
        const nextStatus = getNextStatus(task.status);
        if (nextStatus) {
            const moveBtn = document.createElement("button");
            moveBtn.textContent = "→";
            moveBtn.onclick = () => moveTask(task.id, nextStatus);
            el.appendChild(moveBtn);
        }

        const deleteBtn = document.createElement("button");
        deleteBtn.textContent = "✕";
        deleteBtn.onclick = () => deleteTask(task.id);
        el.appendChild(deleteBtn);

        document.querySelector(`[data-status="${task.status}"] .tasks`).appendChild(el);
    });
}

function getNextStatus(current) {
    if (current === "todo") return "in_progress";
    if (current === "in_progress") return "done";
    return null;
}

async function moveTask(id, newStatus) {
    const res = await fetch(`/api/tasks/${id}/move`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: newStatus })
    });

    if (!res.ok) {
        const err = await res.json();
        alert(err.error);
        return;
    }

    loadTasks();
}

async function deleteTask(id) {
    await fetch(`/api/tasks/${id}`, { method: "DELETE" });
    loadTasks();
}

document.getElementById("add-task-btn").addEventListener("click", async () => {
    const input = document.getElementById("new-task-input");
    const title = input.value.trim();
    if (!title) return;

    await fetch("/api/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title })
    });

    input.value = "";
    loadTasks();
});

loadTasks();