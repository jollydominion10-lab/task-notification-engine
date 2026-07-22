import os
import sys
import time
import requests
import firebase_admin
from datetime import datetime, timedelta
from firebase_admin import credentials, firestore

# Locate Firebase key
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEY_PATH = os.path.join(BASE_DIR, "serviceAccountKey.json")

print("--------------------------------------------------")
print("⚡ TASK MANAGEMENT & WEBHOOK SERVICE INITIALIZING...")
print("--------------------------------------------------")

try:
    if not firebase_admin._apps:
        cred = credentials.Certificate(KEY_PATH)
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("✅ Connected to Firebase Cloud Firestore Database!")
except Exception as e:
    print(f"❌ Connection Error: {e}")
    sys.exit()

# Optional: Add a Discord or Slack Webhook URL here
DISCORD_WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL_HERE" 

def create_task_if_not_exists(title, description, priority, due_in_minutes=5):
    """Creates a task only if a pending task with the exact same title doesn't exist."""
    existing_tasks = db.collection("tasks").where("title", "==", title).where("status", "==", "Pending").get()
    
    if len(existing_tasks) > 0:
        print(f"⚠️ Duplicate Task Prevented: '{title}' already exists in Pending status.")
        return None

    due_time = datetime.now() + timedelta(minutes=due_in_minutes)
    
    task_data = {
        "title": title,
        "description": description,
        "priority": priority,  # High, Medium, Low
        "status": "Pending",   # Pending, Completed, Notified
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "due_at": due_time.strftime("%Y-%m-%d %H:%M:%S"),
        "due_timestamp": int(due_time.timestamp())
    }
    
    doc_ref = db.collection("tasks").add(task_data)
    print(f"📌 Task Created: '{title}' (Priority: {priority}) | Due at: {task_data['due_at']}")
    return doc_ref

def send_webhook_notification(task):
    """Triggers an external webhook alert for a due task."""
    message = f"🚨 **TASK DEADLINE ALERT!**\n📌 **Task:** {task['title']}\n📝 **Details:** {task['description']}\n⚠️ **Priority:** {task['priority']}\n⏰ **Due Time:** {task['due_at']}"
    
    print(f"\n🔔 [WEBHOOK TRIGGERED] Sending notification for: '{task['title']}'...")
    print(f"   Payload: {message.replace(chr(10), ' ')}")

    if DISCORD_WEBHOOK_URL and "YOUR_DISCORD" not in DISCORD_WEBHOOK_URL:
        try:
            requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
            print("   ✅ Live Webhook alert delivered successfully!")
        except Exception as e:
            print(f"   ❌ Failed to deliver webhook: {e}")

def check_and_notify_due_tasks():
    """Background monitoring engine that audits upcoming or overdue tasks."""
    print("\n🕵️ Running Task Deadline Monitor...")
    current_time = datetime.now().timestamp()
    
    tasks_ref = db.collection("tasks").where("status", "==", "Pending").get()
    
    notified_count = 0
    for doc in tasks_ref:
        task = doc.to_dict()
        task_id = doc.id
        
        if task.get("due_timestamp", 0) <= (current_time + 60):
            send_webhook_notification(task)
            
            db.collection("tasks").document(task_id).update({
                "status": "Notified",
                "notified_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            notified_count += 1

    if notified_count == 0:
        print("   ✓ All tasks are up to date. No pending deadlines found.")

if __name__ == "__main__":
    print("\n--- 1. Creating Scheduled Tasks (With Deduplication Check) ---")
    create_task_if_not_exists("Backend API Code Review", "Review pull requests for authentication endpoints", "High", due_in_minutes=0)
    create_task_if_not_exists("Update Database Schema", "Add index fields to Firestore tasks", "Medium", due_in_minutes=15)

    time.sleep(1)

    print("\n--- 2. Running Background Notification Monitor ---")
    check_and_notify_due_tasks()

    print("\n--------------------------------------------------")
    print("🎉 TASK ENGINE COMPLETED RUN SUCCESSFULLY!")
    print("--------------------------------------------------")