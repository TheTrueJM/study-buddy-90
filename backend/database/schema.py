import sqlite3
from .connection import get_db_connection

def create_tables():
    with get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS Student (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                password BLOB NOT NULL,
                fax_n TEXT,
                pager_n TEXT,
                avatar_url TEXT
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS Units (
                code TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS Assessments (
                unit_code TEXT NOT NULL,
                num INTEGER NOT NULL,
                size INTEGER,
                due_week INTEGER,
                grade REAL,
                group_formation_week INTEGER,
                PRIMARY KEY (unit_code, num),
                FOREIGN KEY (unit_code) REFERENCES Units (code)
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS groups (
                unit_code TEXT NOT NULL,
                num INTEGER NOT NULL,
                id INTEGER NOT NULL,
                PRIMARY KEY (unit_code, num, id),
                FOREIGN KEY (unit_code, num) REFERENCES Assessments (unit_code, num)
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS group_member (
                group_id INTEGER NOT NULL,
                student_id INTEGER NOT NULL,
                PRIMARY KEY (group_id, student_id),
                FOREIGN KEY (student_id) REFERENCES Student (id)
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS unit_enrolment (
                unit_code TEXT NOT NULL,
                student_id INTEGER NOT NULL,
                grade REAL,
                completed BOOLEAN DEFAULT FALSE,
                availability TEXT,
                PRIMARY KEY (unit_code, student_id),
                FOREIGN KEY (unit_code) REFERENCES Units (code),
                FOREIGN KEY (student_id) REFERENCES Student (id)
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS group_requests (
                group_id INTEGER NOT NULL,
                student_id INTEGER NOT NULL,
                PRIMARY KEY (group_id, student_id),
                FOREIGN KEY (student_id) REFERENCES Student (id)
            )
        """)

def init_database():
    create_tables()
    print("Database initialized successfully.")
