from typing import List, Dict, Any
from .connection import execute_query, execute_update, execute_insert

class TeamPosts:
    @staticmethod
    def create_post(student_id: int, unit_code: str, looking_for_team: bool, 
                   open_to_messages: bool, note: str) -> int:
        query = """
            INSERT INTO team_posts (student_id, unit_code, looking_for_team, open_to_messages, note)
            VALUES (?, ?, ?, ?, ?)
        """
        try:
            return execute_insert(query, (student_id, unit_code, looking_for_team, open_to_messages, note))
        except:
            return 0
    
    @staticmethod
    def get_post_by_id(post_id: int) -> Dict[str, Any] | None:
        query = """
            SELECT tp.*, s.name as student_name
            FROM team_posts tp
            JOIN Student s ON tp.student_id = s.id
            WHERE tp.id = ?
        """
        results = execute_query(query, (post_id,))
        return dict(results[0]) if results else None
    
    @staticmethod
    def get_posts_by_unit(unit_code: str) -> List[Dict[str, Any]]:
        query = """
            SELECT tp.*, s.name as student_name
            FROM team_posts tp
            JOIN Student s ON tp.student_id = s.id
            WHERE tp.unit_code = ?
            ORDER BY tp.created_at DESC
        """
        results = execute_query(query, (unit_code,))
        return [dict(row) for row in results]
    
    @staticmethod
    def get_all_posts() -> List[Dict[str, Any]]:
        query = """
            SELECT tp.*, s.name as student_name
            FROM team_posts tp
            JOIN Student s ON tp.student_id = s.id
            ORDER BY tp.created_at DESC
        """
        results = execute_query(query, ())
        return [dict(row) for row in results]
    
    @staticmethod
    def get_posts_by_student(student_id: int) -> List[Dict[str, Any]]:
        query = """
            SELECT tp.*, s.name as student_name
            FROM team_posts tp
            JOIN Student s ON tp.student_id = s.id
            WHERE tp.student_id = ?
            ORDER BY tp.created_at DESC
        """
        results = execute_query(query, (student_id,))
        return [dict(row) for row in results]
    
    @staticmethod
    def get_looking_for_team_posts() -> List[Dict[str, Any]]:
        query = """
            SELECT tp.*, s.name as student_name
            FROM team_posts tp
            JOIN Student s ON tp.student_id = s.id
            WHERE tp.looking_for_team = 1
            ORDER BY tp.created_at DESC
        """
        results = execute_query(query, ())
        return [dict(row) for row in results]
    
    @staticmethod
    def update_post(post_id: int, looking_for_team: bool, open_to_messages: bool, note: str) -> bool:
        query = """
            UPDATE team_posts 
            SET looking_for_team = ?, open_to_messages = ?, note = ?
            WHERE id = ?
        """
        return execute_update(query, (looking_for_team, open_to_messages, note, post_id)) > 0
    
    @staticmethod
    def delete_post(post_id: int) -> bool:
        query = "DELETE FROM team_posts WHERE id = ?"
        return execute_update(query, (post_id,)) > 0
    
    @staticmethod
    def delete_posts_by_student(student_id: int) -> int:
        query = "DELETE FROM team_posts WHERE student_id = ?"
        return execute_update(query, (student_id,))