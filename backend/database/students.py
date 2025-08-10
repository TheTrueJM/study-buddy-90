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
            INSERT INTO Students (id, name, password, fax_num, pager_num, avatar_url)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        try:
            execute_insert(query, (id, name, hashedpw, fax_num, pager_num, avatar_url))
            return True
        except:
            return False


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
    def update(id: int, name: str, fax_num: str, pager_num: str, avatar_url: str) -> bool:
        query = "UPDATE Students SET name = ?, fax_num = ?, pager_num = ?, avatar_url = ? WHERE id = ?"
        return execute_update(query, (name, fax_num, pager_num, avatar_url, id)) > 0

    @staticmethod
    def delete(id: int) -> bool:
        query = "DELETE FROM Students WHERE id = ?"
        return execute_update(query, (id,)) > 0


    @staticmethod
    def verify_credentials(id: int, plain_password: str) -> bool:
        query = "SELECT password FROM Students WHERE id = ?"
        results = execute_query(query, (id,))
        if not results:
            return False
        stored_hash = results[0][0]  # bytes
        # if isinstance(stored_hash, str):
        #     stored_hash = stored_hash.encode()
        return bcrypt.checkpw(plain_password.encode(), stored_hash)
    
    @staticmethod
    def update_password(id: int, cur_password: str, new_password: str) -> bool:
        if not Students.verify_credentials(id, cur_password):
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
    

    @staticmethod
    def generate_contact_numbers(student_id: str):
        """
        Generate a unique pager and fax number based on a student ID.
        The numbers follow a fixed prefix and embed the student ID digits.
        """

        student_id = ''.join(filter(str.isdigit, student_id))

        while len(student_id) < 8:
            student_id += student_id

        digits = student_id[:8]

        pager_prefix = "5"
        fax_prefix = "5"

        pager_num = f"{pager_prefix}{digits[0]}{digits[1]}-{digits[2]}{digits[3]}{digits[4]}-{digits[5]}{digits[6]}{digits[7]}{digits[0]}"
        fax_num = f"({fax_prefix}{digits[0]}{digits[1]}) {digits[2]}{digits[3]}{digits[4]}-{digits[5]}{digits[6]}{digits[7]}{digits[0]}"

        return pager_num, fax_num