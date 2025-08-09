import bcrypt
from typing import List, Dict, Any
from .connection import execute_query, execute_update, execute_insert

class Student:
    @staticmethod
    def create(name: str, password: str, fax_n: str, pager_n: str, avatar_url: str) -> int:
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        query = """
            INSERT INTO Student (name, password, fax_n, pager_n, avatar_url)
            VALUES (?, ?, ?, ?, ?)
        """
        return execute_insert(query, (name, hashed_pw, fax_n, pager_n, avatar_url))

    @staticmethod
    def get_by_id(student_id: int) -> Dict[str, Any] | None:
        query = "SELECT * FROM Student WHERE student_id = ?"
        results = execute_query(query, (student_id,))
        return dict(results[0]) if results else None

    @staticmethod
    def get_password(student_id: int) -> bytes | None:
        query = "SELECT password FROM Student WHERE student_id = ?"
        results = execute_query(query, (student_id,))
        return results[0][0] if results else None

    @staticmethod
    def verify_password(student_id: int, plain_password: str) -> bool:
        query = "SELECT password FROM Student WHERE student_id = ?"
        results = execute_query(query, (student_id,))
        if not results:
            return False
        stored_hash = results[0][0]  # bytes
        return bcrypt.checkpw(plain_password.encode(), stored_hash)

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        query = "SELECT * FROM Student ORDER BY name"
        results = execute_query(query, ())
        return [dict(row) for row in results]

    @staticmethod
    def update(student_id: int, name: str, password: str, fax_n: str, pager_n: str, avatar_url: str) -> bool:
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        query = "UPDATE Student SET name = ?, password = ?, fax_n = ?, pager_n = ?, avatar_url = ? WHERE student_id = ?"
        return execute_update(query, (name, hashedpw, fax_n, pager_n, avatar_url, student_id)) > 0

    @staticmethod
    def delete(student_id: int) -> bool:
        query = "DELETE FROM Student WHERE student_id = ?"
        return execute_update(query, (student_id,)) > 0

    @staticmethod
    def search_by_name(name_pattern: str) -> List[Dict[str, Any]]:
        query = "SELECT * FROM Student WHERE name LIKE ? ORDER BY name"
        results = execute_query(query, (f"%{name_pattern}%",))
        return [dict(row) for row in results]
    
    @staticmethod
    def create_with_id(student_id: int, name: str, password: str, fax_n: str, pager_n: str, avatar_url: str) -> int:
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        query = """
            INSERT INTO Student (student_id, name, password, fax_n, pager_n, avatar_url)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        return execute_insert(query, (student_id, name, hashed, fax_n, pager_n, avatar_url))

    @staticmethod
    def exists_by_id(student_id: int) -> bool:
        q = "SELECT 1 FROM Student WHERE student_id = ? LIMIT 1"
        return len(execute_query(q, (student_id,))) > 0

    @staticmethod
    def get_by_pager(pager_n: str):
        rows = execute_query("SELECT * FROM Student WHERE pager_n = ? LIMIT 1", (pager_n,))
        return dict(rows[0]) if rows else None
    
