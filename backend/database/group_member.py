from typing import List, Dict, Any
from .connection import execute_query, execute_update, execute_insert

class GroupMember:
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
    
    @staticmethod
    def get_group_members(group_id: int) -> List[Dict[str, Any]]:
        query = """
            SELECT s.id, s.name, s.fax_n, s.pager_n, s.avatar_url
            FROM group_member gm
            JOIN Student s ON gm.student_id = s.id
            WHERE gm.group_id = ?
            ORDER BY s.name
        """
        results = execute_query(query, (group_id,))
        return [dict(row) for row in results]
    
    @staticmethod
    def get_student_groups(student_id: int) -> List[Dict[str, Any]]:
        query = """
            SELECT gm.group_id, g.unit_code, g.num, g.id as group_number
            FROM group_member gm
            JOIN groups g ON gm.group_id = g.id
            WHERE gm.student_id = ?
            ORDER BY g.unit_code, g.num
        """
        results = execute_query(query, (student_id,))
        return [dict(row) for row in results]
    
    @staticmethod
    def is_member(group_id: int, student_id: int) -> bool:
        query = "SELECT 1 FROM group_member WHERE group_id = ? AND student_id = ? LIMIT 1"
        results = execute_query(query, (group_id, student_id))
        return len(results) > 0
    
    @staticmethod
    def get_group_size(group_id: int) -> int:
        query = "SELECT COUNT(*) FROM group_member WHERE group_id = ?"
        results = execute_query(query, (group_id,))
        return results[0][0] if results else 0
    
    @staticmethod
    def remove_all_members(group_id: int) -> int:
        query = "DELETE FROM group_member WHERE group_id = ?"
        return execute_update(query, (group_id,))
    
    @staticmethod
    def get_all_memberships() -> List[Dict[str, Any]]:
        query = """
            SELECT gm.group_id, gm.student_id, s.name as student_name, 
                   g.unit_code, g.num as assessment_num, g.id as group_number
            FROM group_member gm
            JOIN Student s ON gm.student_id = s.id
            JOIN groups g ON gm.group_id = g.id
            ORDER BY g.unit_code, g.num, g.id, s.name
        """
        results = execute_query(query, ())
        return [dict(row) for row in results]
    
    @staticmethod
    def get_students_without_group(unit_code: str, num: int) -> List[Dict[str, Any]]:
        query = """
            SELECT DISTINCT s.id, s.name, s.fax_n, s.pager_n, s.avatar_url
            FROM Student s
            JOIN unit_enrolment ue ON s.id = ue.student_id
            WHERE ue.unit_code = ?
            AND s.id NOT IN (
                SELECT DISTINCT gm.student_id
                FROM group_member gm
                JOIN groups g ON gm.group_id = g.id
                WHERE g.unit_code = ? AND g.num = ?
            )
            ORDER BY s.name
        """
        results = execute_query(query, (unit_code, unit_code, num))
        return [dict(row) for row in results]