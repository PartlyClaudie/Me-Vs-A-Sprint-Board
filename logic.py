WIP_LIMIT = {"in_progress": 3}


def can_move_task(tasks: dict, task_id: int, new_status: str) -> tuple[bool, str | None]:
    """Returns (allowed, error_message). Pure logic, no Flask involved."""
    if task_id not in tasks:
        return False, "task not found"

    if new_status not in ("todo", "in_progress", "done"):
        return False, "invalid status"

    if new_status in WIP_LIMIT:
        current_count = sum(1 for t in tasks.values() if t["status"] == new_status)
        if current_count >= WIP_LIMIT[new_status]:
            return False, f"WIP limit reached for {new_status}"

    return True, None