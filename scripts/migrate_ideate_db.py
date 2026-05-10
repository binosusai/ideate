import os

import psycopg2
from psycopg2.extras import execute_values
from psycopg2 import errors


_PG_SCHEMA = """
CREATE TABLE IF NOT EXISTS ideas (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    slug TEXT NOT NULL UNIQUE,
    category TEXT NOT NULL CHECK(category IN ('money', 'personal')),
    why TEXT NOT NULL DEFAULT '',
    details_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    status TEXT NOT NULL DEFAULT 'captured',
    score REAL NOT NULL DEFAULT 0,
    hardened BOOLEAN NOT NULL DEFAULT FALSE,
    tinkered BOOLEAN NOT NULL DEFAULT FALSE,
    review_status TEXT NOT NULL DEFAULT 'new',
    review_feedback TEXT NOT NULL DEFAULT '',
    last_reviewed_at TIMESTAMPTZ,
    iteration_count INTEGER NOT NULL DEFAULT 0,
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


def _ensure_target_schema(conn) -> None:
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(_PG_SCHEMA)
                cur.execute(
                    "ALTER TABLE ideas ADD COLUMN IF NOT EXISTS tinkered BOOLEAN NOT NULL DEFAULT FALSE"
                )
                cur.execute(
                    "ALTER TABLE ideas ADD COLUMN IF NOT EXISTS hardened BOOLEAN NOT NULL DEFAULT FALSE"
                )
                cur.execute(
                    "ALTER TABLE ideas ADD COLUMN IF NOT EXISTS review_status TEXT NOT NULL DEFAULT 'new'"
                )
                cur.execute(
                    "ALTER TABLE ideas ADD COLUMN IF NOT EXISTS review_feedback TEXT NOT NULL DEFAULT ''"
                )
                cur.execute(
                    "ALTER TABLE ideas ADD COLUMN IF NOT EXISTS last_reviewed_at TIMESTAMPTZ"
                )
                cur.execute(
                    "ALTER TABLE ideas ADD COLUMN IF NOT EXISTS iteration_count INTEGER NOT NULL DEFAULT 0"
                )
                cur.execute(
                    "ALTER TABLE ideas ADD COLUMN IF NOT EXISTS details_json JSONB NOT NULL DEFAULT '{}'::jsonb"
                )
    except errors.InsufficientPrivilege:
        conn.rollback()
        required = {"ideas", "artifacts", "decisions", "runs"}
        with conn.cursor() as cur:
            cur.execute(
                "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public'"
            )
            existing = {row[0] for row in cur.fetchall()}
        missing = sorted(required - existing)
        if missing:
            raise RuntimeError(
                "Target database user cannot create schema objects in public and required tables are missing: "
                + ", ".join(missing)
                + ". Use a DB owner/admin URL for DATABASE_URL once to run schema initialization, "
                "or grant CREATE on schema public to the target role."
            )
        print(
            "NOTE: target role cannot create/alter schema, but required tables already exist; continuing."
        )


def _count(conn, table: str) -> int:
    with conn.cursor() as cur:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        return int(cur.fetchone()[0])


def _columns(conn, table: str) -> set[str]:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = %s
            """,
            (table,),
        )
        return {str(row[0]) for row in cur.fetchall()}


def main() -> int:
    src_url = os.environ.get("OLD_DATABASE_URL", "").strip()
    dst_url = os.environ.get("DATABASE_URL", "").strip()
    if not src_url or not dst_url:
        print("ERROR: OLD_DATABASE_URL and DATABASE_URL must be set")
        return 2

    tables = [
        (
            "ideas",
            [
                "id",
                "title",
                "slug",
                "category",
                "why",
                "details_json",
                "status",
                "score",
                "hardened",
                "tinkered",
                "review_status",
                "review_feedback",
                "last_reviewed_at",
                "iteration_count",
                "created_at",
                "updated_at",
            ],
            "ON CONFLICT (id) DO UPDATE SET "
            "title=EXCLUDED.title, slug=EXCLUDED.slug, category=EXCLUDED.category, why=EXCLUDED.why, "
            "details_json=EXCLUDED.details_json, "
            "status=EXCLUDED.status, score=EXCLUDED.score, hardened=EXCLUDED.hardened, tinkered=EXCLUDED.tinkered, "
            "review_status=EXCLUDED.review_status, review_feedback=EXCLUDED.review_feedback, "
            "last_reviewed_at=EXCLUDED.last_reviewed_at, iteration_count=EXCLUDED.iteration_count, "
            "created_at=EXCLUDED.created_at, updated_at=EXCLUDED.updated_at",
        ),
        (
            "artifacts",
            ["id", "idea_id", "kind", "content", "created_at"],
            "ON CONFLICT (id) DO UPDATE SET "
            "idea_id=EXCLUDED.idea_id, kind=EXCLUDED.kind, content=EXCLUDED.content, created_at=EXCLUDED.created_at",
        ),
        (
            "decisions",
            ["id", "idea_id", "decision", "rationale", "created_at"],
            "ON CONFLICT (id) DO UPDATE SET "
            "idea_id=EXCLUDED.idea_id, decision=EXCLUDED.decision, rationale=EXCLUDED.rationale, created_at=EXCLUDED.created_at",
        ),
        (
            "runs",
            ["id", "idea_id", "kind", "summary", "created_at"],
            "ON CONFLICT (id) DO UPDATE SET "
            "idea_id=EXCLUDED.idea_id, kind=EXCLUDED.kind, summary=EXCLUDED.summary, created_at=EXCLUDED.created_at",
        ),
    ]

    src = psycopg2.connect(src_url)
    dst = psycopg2.connect(dst_url)

    _ensure_target_schema(dst)

    print("SOURCE_COUNTS_BEFORE")
    for t, *_ in tables:
        print(f"{t}={_count(src, t)}")

    print("TARGET_COUNTS_BEFORE")
    for t, *_ in tables:
        print(f"{t}={_count(dst, t)}")

    with src, dst:
        with src.cursor() as sc, dst.cursor() as dc:
            for table, cols, conflict in tables:
                existing_cols = _columns(src, table)
                select_cols = [
                    "'{}'::jsonb AS details_json"
                    if table == "ideas" and col == "details_json" and col not in existing_cols
                    else col
                    for col in cols
                ]
                sc.execute(f"SELECT {', '.join(select_cols)} FROM {table} ORDER BY id")
                rows = sc.fetchall()
                if rows:
                    insert_sql = f"INSERT INTO {table} ({', '.join(cols)}) VALUES %s {conflict}"
                    execute_values(dc, insert_sql, rows, page_size=500)
                print(f"MIGRATED_{table}={len(rows)}")

            for table in ("ideas", "artifacts", "decisions", "runs"):
                dc.execute(
                    f"SELECT setval(pg_get_serial_sequence('{table}','id'), COALESCE(MAX(id),1), MAX(id) IS NOT NULL) FROM {table}"
                )

    print("TARGET_COUNTS_AFTER")
    for t, *_ in tables:
        print(f"{t}={_count(dst, t)}")

    src.close()
    dst.close()
    print("MIGRATION_DONE=1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
