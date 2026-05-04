from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable

from .models import CATEGORIES, STATUSES, Idea
from .text import ranchi_codename


MAX_IDEA_SLUG_LEN = 12


def _alpha_suffix(index: int) -> str:
    letters = "abcdefghijklmnopqrstuvwxyz"
    token = ""
    n = max(1, index)
    while n > 0:
        n, rem = divmod(n - 1, 26)
        token = letters[rem] + token
    return token


SCHEMA = """
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS ideas (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  slug TEXT NOT NULL UNIQUE,
  category TEXT NOT NULL CHECK(category IN ('money', 'personal')),
  why TEXT NOT NULL DEFAULT '',
  status TEXT NOT NULL DEFAULT 'captured',
  score REAL NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS artifacts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  idea_id INTEGER NOT NULL REFERENCES ideas(id) ON DELETE CASCADE,
  kind TEXT NOT NULL,
  content TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS decisions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  idea_id INTEGER NOT NULL REFERENCES ideas(id) ON DELETE CASCADE,
  decision TEXT NOT NULL,
  rationale TEXT NOT NULL DEFAULT '',
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS runs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  idea_id INTEGER REFERENCES ideas(id) ON DELETE SET NULL,
  kind TEXT NOT NULL,
  summary TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


class Store:
    def __init__(self, path: Path):
        self.path = path

    def connect(self) -> sqlite3.Connection:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys=ON")
        return conn

    def init(self) -> None:
        with self.connect() as conn:
            conn.executescript(SCHEMA)

    def add_idea(self, title: str, category: str, why: str) -> Idea:
        if category not in CATEGORIES:
            raise ValueError(f"category must be one of: {', '.join(sorted(CATEGORIES))}")

        base_slug = ranchi_codename(title, max_len=MAX_IDEA_SLUG_LEN)
        with self.connect() as conn:
            slug = self._unique_slug(conn, base_slug)
            score = initial_score(title, category, why)
            conn.execute(
                """
                INSERT INTO ideas(title, slug, category, why, score)
                VALUES (?, ?, ?, ?, ?)
                """,
                (title.strip(), slug, category, why.strip(), score),
            )
            row = conn.execute("SELECT * FROM ideas WHERE slug = ?", (slug,)).fetchone()
        return row_to_idea(row)

    def get_idea(self, idea_id: int) -> Idea:
        with self.connect() as conn:
            row = conn.execute("SELECT * FROM ideas WHERE id = ?", (idea_id,)).fetchone()
        if row is None:
            raise KeyError(f"idea {idea_id} was not found")
        return row_to_idea(row)

    def list_ideas(self, status: str | None = None) -> list[Idea]:
        with self.connect() as conn:
            if status:
                rows = conn.execute(
                    "SELECT * FROM ideas WHERE status = ? ORDER BY score DESC, updated_at DESC",
                    (status,),
                ).fetchall()
            else:
                rows = conn.execute(
                    """
                    SELECT * FROM ideas
                    ORDER BY
                      CASE category WHEN 'money' THEN 0 ELSE 1 END,
                      score DESC,
                      updated_at DESC
                    """
                ).fetchall()
        return [row_to_idea(row) for row in rows]

    def set_status(self, idea_id: int, status: str) -> None:
        if status not in STATUSES:
            raise ValueError(f"unknown status: {status}")
        with self.connect() as conn:
            conn.execute(
                "UPDATE ideas SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (status, idea_id),
            )

    def add_artifact(self, idea_id: int, kind: str, content: str) -> None:
        with self.connect() as conn:
            conn.execute(
                "INSERT INTO artifacts(idea_id, kind, content) VALUES (?, ?, ?)",
                (idea_id, kind, content),
            )

    def latest_artifact(self, idea_id: int, kind: str) -> str | None:
        with self.connect() as conn:
            row = conn.execute(
                """
                SELECT content FROM artifacts
                WHERE idea_id = ? AND kind = ?
                ORDER BY created_at DESC, id DESC
                LIMIT 1
                """,
                (idea_id, kind),
            ).fetchone()
        return None if row is None else str(row["content"])

    def add_decision(self, idea_id: int, decision: str, rationale: str = "") -> None:
        with self.connect() as conn:
            conn.execute(
                "INSERT INTO decisions(idea_id, decision, rationale) VALUES (?, ?, ?)",
                (idea_id, decision, rationale),
            )

    def log_run(self, kind: str, summary: str, idea_id: int | None = None) -> None:
        with self.connect() as conn:
            conn.execute(
                "INSERT INTO runs(idea_id, kind, summary) VALUES (?, ?, ?)",
                (idea_id, kind, summary),
            )

    def _unique_slug(self, conn: sqlite3.Connection, base_slug: str) -> str:
        slug = (base_slug or "ranchi")[:MAX_IDEA_SLUG_LEN]
        candidate = slug
        suffix = 1
        while conn.execute("SELECT 1 FROM ideas WHERE slug = ?", (candidate,)).fetchone():
            tag = _alpha_suffix(suffix)
            head = slug[: max(1, MAX_IDEA_SLUG_LEN - len(tag))]
            candidate = f"{head}{tag}"
            suffix += 1
        return candidate


def row_to_idea(row: sqlite3.Row | dict) -> Idea:
    return Idea(
        id=int(row["id"]),
        title=str(row["title"]),
        slug=str(row["slug"]),
        category=str(row["category"]),
        why=str(row["why"]),
        status=str(row["status"]),
        score=float(row["score"]),
        created_at=str(row["created_at"]),
        updated_at=str(row["updated_at"]),
    )


def initial_score(title: str, category: str, why: str) -> float:
    text = f"{title} {why}".lower()
    score = 50.0
    if category == "money":
        score += 25
    if any(word in text for word in ("revenue", "sell", "customer", "market", "business", "dollar", "saas")):
        score += 10
    if any(word in text for word in ("daily", "agent", "automation", "workflow", "poc")):
        score += 6
    if any(word in text for word in ("maybe", "someday", "unclear")):
        score -= 8
    return max(0.0, min(100.0, score))


# ---------------------------------------------------------------------------
# Postgres backend (used when DATABASE_URL is set in the environment)
# ---------------------------------------------------------------------------

_PG_SCHEMA = """
CREATE TABLE IF NOT EXISTS ideas (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  slug TEXT NOT NULL UNIQUE,
  category TEXT NOT NULL CHECK(category IN ('money', 'personal')),
  why TEXT NOT NULL DEFAULT '',
  status TEXT NOT NULL DEFAULT 'captured',
  score REAL NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS artifacts (
  id SERIAL PRIMARY KEY,
  idea_id INTEGER NOT NULL REFERENCES ideas(id) ON DELETE CASCADE,
  kind TEXT NOT NULL,
  content TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS decisions (
  id SERIAL PRIMARY KEY,
  idea_id INTEGER NOT NULL REFERENCES ideas(id) ON DELETE CASCADE,
  decision TEXT NOT NULL,
  rationale TEXT NOT NULL DEFAULT '',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS runs (
  id SERIAL PRIMARY KEY,
  idea_id INTEGER REFERENCES ideas(id) ON DELETE SET NULL,
  kind TEXT NOT NULL,
  summary TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
"""


class PgStore:
    """Postgres-backed store. Implements the same interface as Store."""

    def __init__(self, database_url: str) -> None:
        self._url = database_url

    def _connect(self):
        try:
            import psycopg2
        except ImportError as exc:
            raise RuntimeError(
                "psycopg2-binary is required for Postgres. "
                "Install with: pip install 'ideate[postgres]'"
            ) from exc
        return psycopg2.connect(self._url)

    def _dict_cursor(self, conn):
        import psycopg2.extras
        return conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def init(self) -> None:
        conn = self._connect()
        try:
            with conn:
                cur = conn.cursor()
                cur.execute(_PG_SCHEMA)
        finally:
            conn.close()

    def add_idea(self, title: str, category: str, why: str) -> Idea:
        if category not in CATEGORIES:
            raise ValueError(f"category must be one of: {', '.join(sorted(CATEGORIES))}")
        base_slug = ranchi_codename(title, max_len=MAX_IDEA_SLUG_LEN)
        score = initial_score(title, category, why)
        conn = self._connect()
        try:
            with conn:
                cur = self._dict_cursor(conn)
                slug = self._unique_slug(cur, base_slug)
                cur.execute(
                    "INSERT INTO ideas(title, slug, category, why, score) VALUES (%s, %s, %s, %s, %s)",
                    (title.strip(), slug, category, why.strip(), score),
                )
                cur.execute("SELECT * FROM ideas WHERE slug = %s", (slug,))
                row = cur.fetchone()
        finally:
            conn.close()
        return row_to_idea(row)

    def get_idea(self, idea_id: int) -> Idea:
        conn = self._connect()
        try:
            cur = self._dict_cursor(conn)
            cur.execute("SELECT * FROM ideas WHERE id = %s", (idea_id,))
            row = cur.fetchone()
        finally:
            conn.close()
        if row is None:
            raise KeyError(f"idea {idea_id} was not found")
        return row_to_idea(row)

    def list_ideas(self, status: str | None = None) -> list[Idea]:
        conn = self._connect()
        try:
            cur = self._dict_cursor(conn)
            if status:
                cur.execute(
                    "SELECT * FROM ideas WHERE status = %s ORDER BY score DESC, updated_at DESC",
                    (status,),
                )
            else:
                cur.execute(
                    """
                    SELECT * FROM ideas
                    ORDER BY
                      CASE category WHEN 'money' THEN 0 ELSE 1 END,
                      score DESC,
                      updated_at DESC
                    """
                )
            rows = cur.fetchall()
        finally:
            conn.close()
        return [row_to_idea(row) for row in rows]

    def set_status(self, idea_id: int, status: str) -> None:
        if status not in STATUSES:
            raise ValueError(f"unknown status: {status}")
        conn = self._connect()
        try:
            with conn:
                cur = conn.cursor()
                cur.execute(
                    "UPDATE ideas SET status = %s, updated_at = NOW() WHERE id = %s",
                    (status, idea_id),
                )
        finally:
            conn.close()

    def add_artifact(self, idea_id: int, kind: str, content: str) -> None:
        conn = self._connect()
        try:
            with conn:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO artifacts(idea_id, kind, content) VALUES (%s, %s, %s)",
                    (idea_id, kind, content),
                )
        finally:
            conn.close()

    def latest_artifact(self, idea_id: int, kind: str) -> str | None:
        conn = self._connect()
        try:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT content FROM artifacts
                WHERE idea_id = %s AND kind = %s
                ORDER BY created_at DESC, id DESC
                LIMIT 1
                """,
                (idea_id, kind),
            )
            row = cur.fetchone()
        finally:
            conn.close()
        return None if row is None else str(row[0])

    def add_decision(self, idea_id: int, decision: str, rationale: str = "") -> None:
        conn = self._connect()
        try:
            with conn:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO decisions(idea_id, decision, rationale) VALUES (%s, %s, %s)",
                    (idea_id, decision, rationale),
                )
        finally:
            conn.close()

    def log_run(self, kind: str, summary: str, idea_id: int | None = None) -> None:
        conn = self._connect()
        try:
            with conn:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO runs(idea_id, kind, summary) VALUES (%s, %s, %s)",
                    (idea_id, kind, summary),
                )
        finally:
            conn.close()

    def _unique_slug(self, cur, base_slug: str) -> str:
        slug = (base_slug or "ranchi")[:MAX_IDEA_SLUG_LEN]
        candidate = slug
        suffix = 1
        cur.execute("SELECT 1 FROM ideas WHERE slug = %s", (candidate,))
        while cur.fetchone():
            tag = _alpha_suffix(suffix)
            head = slug[: max(1, MAX_IDEA_SLUG_LEN - len(tag))]
            candidate = f"{head}{tag}"
            suffix += 1
            cur.execute("SELECT 1 FROM ideas WHERE slug = %s", (candidate,))
        return candidate
