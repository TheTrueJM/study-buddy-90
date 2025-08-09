import sqlite3
import os
from contextlib import contextmanager
from typing import Generator

DB_PATH = os.path.join(os.path.dirname(__file__), 'study_mates.db')

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@contextmanager
def get_db_connection() -> Generator[sqlite3.Connection, None, None]:
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def execute_query(query: str, params: tuple) -> list:
    with get_db_connection() as conn:
        cursor = conn.execute(query, params)
        return cursor.fetchall()

def execute_update(query: str, params: tuple) -> int:
    with get_db_connection() as conn:
        cursor = conn.execute(query, params)
        return cursor.rowcount

def execute_insert(query: str, params: tuple) -> int:
    with get_db_connection() as conn:
        cursor = conn.execute(query, params)
        return cursor.lastrowid or 0