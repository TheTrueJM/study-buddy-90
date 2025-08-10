from typing import List, Dict, Any
from .connection import execute_query, execute_update, execute_insert

class Assessments:
    @staticmethod
    def create(
        unit_code: str, num: int, grade: float, due_week: int, group_size: int, group_formation_week: int
    ) -> bool:
        query = """
            INSERT INTO Assessments (unit_code, num, grade, due_week, group_size, group_formation_week)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        try:
            execute_insert(query, (unit_code, num, grade, due_week, group_size, group_formation_week))
            return True
        except:
            return False
    
    
    @staticmethod
    def get_by_key(unit_code: str, num: int) -> Dict[str, Any] | None:
        query = "SELECT * FROM Assessments WHERE unit_code = ? AND num = ?"
        results = execute_query(query, (unit_code, num))
        return dict(results[0]) if results else None
    
    @staticmethod
    def get_by_unit(unit_code: str) -> List[Dict[str, Any]]:
        query = "SELECT * FROM Assessments WHERE unit_code = ? ORDER BY num"
        results = execute_query(query, (unit_code,))
        return [dict(row) for row in results]
    
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        query = "SELECT * FROM Assessments ORDER BY unit_code, num"
        results = execute_query(query, ())
        return [dict(row) for row in results]
    

    @staticmethod
    def update(
        unit_code: str, num: int, grade: float, due_week: int, group_size: int, group_formation_week: int
    ) -> bool:
        query = """
            UPDATE Assessments SET grade = ?, due_week = ?, group_size = ?, group_formation_week = ?
            WHERE unit_code = ? AND num = ?
        """
        return execute_update(query, (grade, due_week, group_size, group_formation_week, unit_code, num)) > 0
    
    @staticmethod
    def delete(unit_code: str, num: int) -> bool:
        query = "DELETE FROM Assessments WHERE unit_code = ? AND num = ?"
        return execute_update(query, (unit_code, num)) > 0
    

    @staticmethod
    def get_by_due_week(due_week: int) -> List[Dict[str, Any]]:
        query = "SELECT * FROM Assessments WHERE due_week = ? ORDER BY unit_code, num"
        results = execute_query(query, (due_week,))
        return [dict(row) for row in results]
