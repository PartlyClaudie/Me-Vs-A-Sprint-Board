class BoardPage:
    URL = "http://127.0.0.1:5000"

    def __init__(self, page):
        self.page = page
        self.new_task_input = page.locator("#new-task-input")
        self.add_task_button = page.locator("#add-task-btn")

    def goto(self):
        self.page.goto(self.URL)

    def add_task(self, title):
        self.new_task_input.fill(title)
        self.add_task_button.click()

    def task_in_column(self, title, status):
        column = self.page.locator(f'[data-status="{status}"] .tasks')
        return column.locator(".task", has_text=title)

    def move_task(self, title, current_status):
        task = self.task_in_column(title, current_status)
        task.locator("button", has_text="→").click()

    def delete_task(self, title, status):
        task = self.task_in_column(title, status)
        task.locator("button", has_text="✕").click()