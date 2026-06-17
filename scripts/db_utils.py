"""
LinguaGraph Database Utilities
================================
Shared database tools for all LinguaGraph agents.

Provides:
    - get_connection()       — Standardized DB connection
    - query()                — Execute SELECT and return list of dicts
    - query_one()            — Execute SELECT and return single dict or None
    - insert()               — Insert single row, return last_id
    - insert_many()          — Bulk insert rows
    - upsert()               — Insert or update on conflict
    - export_to_json()       — Export any table to JSON file
    - export_all_to_json()   — Export all tables
    - get_summary()          — High-level project data summary

Usage:
    from db_utils import get_connection, query, insert

    conn = get_connection()
    students = query(conn, "SELECT * FROM students")
    insert(conn, "responses", {
        "response_id": "R002_zh_q1",
        "student_id": "S002",
        ...
    })
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# === Database Path ===
DB_DIR = Path(__file__).parent.parent  # project root (scripts/../)
DB_PATH = DB_DIR / "linguaGraph.db"


def get_connection() -> sqlite3.Connection:
    """Get a standardized database connection."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


# ===== Query Helpers =====

def query(conn: sqlite3.Connection, sql: str, params: tuple = ()) -> List[Dict[str, Any]]:
    """Execute SELECT and return list of dicts."""
    cursor = conn.execute(sql, params)
    return [dict(row) for row in cursor.fetchall()]


def query_one(conn: sqlite3.Connection, sql: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
    """Execute SELECT and return single dict or None."""
    cursor = conn.execute(sql, params)
    row = cursor.fetchone()
    return dict(row) if row else None


def query_value(conn: sqlite3.Connection, sql: str, params: tuple = ()) -> Any:
    """Execute SELECT and return single value or None."""
    cursor = conn.execute(sql, params)
    row = cursor.fetchone()
    return row[0] if row else None


# ===== Insert Helpers =====

def insert(conn: sqlite3.Connection, table: str, data: Dict[str, Any]) -> str:
    """
    Insert a single row.

    Args:
        conn: Database connection
        table: Table name (e.g., "students", "responses")
        data: Dict of {column: value}

    Returns:
        The inserted row's primary key (first column value)
    """
    columns = list(data.keys())
    placeholders = ", ".join(["?" for _ in columns])
    col_names = ", ".join(columns)
    values = [data[c] for c in columns]

    sql = f"INSERT INTO {table} ({col_names}) VALUES ({placeholders})"
    conn.execute(sql, values)
    conn.commit()
    return str(data.get(columns[0], ""))


def insert_many(conn: sqlite3.Connection, table: str, rows: List[Dict[str, Any]]) -> int:
    """
    Bulk insert multiple rows.

    Args:
        conn: Database connection
        table: Table name
        rows: List of dicts (must all have same keys)

    Returns:
        Number of rows inserted
    """
    if not rows:
        return 0

    columns = list(rows[0].keys())
    placeholders = ", ".join(["?" for _ in columns])
    col_names = ", ".join(columns)

    values_list = [[r[c] for c in columns] for r in rows]
    sql = f"INSERT INTO {table} ({col_names}) VALUES ({placeholders})"
    conn.executemany(sql, values_list)
    conn.commit()
    return len(rows)


def upsert(conn: sqlite3.Connection, table: str, data: Dict[str, Any], conflict_column: str) -> str:
    """
    Insert or update on conflict.

    Args:
        conn: Database connection
        table: Table name
        data: Dict of {column: value}
        conflict_column: Column name for conflict detection (usually the PK)

    Returns:
        The row's primary key
    """
    columns = list(data.keys())
    placeholders = ", ".join(["?" for _ in columns])
    col_names = ", ".join(columns)

    # Build update part: col1=excluded.col1, col2=excluded.col2, ...
    update_set = ", ".join([f"{c}=excluded.{c}" for c in columns])

    sql = f"""
        INSERT INTO {table} ({col_names}) VALUES ({placeholders})
        ON CONFLICT({conflict_column}) DO UPDATE SET {update_set}
    """
    values = [data[c] for c in columns]
    conn.execute(sql, values)
    conn.commit()
    return str(data.get(columns[0], ""))


# ===== Export Helpers =====

def export_to_json(conn: sqlite3.Connection, table: str, output_dir: Optional[Path] = None) -> Path:
    """Export a table to a JSON file."""
    if output_dir is None:
        output_dir = DB_DIR / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    rows = query(conn, f"SELECT * FROM {table} ORDER BY rowid")
    output_path = output_dir / f"{table}.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    print(f"  [EXPORT] {table}: {len(rows)} rows → {output_path.name}")
    return output_path


def export_all_to_json(conn: sqlite3.Connection, output_dir: Optional[Path] = None) -> Dict[str, Path]:
    """Export all tables to JSON files."""
    tables = [
        "students", "questionnaires", "responses",
        "extractions", "graphs", "gold_labels",
        "cross_language_analysis", "evaluation_results"
    ]
    results = {}
    for table in tables:
        results[table] = export_to_json(conn, table, output_dir)
    return results


# ===== Summary =====

def get_summary(conn: sqlite3.Connection) -> Dict[str, Any]:
    """Get a high-level project data summary."""
    return {
        "db_path": str(DB_PATH),
        "total_students": query_value(conn, "SELECT COUNT(*) FROM students"),
        "total_responses": query_value(conn, "SELECT COUNT(*) FROM responses"),
        "resp_by_language": {
            row["language"]: row["count"]
            for row in query(conn, "SELECT language, COUNT(*) as count FROM responses GROUP BY language")
        },
        "total_extractions": query_value(conn, "SELECT COUNT(*) FROM extractions"),
        "total_gold_labels": query_value(conn, "SELECT COUNT(*) FROM gold_labels"),
        "total_analyses": query_value(conn, "SELECT COUNT(*) FROM cross_language_analysis"),
        "languages_present": [
            row["language"]
            for row in query(conn, "SELECT DISTINCT language FROM responses ORDER BY language")
        ],
        "timestamp": datetime.now().isoformat()
    }


# ===== CLI =====

def main():
    import argparse
    parser = argparse.ArgumentParser(description="LinguaGraph Database Utilities")
    parser.add_argument("--export", metavar="TABLE", help="Export a specific table to JSON")
    parser.add_argument("--export-all", action="store_true", help="Export all tables to JSON")
    parser.add_argument("--summary", action="store_true", help="Print project summary")
    parser.add_argument("--query", metavar="SQL", help="Run a raw SQL query and show results")
    parser.add_argument("--limit", type=int, default=20, help="Max rows for --query output")

    args = parser.parse_args()

    conn = get_connection()

    if args.summary:
        summary = get_summary(conn)
        print(f"\n{'='*50}")
        print(f"  LinguaGraph Project Summary")
        print(f"{'='*50}")
        for key, value in summary.items():
            if key == "timestamp":
                continue
            print(f"  {key:<25s}: {value}")
        print(f"{'='*50}\n")

    elif args.export:
        path = export_to_json(conn, args.export)
        print(f"  [OK] Exported to {path}")

    elif args.export_all:
        export_all_to_json(conn)

    elif args.query:
        try:
            from db_init import print_stats
            sql_upper = args.query.strip().upper()
            if sql_upper.startswith("SELECT") or sql_upper.startswith("PRAGMA"):
                results = query(conn, args.query)
                if results:
                    # Pretty print
                    keys = results[0].keys()
                    print(f"\n  {len(results)} row(s) returned")
                    print(f"  {'─'*80}")
                    for r in results[:args.limit]:
                        for k in keys:
                            v = r.get(k, "")
                            v_str = str(v)[:60]
                            print(f"    {k:<25s}: {v_str}")
                        print(f"  {'─'*80}")
                    if len(results) > args.limit:
                        print(f"  ... and {len(results) - args.limit} more rows")
                else:
                    print("  (no results)")
            else:
                conn.execute(args.query)
                conn.commit()
                print(f"  [OK] Statement executed.")
        except Exception as e:
            print(f"  [ERROR] {e}")

    else:
        parser.print_help()

    conn.close()


if __name__ == "__main__":
    main()
