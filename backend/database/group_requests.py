from typing import List, Dict, Any
from .connection import execute_query, execute_update, execute_insert

class GroupRequests:
    @staticmethod
    def get_by_key(group_id: int, student_id: int) -> Dict[str, Any] | None:
        query = "SELECT * FROM GroupRequests WHERE group_id = ? AND student_id = ?"
        results = execute_query(query, (group_id, student_id))
        return dict(results[0]) if results else None

    @staticmethod
    def create_request(group_id: int, student_id: int) -> bool:
        query = "INSERT INTO GroupRequests (group_id, student_id) VALUES (?, ?)"
        try:
            execute_insert(query, (group_id, student_id))
            return True
        except:
            return False
    
    @staticmethod
    def delete_request(group_id: int, student_id: int) -> bool:
        query = "DELETE FROM GroupRequests WHERE group_id = ? AND student_id = ?"
        return execute_update(query, (group_id, student_id)) > 0