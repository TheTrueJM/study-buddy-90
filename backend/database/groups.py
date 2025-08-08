from typing import List, Dict, Any
from .connection import execute_query, execute_update, execute_insert

class Groups:
    @staticmethod
    def create(unit_code: str, num: int, id: int) -> bool:
        query = """
            INSERT INTO groups (unit_code, num, id)
            VALUES (?, ?, ?)
        """
        try:
            execute_insert(query, (unit_code, num, id))
            return True
        except:
            return False
    
    @staticmethod
    def get_by_key(unit_code: str, num: int, id: int) -> Dict[str, Any] | None:
        query = "SELECT * FROM groups WHERE unit_code = ? AND num = ? AND id = ?"
        results = execute_query(query, (unit_code, num, id))
        return dict(results[0]) if results else None
    
    @staticmethod
    def get_by_assessment(unit_code: str, num: int) -> List[Dict[str, Any]]:
        query = "SELECT * FROM groups WHERE unit_code = ? AND num = ? ORDER BY id"
        results = execute_query(query, (unit_code, num))
        return [dict(row) for row in results]
    
    @staticmethod
    def get_by_unit(unit_code: str) -> List[Dict[str, Any]]:
        query = "SELECT * FROM groups WHERE unit_code = ? ORDER BY num, id"
        results = execute_query(query, (unit_code,))
        return [dict(row) for row in results]
    
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        query = "SELECT * FROM groups ORDER BY unit_code, num, id"
        results = execute_query(query, ())
        return [dict(row) for row in results]
    
    @staticmethod
    def delete(unit_code: str, num: int, id: int) -> bool:
        query = "DELETE FROM groups WHERE unit_code = ? AND num = ? AND id = ?"
        return execute_update(query, (unit_code, num, id)) > 0
    
    @staticmethod
    def delete_by_assessment(unit_code: str, num: int) -> int:
        query = "DELETE FROM groups WHERE unit_code = ? AND num = ?"
        return execute_update(query, (unit_code, num))
    
    @staticmethod
    def get_next_group_id(unit_code: str, num: int) -> int:
        query = "SELECT MAX(id) FROM groups WHERE unit_code = ? AND num = ?"
        results = execute_query(query, (unit_code, num))
        max_id = results[0][0] if results and results[0][0] is not None else 0
        return max_id + 1
    
    @staticmethod
    def exists(unit_code: str, num: int, id: int) -> bool:
        query = "SELECT 1 FROM groups WHERE unit_code = ? AND num = ? AND id = ? LIMIT 1"
        results = execute_query(query, (unit_code, num, id))
        return len(results) > 0