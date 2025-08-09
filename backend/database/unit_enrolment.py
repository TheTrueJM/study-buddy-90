from typing import List, Dict, Any
from .connection import execute_query, execute_update, execute_insert

class UnitEnrolment:
    @staticmethod
    def enroll_student(unit_code: str, student_id: int, grade: float,
                      completed: bool, availability: str) -> bool:
        query = """
            INSERT INTO unit_enrolment (unit_code, student_id, grade, completed, availability)
            VALUES (?, ?, ?, ?, ?)
        """
        try:
            execute_insert(query, (unit_code, student_id, grade, completed, availability))
            return True
        except:
            return False
    
    @staticmethod
    def get_enrolment(unit_code: str, student_id: int) -> Dict[str, Any] | None:
        query = "SELECT * FROM unit_enrolment WHERE unit_code = ? AND student_id = ?"
        results = execute_query(query, (unit_code, student_id))
        return dict(results[0]) if results else None
    
    @staticmethod
    def get_students_in_unit(unit_code: str) -> List[Dict[str, Any]]:
        query = """
            SELECT ue.*, s.name, s.fax_n, s.pager_n, s.avatar_url
            FROM unit_enrolment ue
            JOIN Student s ON ue.student_id = s.student_id
            WHERE ue.unit_code = ?
            ORDER BY s.name
        """
        results = execute_query(query, (unit_code,))
        return [dict(row) for row in results]
    
    @staticmethod
    def get_student_units(student_id: int) -> List[Dict[str, Any]]:
        query = """
            SELECT ue.*, u.name as unit_name, u.description
            FROM unit_enrolment ue
            JOIN Units u ON ue.unit_code = u.code
            WHERE ue.student_id = ?
            ORDER BY u.code
        """
        results = execute_query(query, (student_id,))
        return [dict(row) for row in results]
    
    @staticmethod
    def update_enrolment(unit_code: str, student_id: int, grade: float,
                        completed: bool, availability: str) -> bool:
        query = """
            UPDATE unit_enrolment SET grade = ?, completed = ?, availability = ? 
            WHERE unit_code = ? AND student_id = ?
        """
        return execute_update(query, (grade, completed, availability, unit_code, student_id)) > 0
    
    @staticmethod
    def unenroll_student(unit_code: str, student_id: int) -> bool:
        query = "DELETE FROM unit_enrolment WHERE unit_code = ? AND student_id = ?"
        return execute_update(query, (unit_code, student_id)) > 0
    
    @staticmethod
    def is_enrolled(unit_code: str, student_id: int) -> bool:
        query = "SELECT 1 FROM unit_enrolment WHERE unit_code = ? AND student_id = ? LIMIT 1"
        results = execute_query(query, (unit_code, student_id))
        return len(results) > 0
    
    @staticmethod
    def get_completed_enrolments(student_id: int) -> List[Dict[str, Any]]:
        query = """
            SELECT ue.*, u.name as unit_name, u.description
            FROM unit_enrolment ue
            JOIN Units u ON ue.unit_code = u.code
            WHERE ue.student_id = ? AND ue.completed = 1
            ORDER BY u.code
        """
        results = execute_query(query, (student_id,))
        return [dict(row) for row in results]
    
    @staticmethod
    def get_active_enrolments(student_id: int) -> List[Dict[str, Any]]:
        query = """
            SELECT ue.*, u.name as unit_name, u.description
            FROM unit_enrolment ue
            JOIN Units u ON ue.unit_code = u.code
            WHERE ue.student_id = ? AND ue.completed = 0
            ORDER BY u.code
        """
        results = execute_query(query, (student_id,))
        return [dict(row) for row in results]
    
    @staticmethod
    def get_all_enrolments() -> List[Dict[str, Any]]:
        query = """
            SELECT ue.*, s.name as student_name, u.name as unit_name
            FROM unit_enrolment ue
            JOIN Student s ON ue.student_id = s.student_id
            JOIN Units u ON ue.unit_code = u.code
            ORDER BY u.code, s.name
        """
        results = execute_query(query, ())
        return [dict(row) for row in results]
    
    @staticmethod
    def get_enrolment_count(unit_code: str) -> int:
        query = "SELECT COUNT(*) FROM unit_enrolment WHERE unit_code = ?"
        results = execute_query(query, (unit_code,))
        return results[0][0] if results else 0
    
    @staticmethod
    def get_students_by_availability(unit_code: str, availability_pattern: str) -> List[Dict[str, Any]]:
        query = """
            SELECT ue.*, s.name, s.fax_n, s.pager_n, s.avatar_url
            FROM unit_enrolment ue
            JOIN Student s ON ue.student_id = s.student_id
            WHERE ue.unit_code = ? AND ue.availability LIKE ?
            ORDER BY s.name
        """
        results = execute_query(query, (unit_code, f"%{availability_pattern}%"))
        return [dict(row) for row in results]
