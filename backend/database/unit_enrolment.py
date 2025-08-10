from typing import List, Dict, Any
from .connection import execute_query, execute_update, execute_insert


class UnitEnrolment:
    @staticmethod
    def get_all_enrolments() -> List[Dict[str, Any]]:
        rows = execute_query(
            "SELECT unit_code, student_id, grade, completed, availability FROM unit_enrolment ORDER BY unit_code, student_id",
            (),
        )
        return [dict(row) for row in rows]

    @staticmethod
    def get_students_in_unit(unit_code: str) -> List[Dict[str, Any]]:
        rows = execute_query(
            """
            SELECT ue.unit_code, s.id AS student_id, s.name, ue.grade, ue.completed, ue.availability
            FROM unit_enrolment ue
            JOIN Student s ON s.id = ue.student_id
            WHERE ue.unit_code = ?
            ORDER BY s.name
            """,
            (unit_code,),
        )
        return [dict(row) for row in rows]

    @staticmethod
    def get_student_units(student_id: int) -> List[Dict[str, Any]]:
        rows = execute_query(
            """
            SELECT ue.unit_code, ue.grade, ue.completed, ue.availability
            FROM unit_enrolment ue
            WHERE ue.student_id = ?
            ORDER BY ue.unit_code
            """,
            (student_id,),
        )
        return [dict(row) for row in rows]

    @staticmethod
    def get_active_enrolments(student_id: int) -> List[Dict[str, Any]]:
        rows = execute_query(
            """
            SELECT ue.unit_code, ue.grade, ue.completed, ue.availability
            FROM unit_enrolment ue
            WHERE ue.student_id = ? AND ue.completed = 0
            ORDER BY ue.unit_code
            """,
            (student_id,),
        )
        return [dict(row) for row in rows]

    @staticmethod
    def get_completed_enrolments(student_id: int) -> List[Dict[str, Any]]:
        rows = execute_query(
            """
            SELECT ue.unit_code, ue.grade, ue.completed, ue.availability
            FROM unit_enrolment ue
            WHERE ue.student_id = ? AND ue.completed = 1
            ORDER BY ue.unit_code
            """,
            (student_id,),
        )
        return [dict(row) for row in rows]

    @staticmethod
    def enroll_student(
        unit_code: str, student_id: int, grade: float, completed: bool, availability: str
    ) -> bool:
        try:
            execute_insert(
                "INSERT INTO unit_enrolment (unit_code, student_id, grade, completed, availability) VALUES (?, ?, ?, ?, ?)",
                (unit_code, student_id, grade, int(bool(completed)), availability),
            )
            return True
        except Exception:
            return False

    @staticmethod
    def update_enrolment(
        unit_code: str, student_id: int, grade: float, completed: bool, availability: str
    ) -> bool:
        return (
            execute_update(
                """
                UPDATE unit_enrolment
                SET grade = ?, completed = ?, availability = ?
                WHERE unit_code = ? AND student_id = ?
                """,
                (grade, int(bool(completed)), availability, unit_code, student_id),
            )
            > 0
        )

    @staticmethod
    def unenroll_student(unit_code: str, student_id: int) -> bool:
        return (
            execute_update(
                "DELETE FROM unit_enrolment WHERE unit_code = ? AND student_id = ?",
                (unit_code, student_id),
            )
            > 0
        )

