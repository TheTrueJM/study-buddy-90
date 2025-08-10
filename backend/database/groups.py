from typing import List, Dict, Any
from .connection import execute_query, execute_update, execute_insert

class Groups:
    @staticmethod
    def create(unit_code: str, num: int, name: str) -> int:
        query = """
            INSERT INTO Groups (unit_code, num, name)
            VALUES (?, ?, ?)
        """
        try:
            return execute_insert(query, (unit_code, num, name))
        except:
            return -1
    

    @staticmethod
    def get_by_id(id: int) -> Dict[str, Any] | None:
        query = "SELECT * FROM Groups WHERE id = ?"
        results = execute_query(query, (id,))
        return dict(results[0]) if results else None
    
    @staticmethod
    def get_by_assessment(unit_code: str, num: int) -> List[Dict[str, Any]]:
        query = "SELECT * FROM Groups WHERE unit_code = ? AND num = ? ORDER BY id"
        results = execute_query(query, (unit_code, num))
        return [dict(row) for row in results]
    
    @staticmethod
    def get_by_unit(unit_code: str) -> List[Dict[str, Any]]:
        query = "SELECT * FROM Groups WHERE unit_code = ? ORDER BY num, id"
        results = execute_query(query, (unit_code,))
        return [dict(row) for row in results]
    
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        query = "SELECT * FROM Groups ORDER BY unit_code, num, id"
        results = execute_query(query, ())
        return [dict(row) for row in results]
    

    @staticmethod
    def update(id: int, name: str) -> bool:
        query = "UPDATE Groups SET name = ? WHERE id = ?"
        return execute_update(query, (name, id)) > 0

    @staticmethod
    def delete(id: int) -> bool:
        query = "DELETE FROM Groups WHERE id = ?"
        return execute_update(query, (id,)) > 0
    
    @staticmethod
    def delete_by_assessment(unit_code: str, num: int) -> int:
        query = "DELETE FROM Groups WHERE unit_code = ? AND num = ?"
        return execute_update(query, (unit_code, num))
    

    @staticmethod
    def get_members(id: int) -> List[Dict[str, Any]]:
        query = """
            SELECT s.id, s.name
            FROM Students s
            JOIN GroupMembers gm ON s.id = gm.student_id
            WHERE gm.group_id = ?
            ORDER BY s.name
        """
        results = execute_query(query, (id,))
        return [dict(row) for row in results]
    
    @staticmethod
    def remove_all_members(id: int) -> int:
        query = "DELETE FROM GroupMembers WHERE group_id = ?"
        return execute_update(query, (id,))
    
    @staticmethod
    def get_requests(id: int) -> List[Dict[str, Any]]:
        query = """
            SELECT s.id, s.name
            FROM Students s
            JOIN GroupRequests gr ON s.id = gr.student_id
            WHERE gr.group_id = ?
            ORDER BY s.name
        """
        results = execute_query(query, (id,))
        return [dict(row) for row in results]
    
    @staticmethod
    def remove_all_requests(id: int) -> int:
        query = "DELETE FROM GroupRequests WHERE group_id = ?"
        return execute_update(query, (id,))


    @staticmethod
    def is_member(id: int, student_id: int) -> bool:
        query = "SELECT 1 FROM GroupMembers WHERE group_id = ? AND student_id = ? LIMIT 1"
        results = execute_query(query, (id, student_id))
        return len(results) > 0
    
    @staticmethod
    def get_current_size(id: int) -> int:
        query = "SELECT COUNT(*) FROM GroupMembers WHERE group_id = ?"
        results = execute_query(query, (id,))
        return results[0][0] if results else 0


    @staticmethod
    def student_already_in_group(unit_code: int, num: int, student_id: int) -> bool:
        query = """
            SELECT 1
            FROM Groups g
            JOIN GroupMembers gm ON g.id = gm.id
            WHERE g.unit_code = ? AND g.num = ? AND gm.student_id = ?
            LIMIT 1
        """
        results = execute_query(query, (unit_code, num, student_id))
        return len(results) > 0
