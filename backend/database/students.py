import bcrypt
from typing import List, Dict, Any
from .connection import execute_query, execute_update, execute_insert

class Students:
    @staticmethod
    def create(
        id: int, name: str, password: str, fax_num: str, pager_num: str, avatar_url: str
    ) -> int:
        hashedpw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        query = """
            INSERT INTO Students (id, name, password, fax_n, pager_n, avatar_url)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        return execute_insert(query, (id, name, hashedpw, fax_num, pager_num, avatar_url))


    @staticmethod
    def get_by_id(id: int) -> Dict[str, Any] | None:
        query = "SELECT * FROM Students WHERE id = ?"
        results = execute_query(query, (id,))
        return dict(results[0]) if results else None

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        query = "SELECT * FROM Students ORDER BY name"
        results = execute_query(query, ())
        return [dict(row) for row in results]
    

    @staticmethod
    def update(id: int, name: str, fax_n: str, pager_n: str, avatar_url: str) -> bool:
        query = "UPDATE Students SET name = ?, fax_n = ?, pager_n = ?, avatar_url = ? WHERE id = ?"
        return execute_update(query, (name, fax_n, pager_n, avatar_url, id)) > 0

    @staticmethod
    def delete(id: int) -> bool:
        query = "DELETE FROM Students WHERE id = ?"
        return execute_update(query, (id,)) > 0


    @staticmethod
    def verify_password(student_id: int, plain_password: str) -> bool:
        query = "SELECT password FROM Students WHERE id = ?"
        results = execute_query(query, (student_id,))
        if not results:
            return False
        stored_hash = results[0][0]  # bytes
        return bcrypt.checkpw(plain_password.encode(), stored_hash)
    
    @staticmethod
    def update_password(id: int, cur_password: str, new_password: str) -> bool:
        if not Students.verify_password(cur_password):
            return False
        hashed_pw = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
        query = "UPDATE Students SET password = ? WHERE id = ?"
        return execute_update(query, (hashed_pw, id)) > 0
    

    @staticmethod
    def search_by_name(name_pattern: str) -> List[Dict[str, Any]]:
        query = "SELECT * FROM Students WHERE name LIKE ? ORDER BY name"
        results = execute_query(query, (f"%{name_pattern}%",))
        return [dict(row) for row in results]
    

    @staticmethod
    def get_groups(id: int) -> List[Dict[str, Any]]:
        query = """
            SELECT g.*
            FROM Groups g
            JOIN GroupMembers gm ON g.id = gm.group_id
            WHERE gm.student_id = ?
            ORDER BY g.unit_code, g.num
        """
        results = execute_query(query, (id,))
        return [dict(row) for row in results]
    
    @staticmethod
    def get_requests(id: int) -> List[Dict[str, Any]]:
        query = """
            SELECT g.*
            FROM Groups g
            JOIN GroupRequests gr ON g.id = gr.group_id
            WHERE gr.student_id = ?
            ORDER BY g.unit_code, g.num
        """
        results = execute_query(query, (id,))
        return [dict(row) for row in results]
    
    @staticmethod
    def delete_all_requests(id: int) -> int:
        query = "DELETE FROM group_requests WHERE student_id = ?"
        return execute_update(query, (id,))