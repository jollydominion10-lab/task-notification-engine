# Task Notification Engine

A task dashboard with deadlines and alerts.

This is a software project. The live demo is a web dashboard.
The Python file can create tasks in Firestore and send webhook alerts when a task is due.

Live demo: https://jollydominion10-lab.github.io/task-notification-engine/

## What it does
- Lets you add tasks with a countdown
- Shows progress in the dashboard
- Can play an alert when a deadline is reached
- Includes a Python helper in `task_engine.py` that checks due tasks

## Tech
- HTML, CSS, JavaScript
- Python
- Firebase / Firestore
- Optional Discord webhook

## How to run the dashboard
Open the live demo, or open `index.html` in a browser.

## How to run the Python helper
```bash
pip install -r requirements.txt
python task_engine.py
