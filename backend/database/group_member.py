from typing import List, Dict, Any
from .connection import execute_query, execute_update, execute_insert

class GroupMembers:
    @staticmethod
    def add_member(group_id: int, student_id: int) -> bool:
        query = """
            INSERT INTO group_member (group_id, student_id)
            VALUES (?, ?)
        """
        try:
            execute_insert(query, (group_id, student_id))
            return True
        except:
            return False
    
    @staticmethod
    def remove_member(group_id: int, student_id: int) -> bool:
        query = "DELETE FROM group_member WHERE group_id = ? AND student_id = ?"
        return execute_update(query, (group_id, student_id)) > 0