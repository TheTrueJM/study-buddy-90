from typing import List, Dict, Any
from .connection import execute_query, execute_update, execute_insert

class Units:
    @staticmethod
    def create(code: str, name: str, description: str) -> bool:
        query = """
            INSERT INTO Units (code, name, description)
            VALUES (?, ?, ?)
        """
        try:
            execute_insert(query, (code, name, description))
            return True
        except:
            return False
    
    @staticmethod
    def get_by_code(code: str) -> Dict[str, Any] | None:
        query = "SELECT * FROM Units WHERE code = ?"
        results = execute_query(query, (code,))
        return dict(results[0]) if results else None
    
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        query = "SELECT * FROM Units ORDER BY code"
        results = execute_query(query, ())
        return [dict(row) for row in results]
    
    @staticmethod
    def update(code: str, name: str, description: str) -> bool:
        query = "UPDATE Units SET name = ?, description = ? WHERE code = ?"
        return execute_update(query, (name, description, code)) > 0
    
    @staticmethod
    def delete(code: str) -> bool:
        query = "DELETE FROM Units WHERE code = ?"
        return execute_update(query, (code,)) > 0
    
    @staticmethod
    def search_by_name(name_pattern: str) -> List[Dict[str, Any]]:
        query = "SELECT * FROM Units WHERE name LIKE ? ORDER BY name"
        results = execute_query(query, (f"%{name_pattern}%",))
        return [dict(row) for row in results]