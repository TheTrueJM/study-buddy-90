from typing import List, Dict, Any
from .connection import execute_query, execute_update, execute_insert

class Student:
    @staticmethod
    def create(name: str, fax_n: str, pager_n: str, avatar_url: str) -> int:
        query = """
            INSERT INTO Student (name, fax_n, pager_n, avatar_url)
            VALUES (?, ?, ?, ?)
        """
        return execute_insert(query, (name, fax_n, pager_n, avatar_url))
    
    @staticmethod
    def get_by_id(student_id: int) -> Dict[str, Any] | None:
        query = "SELECT * FROM Student WHERE id = ?"
        results = execute_query(query, (student_id,))
        return dict(results[0]) if results else None
    
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        query = "SELECT * FROM Student ORDER BY name"
        results = execute_query(query, ())
        return [dict(row) for row in results]
    
    @staticmethod
    def update(student_id: int, name: str, fax_n: str, pager_n: str, avatar_url: str) -> bool:
        query = "UPDATE Student SET name = ?, fax_n = ?, pager_n = ?, avatar_url = ? WHERE id = ?"
        return execute_update(query, (name, fax_n, pager_n, avatar_url, student_id)) > 0
    
    @staticmethod
    def delete(student_id: int) -> bool:
        query = "DELETE FROM Student WHERE id = ?"
        return execute_update(query, (student_id,)) > 0
    
    @staticmethod
    def search_by_name(name_pattern: str) -> List[Dict[str, Any]]:
        query = "SELECT * FROM Student WHERE name LIKE ? ORDER BY name"
        results = execute_query(query, (f"%{name_pattern}%",))
        return [dict(row) for row in results]