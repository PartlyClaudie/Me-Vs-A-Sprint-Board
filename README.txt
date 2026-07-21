# Sprint Board

[![Sprint Board Tests](https://github.com/PartlyClaudie/Me-Vs-A-Sprint-Board/actions/workflows/tests.yml/badge.svg)](https://github.com/PartlyClaudie/Me-Vs-A-Sprint-Board/actions/workflows/tests.yml)

A minimal Kanban-style sprint task board (To Do / In Progress / Done),
built with Flask and vanilla JavaScript — created as the flagship
project in my testing portfolio: an app I own end-to-end, tested
across all three layers of the testing pyramid.

## Why this project
My earlier portfolio projects tested other people's apps (the-internet,
restful-booker). This one flips that — I designed, built, and tested
my own application, including a real piece of business logic: a
Work-In-Progress (WIP) limit, a genuine Scrum practice that caps
"In Progress" at 3 tasks at once.

## Tech stack
- **Backend:** Python, Flask
- **Frontend:** Vanilla JavaScript, HTML/CSS
- **Testing:** pytest, Flask test client, Playwright

## Architecture & testing strategy
This project is deliberately structured to demonstrate the full
testing pyramid against one real codebase:

| Layer | Tool | What it tests | Speed |
|---|---|---|---|
| Unit | pytest | `can_move_task()` — the WIP limit rule, in isolation, no server involved | Milliseconds |
| API | pytest + Flask test client | Real HTTP status codes, routing, and request/response shape | Fast (in-process) |
| E2E | Playwright | The actual UI — clicking, dragging, and the WIP-limit alert dialog a real user would see | Slower (real browser) |

The WIP limit rule is tested at all three layers deliberately — each
layer catches a different class of bug: unit tests confirm the logic
itself is correct, API tests confirm it's correctly wired into the
endpoint (right status code, right error message), and E2E tests
confirm it's correctly surfaced to an actual user.

## Setup
\`\`\`bash
python -m venv venv
source venv/Scripts/activate   # Windows Git Bash
pip install -r requirements.txt
playwright install
\`\`\`

## Run the app
\`\`\`bash
python app.py
\`\`\`
Visit http://127.0.0.1:5000

## Run tests
\`\`\`bash
# Unit + API tests (no server needed)
pytest tests/test_logic.py tests/test_api.py -v

# E2E tests (requires the app running separately — see above)
pytest tests/test_board_e2e.py -v --headed
\`\`\`

## Lessons learned
- Separated business logic (`logic.py`) from the Flask route layer
  specifically to make it unit-testable without HTTP or a server —
  this made the WIP limit rule fast and simple to test in isolation.
- Learned to consistently use Playwright's `expect()` over plain
  `assert` for anything that changes the DOM asynchronously — mixing
  the two caused real, confusing flaky failures during development
  (see E2E test history for the specific bug).
- Built a CI pipeline that runs unit/API tests first (fast, no
  dependencies) before booting a live server and running slower E2E
  tests — including a readiness-polling step so CI doesn't race
  ahead of the server actually being up.
- Added a test-only `/api/reset` endpoint to give E2E tests a clean,
  predictable server state before each test, avoiding cross-test
  pollution from the in-memory task store.

## Related portfolio projects
- [Manual test cases & bug reports](https://github.com/PartlyClaudie/Me-Vs-the-internet)
- [API automation (restful-booker)](https://github.com/PartlyClaudie/Me-Vs-restful-booker)
- [UI automation (Playwright, the-internet)](https://github.com/PartlyClaudie/Me-Vs-Playwright)