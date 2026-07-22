# ⏱️ Task Notification Engine & Real-Time Dashboard

A full-stack, microservice-architected task scheduling and deadline monitoring platform. The system combines an asynchronous Python background polling engine with a real-time JavaScript web dashboard to track task lifetimes, execute deduplication guards, and trigger multi-channel alerts upon deadline expiration.

---

## 🌟 Key Features

* **⏱️ Flexible Multi-Day Countdowns:** Schedule tasks down to Days, Hours, and Minutes with real-time ticking UI updates.
* **🚨 Multi-Channel Alert System:** Fires Web Audio API alarm sounds, browser system notifications, and modal pop-ups the moment deadlines hit zero.
* **📊 Progress & Goal Tracking:** Interactive completion metrics and progress bars synchronized live across sessions.
* **🛡️ Backend Deduplication Guards:** Python service prevents redundant task creation by auditing database state before insertion.
* **⚡ Real-Time Cloud Sync:** Built on Cloud Firestore listeners (`onSnapshot`) for instant sub-second dashboard updates.
* **👋 Interactive Onboarding:** Clean welcome screen explaining the microservice architecture before granting app access.

---

## 📐 System Architecture

```text
  ┌──────────────────────┐          ┌─────────────────────────┐
  │   User Interface     │          │   Python Engine Service │
  │ (HTML5/ES6 Dashboard)│          │  (Polling & Validation) │
  └──────────┬───────────┘          └────────────┬────────────┘
             │                                   │
             │ Real-time Stream                  │ Admin SDK Check
             ▼                                   ▼
  ┌───────────────────────────────────────────────────────────┐
  │               Google Cloud Firestore DB                   │
  └──────────────────────────────┬────────────────────────────┘
                                 │
                                 │ Overdue Deadline Trigger
                                 ▼
                    ┌──────────────────────────┐
                    │ Webhooks / Audio Alarms  │
                    └──────────────────────────┘
