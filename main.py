from __future__ import annotations

import json
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse

DATA_FILE = Path(__file__).with_name("data.json")


def default_data() -> dict:
    return {
        "user": {
            "name": "Ghulam",
            "avatar": "https://i.pravatar.cc/100?img=12",
            "pending": 6,
        },
        "stats": {"done": 22, "in_progress": 7, "ongoing": 10, "waiting_review": 12},
        "tasks": [
            {
                "id": 1,
                "title": "Mobile App Design",
                "assignees": ["Mike", "Anita"],
                "time": "09:00 - 10:00",
                "status": "in_progress",
                "date": "2026-04-12",
            },
            {
                "id": 2,
                "title": "Software Testing",
                "assignees": ["Anita", "David"],
                "time": "10:00 - 11:20",
                "status": "ongoing",
                "date": "2026-04-12",
            },
            {
                "id": 3,
                "title": "Web Development",
                "assignees": ["Mike", "Anita"],
                "time": "13:00 - 14:00",
                "status": "waiting_review",
                "date": "2026-04-12",
            },
        ],
    }


def load_data() -> dict:
    if not DATA_FILE.exists():
        save_data(default_data())
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def save_data(data: dict) -> None:
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


class APIHandler(BaseHTTPRequestHandler):
    def _send_json(self, payload: dict | list, status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        data = load_data()

        if path == "/api/health":
            return self._send_json({"ok": True, "timestamp": datetime.utcnow().isoformat() + "Z"})

        if path == "/api/dashboard":
            return self._send_json(
                {
                    "user": data["user"],
                    "stats": data["stats"],
                    "featured_task": data["tasks"][0] if data["tasks"] else None,
                }
            )

        if path == "/api/tasks":
            return self._send_json(data["tasks"])

        return self._send_json({"error": "not found"}, 404)

    def do_POST(self):
        path = urlparse(self.path).path
        data = load_data()

        if path == "/api/tasks":
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length) or b"{}")
            if not payload.get("title"):
                return self._send_json({"error": "title is required"}, 400)

            task = {
                "id": max([task["id"] for task in data["tasks"]], default=0) + 1,
                "title": payload["title"],
                "assignees": payload.get("assignees", ["Unassigned"]),
                "time": payload.get("time", "00:00 - 00:30"),
                "status": payload.get("status", "ongoing"),
                "date": payload.get("date", "2026-04-12"),
            }
            data["tasks"].append(task)
            data["user"]["pending"] = len(data["tasks"])
            save_data(data)
            return self._send_json(task, 201)

        if path.startswith("/api/tasks/") and path.endswith("/complete"):
            task_id = int(path.split("/")[3])
            task = next((task for task in data["tasks"] if task["id"] == task_id), None)
            if not task:
                return self._send_json({"error": "task not found"}, 404)

            task["status"] = "done"
            data["stats"]["done"] += 1
            data["stats"]["in_progress"] = max(0, data["stats"]["in_progress"] - 1)
            save_data(data)
            return self._send_json(task)

        return self._send_json({"error": "not found"}, 404)


def run() -> None:
    server = HTTPServer(("0.0.0.0", 8000), APIHandler)
    print("API running on http://0.0.0.0:8000")
    server.serve_forever()


if __name__ == "__main__":
    run()
