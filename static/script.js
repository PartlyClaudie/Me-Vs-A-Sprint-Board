async function loadTasks() {
    const res = await fetch("/api/tasks");
    const tasks = await res.json();

    document.querySelectorAll(".tasks").forEach(col => col.innerHTML = "");

    tasks.forEach(task => {
        const el = document.createElement("div");
        el.textContent = task.title;
        el.className = "task";
        el.dataset.id = task.id;
        document.querySelector(`[data-status="${task.status}"] .tasks`).appendChild(el);
    });
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