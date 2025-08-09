import sqlite3
from .connection import get_db_connection

def create_tables():
    with get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS Students (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                password BLOB NOT NULL,
                fax_num TEXT,
                pager_num TEXT,
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
                grade REAL NOT NULL,
                due_week INTEGER NOT NULL,
                group_size INTEGER NOT NULL,
                group_formation_week INTEGER NOT NULL,
                PRIMARY KEY (unit_code, num),
                FOREIGN KEY (unit_code) REFERENCES Units (code)
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS Enrolments (
                unit_code TEXT NOT NULL,
                student_id INTEGER NOT NULL,
                grade REAL,
                availability TEXT,
                complete BOOLEAN DEFAULT FALSE,
                PRIMARY KEY (unit_code, student_id),
                FOREIGN KEY (unit_code) REFERENCES Units (code),
                FOREIGN KEY (student_id) REFERENCES Students (id)
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS Groups (
                id INTEGER PRIMARY KEY,
                unit_code TEXT NOT NULL,
                num INTEGER NOT NULL,
                name STRING NOT NULL,
                FOREIGN KEY (unit_code, num) REFERENCES Assessments (unit_code, num)
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS GroupRequests (
                group_id INTEGER NOT NULL,
                student_id INTEGER NOT NULL,
                PRIMARY KEY (group_id, student_id),
                FOREIGN KEY (group_id) REFERENCES Groups (id),
                FOREIGN KEY (student_id) REFERENCES Students (id)
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS GroupMembers (
                group_id INTEGER NOT NULL,
                student_id INTEGER NOT NULL,
                PRIMARY KEY (group_id, student_id),
                FOREIGN KEY (group_id) REFERENCES Groups (id),
                FOREIGN KEY (student_id) REFERENCES Students (id)
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS Messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_id INTEGER NOT NULL,
                group_id INTEGER NOT NULL,
                body TEXT NOT NULL,
                created_at INTEGER NOT NULL, -- unix epoch seconds
                CHECK (length(body) <= 160),
                FOREIGN KEY (sender_id) REFERENCES Students (id),
                FOREIGN KEY (group_id) REFERENCES Groups (id)
            )
        """)



def init_database():
    create_tables()
    print("Database initialized successfully.")