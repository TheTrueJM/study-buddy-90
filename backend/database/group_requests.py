from typing import List, Dict, Any
from .connection import execute_query, execute_update, execute_insert

class GroupRequests:
    @staticmethod
    def create_request(group_id: int, student_id: int) -> bool:
        query = """
            INSERT INTO group_requests (group_id, student_id)
            VALUES (?, ?)
        """
        try:
            execute_insert(query, (group_id, student_id))
            return True
        except:
            return False
    
    @staticmethod
    def get_request(group_id: int, student_id: int) -> Dict[str, Any] | None:
        query = "SELECT * FROM group_requests WHERE group_id = ? AND student_id = ?"
        results = execute_query(query, (group_id, student_id))
        return dict(results[0]) if results else None
    
    @staticmethod
    def get_requests_for_group(group_id: int) -> List[Dict[str, Any]]:
        query = """
            SELECT gr.*, s.name, s.fax_n, s.pager_n, s.avatar_url
            FROM group_requests gr
            JOIN Student s ON gr.student_id = s.id
            WHERE gr.group_id = ?
            ORDER BY s.name
        """
        results = execute_query(query, (group_id,))
        return [dict(row) for row in results]
    
    @staticmethod
    def get_requests_by_student(student_id: int) -> List[Dict[str, Any]]:
        query = """
            SELECT gr.*, g.unit_code, g.num as assessment_num, g.id as group_number
            FROM group_requests gr
            JOIN groups g ON gr.group_id = g.id
            WHERE gr.student_id = ?
            ORDER BY g.unit_code, g.num, g.id
        """
        results = execute_query(query, (student_id,))
        return [dict(row) for row in results]
    
    @staticmethod
    def delete_request(group_id: int, student_id: int) -> bool:
        query = "DELETE FROM group_requests WHERE group_id = ? AND student_id = ?"
        return execute_update(query, (group_id, student_id)) > 0
    
    @staticmethod
    def delete_requests_for_group(group_id: int) -> int:
        query = "DELETE FROM group_requests WHERE group_id = ?"
        return execute_update(query, (group_id,))
    
    @staticmethod
    def delete_requests_by_student(student_id: int) -> int:
        query = "DELETE FROM group_requests WHERE student_id = ?"
        return execute_update(query, (student_id,))
    
    @staticmethod
    def request_exists(group_id: int, student_id: int) -> bool:
        query = "SELECT 1 FROM group_requests WHERE group_id = ? AND student_id = ? LIMIT 1"
        results = execute_query(query, (group_id, student_id))
        return len(results) > 0
    
    @staticmethod
    def get_all_requests() -> List[Dict[str, Any]]:
        query = """
            SELECT gr.*, s.name as student_name, 
                   g.unit_code, g.num as assessment_num, g.id as group_number
            FROM group_requests gr
            JOIN Student s ON gr.student_id = s.id
            JOIN groups g ON gr.group_id = g.id
            ORDER BY g.unit_code, g.num, g.id, s.name
        """
        results = execute_query(query, ())
        return [dict(row) for row in results]
    
    @staticmethod
    def get_requests_for_unit(unit_code: str) -> List[Dict[str, Any]]:
        query = """
            SELECT gr.*, s.name as student_name, 
                   g.num as assessment_num, g.id as group_number
            FROM group_requests gr
            JOIN Student s ON gr.student_id = s.id
            JOIN groups g ON gr.group_id = g.id
            WHERE g.unit_code = ?
            ORDER BY g.num, g.id, s.name
        """
        results = execute_query(query, (unit_code,))
        return [dict(row) for row in results]
    
    @staticmethod
    def get_requests_for_assessment(unit_code: str, num: int) -> List[Dict[str, Any]]:
        query = """
            SELECT gr.*, s.name as student_name, g.id as group_number
            FROM group_requests gr
            JOIN Student s ON gr.student_id = s.id
            JOIN groups g ON gr.group_id = g.id
            WHERE g.unit_code = ? AND g.num = ?
            ORDER BY g.id, s.name
        """
        results = execute_query(query, (unit_code, num))
        return [dict(row) for row in results]
    
    @staticmethod
    def get_request_count_for_group(group_id: int) -> int:
        query = "SELECT COUNT(*) FROM group_requests WHERE group_id = ?"
        results = execute_query(query, (group_id,))
        return results[0][0] if results else 0