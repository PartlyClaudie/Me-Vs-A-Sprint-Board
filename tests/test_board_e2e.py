import requests
import pytest
from playwright.sync_api import expect
from pages.board_page import BoardPage


@pytest.fixture(autouse=True)
def reset_board():
    requests.post("http://127.0.0.1:5000/api/reset")
    yield


def test_add_task_appears_in_todo(page):
    board = BoardPage(page)
    board.goto()
    board.add_task("Write E2E tests")

    task = board.task_in_column("Write E2E tests", "todo")
    expect(task).to_be_visible()


def test_move_task_from_todo_to_in_progress(page):
    board = BoardPage(page)
    board.goto()
    board.add_task("Review PR")
    board.move_task("Review PR", "todo")

    task = board.task_in_column("Review PR", "in_progress")
    expect(task).to_be_visible()


def test_wip_limit_shows_alert_dialog(page):
    board = BoardPage(page)
    board.goto()

    for i in range(3):
        title = f"Task {i}"
        board.add_task(title)
        expect(board.task_in_column(title, "todo")).to_be_visible()
        board.move_task(title, "todo")
        expect(board.task_in_column(title, "in_progress")).to_be_visible()

    board.add_task("Task 4")
    expect(board.task_in_column("Task 4", "todo")).to_be_visible()

    dialog_message = None
    def handle_dialog(dialog):
        nonlocal dialog_message
        dialog_message = dialog.message
        dialog.accept()

    page.once("dialog", handle_dialog)
    board.move_task("Task 4", "todo")
    page.wait_for_timeout(500)  # give the dialog callback a moment to fire

    assert dialog_message is not None
    assert "WIP limit" in dialog_message


def test_delete_task_removes_it_from_board(page):
    board = BoardPage(page)
    board.goto()
    board.add_task("Temporary task")
    expect(board.task_in_column("Temporary task", "todo")).to_be_visible()

    board.delete_task("Temporary task", "todo")

    task = board.task_in_column("Temporary task", "todo")
    expect(task).to_have_count(0)