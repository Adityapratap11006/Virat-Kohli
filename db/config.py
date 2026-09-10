"""Database connection settings. Env-driven; dev defaults target the
project-local MySQL 8 container (host port 3307). No secrets in code."""
import os

HOST = os.getenv("KOHLIIQ_DB_HOST", "127.0.0.1")
PORT = int(os.getenv("KOHLIIQ_DB_PORT", "3307"))
USER = os.getenv("KOHLIIQ_DB_USER", "root")
PASSWORD = os.getenv("KOHLIIQ_DB_PASSWORD", "kohliiq-dev")
NAME = os.getenv("KOHLIIQ_DB_NAME", "kohliiq")

STRICT_MODE = ("STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,"
               "ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION")

BATCH_SIZE = 2000


def connect(database: str | None = None):
    import mysql.connector
    conn = mysql.connector.connect(
        host=HOST, port=PORT, user=USER, password=PASSWORD,
        database=database or NAME, charset="utf8mb4",
        autocommit=False,
    )
    cur = conn.cursor()
    cur.execute(f"SET SESSION sql_mode = '{STRICT_MODE}'")
    cur.close()
    return conn
