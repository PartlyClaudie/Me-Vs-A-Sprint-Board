from logic import can_move_task


def make_tasks(statuses):
    """Helper: build a fake tasks dict from a list of statuses.
    e.g. make_tasks(["todo", "in_progress", "in_progress"])
    """
    return {
        i + 1: {"id": i + 1, "title": f"Task {i+1}", "status": status}
        for i, status in enumerate(statuses)
    }


def test_move_allowed_when_under_wip_limit():
    tasks = make_tasks(["todo", "in_progress"])
    allowed, error = can_move_task(tasks, 1, "in_progress")

    assert allowed is True
    assert error is None


def test_move_blocked_when_wip_limit_reached():
    tasks = make_tasks(["todo", "in_progress", "in_progress", "in_progress"])
    allowed, error = can_move_task(tasks, 1, "in_progress")

    assert allowed is False
    assert error == "WIP limit reached for in_progress"


def test_move_to_done_not_subject_to_wip_limit():
    tasks = make_tasks(["in_progress", "in_progress", "in_progress"])
    allowed, error = can_move_task(tasks, 1, "done")

    assert allowed is True
    assert error is None


def test_move_nonexistent_task_returns_not_found():
    tasks = make_tasks(["todo"])
    allowed, error = can_move_task(tasks, 999, "in_progress")

    assert allowed is False
    assert error == "task not found"


def test_move_to_invalid_status_is_rejected():
    tasks = make_tasks(["todo"])
    allowed, error = can_move_task(tasks, 1, "archived")

    assert allowed is False
    assert error == "invalid status"


def test_wip_limit_counts_only_current_status_not_others():
    # 3 todo + 2 done shouldn't affect the in_progress WIP count at all
    tasks = make_tasks(["todo", "todo", "todo", "done", "done"])
    allowed, error = can_move_task(tasks, 1, "in_progress")

    assert allowed is True
    assert error is None