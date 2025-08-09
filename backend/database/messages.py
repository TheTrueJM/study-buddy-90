from typing import List, Dict, Any, Optional
from .connection import execute_query, execute_update, execute_insert
import time

PAGER_CHAR_LIMIT = 160 

class Messages:
    @staticmethod
    def send(group_id: int, sender_id: int, body: str, created_at: Optional[int] = None) -> int:
        body = body or ""
        if len(body) > PAGER_CHAR_LIMIT:
            raise ValueError(f"Message too long (>{PAGER_CHAR_LIMIT} chars)")
        ts = created_at or int(time.time())
        q = "INSERT INTO Messages (sender_id, group_id, body, created_at) VALUES (?, ?, ?, ?)"
        return execute_insert(q, (sender_id, group_id, body, ts))


    @staticmethod
    def get_group_messages(group_id: int, limit: int = 100) -> List[Dict[str, Any]]:
        q = """
            SELECT * FROM Messages WHERE group_id = ?
            ORDER BY created_at DESC, id DESC LIMIT ?
        """
        rows = execute_query(q, (group_id, limit))
        return [dict(r) for r in rows]
    

    @staticmethod
    def delete(message_id: int, student_id: int) -> bool:
        q = "DELETE FROM Messages WHERE id = ? AND sender_id = ?"
        return execute_update(q, (message_id, student_id)) > 0
    
    # CHECK IF THIS WORKS
    @staticmethod
    def delete_all_by_group(group_id: int, student_id: int) -> bool:
        q = """
            DELETE FROM Messages WHERE group_id = ? AND (
                SELECT COUNT(*) FROM GroupMembers WHERE group_id = ? AND student_id = ?
            ) > 1
        """
        return execute_update(q, (group_id, group_id, student_id))

