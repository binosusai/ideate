#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ideate.db import PgStore  # noqa: E402


TABLES = ("ideas", "artifacts", "decisions", "runs")
BOOLEAN_COLUMNS = {
    "ideas": {"tinkered", "hardened"},
}
JSON_COLUMNS = {
    "ideas": {"details_json"},
}


def sqlite_rows(sqlite_path: Path, table: str) -> list[dict]:
    with sqlite3.connect(sqlite_path) as conn:
        conn.row_factory = sqlite3.Row
        return [dict(row) for row in conn.execute(f"SELECT * FROM {table} ORDER BY id")]


def table_columns(db, table: str) -> list[str]:
    db.execute(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name = %s
        ORDER BY ordinal_position
        """,
        (table,),
    )
    return [row[0] for row in db.fetchall()]


def remote_tables_exist(conn) -> bool:
    with conn.cursor() as db:
        result = db.execute(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
              AND table_name = ANY(%s)
            """,
            (list(TABLES),),
        )
        found = {row[0] for row in db.fetchall()}
    return set(TABLES).issubset(found)


def print_remote_privileges(conn) -> None:
    with conn.cursor() as db:
        db.execute(
            """
            SELECT
              current_user,
              session_user,
              current_database(),
              current_schema(),
              n.nspname,
              pg_get_userbyid(n.nspowner),
              has_schema_privilege(current_user, 'public', 'USAGE'),
              has_schema_privilege(current_user, 'public', 'CREATE')
            FROM pg_namespace n
            WHERE n.nspname = 'public'
            """
        )
        row = db.fetchone()
    if not row:
        print("Remote privilege check: public schema was not found.")
        return
    (
        current_user,
        session_user,
        database,
        current_schema,
        schema_name,
        schema_owner,
        has_usage,
        has_create,
    ) = row
    print("Remote privilege check:")
    print(f"  current_user:   {current_user}")
    print(f"  session_user:   {session_user}")
    print(f"  database:       {database}")
    print(f"  current_schema: {current_schema}")
    print(f"  schema:         {schema_name}")
    print(f"  schema_owner:   {schema_owner}")
    print(f"  has_usage:      {has_usage}")
    print(f"  has_create:     {has_create}")


def ensure_schema_or_existing_tables(store: PgStore) -> None:
    try:
        store.init()
        return
    except Exception as exc:  # noqa: BLE001
        cause = getattr(exc, "__cause__", None)
        pgcode = getattr(exc, "pgcode", "") or getattr(cause, "pgcode", "")
        message = f"{exc} {cause or ''}".lower()
        if pgcode != "42501" and "permission denied for schema public" not in message:
            raise

    conn = store._connect()
    try:
        print_remote_privileges(conn)
        if remote_tables_exist(conn):
            print("Remote tables already exist; continuing without schema initialization.")
            return
    finally:
        conn.close()

    raise SystemExit(
        "DATABASE_URL user cannot create tables in schema public, and required Ideate "
        "tables are missing. Run `idea init` once with the Neon owner/admin connection "
        "string, then rerun this restore with the app connection string."
    )


def pg_value(table: str, column: str, value):
    if column in BOOLEAN_COLUMNS.get(table, set()):
        return bool(value)
    if column in JSON_COLUMNS.get(table, set()):
        if value in (None, ""):
            return "{}"
        if isinstance(value, (dict, list)):
            return json.dumps(value, sort_keys=True, separators=(",", ":"))
        return str(value)
    return value


def upsert_rows(db, table: str, rows: list[dict]) -> int:
    if not rows:
        return 0

    pg_columns = set(table_columns(db, table))
    columns = [column for column in rows[0].keys() if column in pg_columns]
    placeholders = ", ".join(["%s"] * len(columns))
    column_sql = ", ".join(columns)
    updates = ", ".join(
        f"{column} = EXCLUDED.{column}" for column in columns if column != "id"
    )

    sql = f"""
        INSERT INTO {table} ({column_sql})
        VALUES ({placeholders})
        ON CONFLICT (id) DO UPDATE SET {updates}
    """
    values = [
        tuple(pg_value(table, column, row.get(column)) for column in columns)
        for row in rows
    ]
    db.executemany(sql, values)
    return len(values)


def reset_sequence(db, table: str) -> None:
    db.execute(
        """
        SELECT setval(
            pg_get_serial_sequence(%s, 'id'),
            COALESCE((SELECT MAX(id) FROM public.%s), 1),
            (SELECT COUNT(*) > 0 FROM public.%s)
        )
        """
        % ("%s", table, table),
        (table,),
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Restore Ideate Neon/Postgres rows from local SQLite state."
    )
    parser.add_argument(
        "--sqlite",
        default=str(ROOT / ".ideate" / "ideate.sqlite3"),
        help="Path to source SQLite DB.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show row counts without writing to Postgres.",
    )
    args = parser.parse_args()

    sqlite_path = Path(args.sqlite).resolve()
    if not sqlite_path.exists():
        raise SystemExit(f"SQLite source was not found: {sqlite_path}")

    rows_by_table = {table: sqlite_rows(sqlite_path, table) for table in TABLES}
    for table, rows in rows_by_table.items():
        print(f"{table}: {len(rows)} source rows")

    if args.dry_run:
        print("Dry run only; no remote rows changed.")
        return 0

    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise SystemExit("DATABASE_URL must be exported before restoring to Neon.")

    store = PgStore(database_url)
    ensure_schema_or_existing_tables(store)
    conn = store._connect()
    try:
        with conn:
            with conn.cursor() as db:
                for table in TABLES:
                    restored = upsert_rows(db, table, rows_by_table[table])
                    reset_sequence(db, table)
                    print(f"{table}: restored {restored} rows")
    finally:
        conn.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
