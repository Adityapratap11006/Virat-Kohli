"""Versioned migration runner. Applies db/migrations/V*__*.sql in order,
recording each version in schema_version. One transaction per file.

Usage: python -m db.migrate   (run from repo root)
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from db import config

MIGRATIONS = Path(__file__).resolve().parent / "migrations"


def ensure_database() -> None:
    conn = config.connect(database=None)
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS `{config.NAME}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci")
    conn.commit()
    cur.close()
    conn.close()


def applied_versions(conn) -> set:
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS schema_version ("
                "version INT NOT NULL PRIMARY KEY, "
                "applied_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP) "
                "ENGINE=InnoDB DEFAULT CHARSET=utf8mb4")
    conn.commit()
    cur.execute("SELECT version FROM schema_version")
    out = {r[0] for r in cur.fetchall()}
    cur.close()
    return out


def pending() -> list:
    files = sorted(MIGRATIONS.glob("V*__*.sql"))
    out = []
    for f in files:
        m = re.match(r"V(\d+)__", f.name)
        if not m:
            raise RuntimeError(f"bad migration name: {f.name}")
        out.append((int(m.group(1)), f))
    return out


def _split_statements(sql: str) -> list:
    """Split on semicolons outside single-quoted strings (' doubled)."""
    stmts, buf, in_str = [], [], False
    i = 0
    while i < len(sql):
        ch = sql[i]
        if ch == "'":
            if in_str and i + 1 < len(sql) and sql[i + 1] == "'":
                buf.append("''")
                i += 2
                continue
            in_str = not in_str
            buf.append(ch)
        elif ch == ";" and not in_str:
            stmt = "".join(buf).strip()
            if stmt:
                stmts.append(stmt)
            buf = []
        else:
            buf.append(ch)
        i += 1
    tail = "".join(buf).strip()
    if tail:
        stmts.append(tail)
    return stmts


def migrate() -> list:
    ensure_database()
    conn = config.connect()
    done = applied_versions(conn)
    applied = []
    for version, path in pending():
        if version in done:
            continue
        lines = [ln for ln in path.read_text(encoding="utf-8").splitlines()
                 if ln.strip() and not ln.strip().startswith("--")]
        cur = conn.cursor()
        try:
            for stmt in _split_statements("\n".join(lines)):
                cur.execute(stmt)
            cur.execute("INSERT INTO schema_version (version) VALUES (%s)", (version,))
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close()
        applied.append(version)
        print(f"applied V{version} ({path.name})")
    conn.close()
    if not applied:
        print("schema up to date")
    return applied


if __name__ == "__main__":
    migrate()
