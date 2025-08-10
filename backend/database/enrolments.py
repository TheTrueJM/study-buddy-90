from typing import List, Dict, Any
from .connection import execute_query, execute_update, execute_insert

class Enrolments:
    @staticmethod
    def enroll_student(
        unit_code: str, student_id: int, grade: float, availability: str, complete: bool
    ) -> bool:
        query = """
            INSERT INTO Enrolments (unit_code, student_id, grade, availability, complete)
            VALUES (?, ?, ?, ?, ?)
        """
        try:
            execute_insert(query, (unit_code, student_id, grade, availability, complete))
            return True
        except:
            return False
    

    @staticmethod
    def get_student_enrolments(student_id: int) -> List[Dict[str, Any]]:
        query = "SELECT * FROM Enrolments WHERE student_id = ? ORDER BY unit_code"
        results = execute_query(query, (student_id,))
        return [dict(row) for row in results]

    @staticmethod
    def get_enrolment(unit_code: str, student_id: int) -> Dict[str, Any] | None:
        query = "SELECT * FROM Enrolments WHERE unit_code = ? AND student_id = ?"
        results = execute_query(query, (unit_code, student_id))
        return dict(results[0]) if results else None

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        query = "SELECT * FROM Enrolments ORDER BY unit_code, student_id"
        results = execute_query(query, ())
        return [dict(row) for row in results]
    
    @staticmethod
    def get_unit_students(unit_code: str) -> List[Dict[str, Any]]:
        query = """
            SELECT e.unit_code, s.id, s.name
            FROM Enrolments e
            JOIN Students s ON e.student_id = s.id
            WHERE e.unit_code = ?
            ORDER BY s.name
        """
        results = execute_query(query, (unit_code,))
        return [dict(row) for row in results]
    

    @staticmethod
    def update(unit_code: str, student_id: int, grade: float, availability: str, complete: bool) -> bool:
        query = """
            UPDATE Enrolments SET grade = ?, availability = ?, complete = ?
            WHERE unit_code = ? AND student_id = ?
        """
        return execute_update(query, (grade, availability, complete, unit_code, student_id)) > 0
    
    @staticmethod
    def delete(unit_code: str, student_id: int) -> bool:
        query = "DELETE FROM Enrolments WHERE unit_code = ? AND student_id = ?"
        return execute_update(query, (unit_code, student_id)) > 0
    

    @staticmethod
    def is_enrolled(unit_code: str, student_id: int) -> bool:
        query = "SELECT 1 FROM Enrolments WHERE unit_code = ? AND student_id = ? LIMIT 1"
        results = execute_query(query, (unit_code, student_id))
        return len(results) > 0

    @staticmethod
    def get_completed_enrolments(student_id: int) -> List[Dict[str, Any]]:
        query = "SELECT * FROM Enrolments WHERE e.student_id = ? AND complete = 1 ORDER BY code"
        results = execute_query(query, (student_id,))
        return [dict(row) for row in results]

    @staticmethod
    def get_active_enrolments(student_id: int) -> List[Dict[str, Any]]:
        query = "SELECT * FROM Enrolments WHERE e.student_id = ? AND complete = 0 ORDER BY code"
        results = execute_query(query, (student_id,))
        return [dict(row) for row in results]
    

    @staticmethod
    def get_unit_enrolment_count(unit_code: str) -> int:
        query = "SELECT COUNT(*) FROM Enrolments WHERE unit_code = ?"
        results = execute_query(query, (unit_code,))
        return results[0][0] if results else 0
    

    @staticmethod
    def get_students_by_availability(unit_code: str, availability_pattern: str) -> List[Dict[str, Any]]:
        query = """
            SELECT e.code, s.id, s.name
            FROM Enrolments e
            JOIN Student s ON e.student_id = s.id
            WHERE e.unit_code = ? AND e.availability LIKE ?
            ORDER BY s.name
        """
        results = execute_query(query, (unit_code, f"%{availability_pattern}%"))
        return [dict(row) for row in results]