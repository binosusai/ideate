from __future__ import annotations

import json
import sqlite3
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "poc.sqlite3"
FRONTEND = ROOT / "frontend"
IDEA_TITLE = 'Local contractor quote comparison tool'
IDEA_CATEGORY = 'money'


def init_db() -> None:
    with sqlite3.connect(DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS runs (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              input TEXT NOT NULL,
              recommendation TEXT NOT NULL,
              created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)


def create_recommendation(raw: str) -> str:
    text = raw.strip() or "No input provided."
    return (
        f"POC recommendation for {IDEA_TITLE}: start with one user workflow, "
        f"turn this input into a visible before/after, and capture the next manual approval. "
        f"Input reviewed: {text[:240]}"
    )


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FRONTEND), **kwargs)

    def do_GET(self):
        if urlparse(self.path).path == "/api/health":
            self.send_json({"ok": True, "idea": IDEA_TITLE, "category": IDEA_CATEGORY})
            return
        super().do_GET()

    def do_POST(self):
        if urlparse(self.path).path != "/api/run":
            self.send_error(404)
            return
        length = int(self.headers.get("content-length", "0"))
        payload = json.loads(self.rfile.read(length) or b"{}")
        raw = str(payload.get("input", ""))
        recommendation = create_recommendation(raw)
        with sqlite3.connect(DB) as conn:
            conn.execute(
                "INSERT INTO runs(input, recommendation) VALUES (?, ?)",
                (raw, recommendation),
            )
        self.send_json({"recommendation": recommendation})

    def send_json(self, payload):
        data = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def main() -> None:
    init_db()
    server = ThreadingHTTPServer(("127.0.0.1", 8000), Handler)
    print("POC running at http://localhost:8000")
    print("Press Ctrl+C to stop.")
    server.serve_forever()


if __name__ == "__main__":
    main()
