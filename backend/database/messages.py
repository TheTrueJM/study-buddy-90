from typing import List, Dict, Any, Optional
import time
from .connection import execute_query, execute_update, execute_insert

PAGER_CHAR_LIMIT = 160 

class Messages:
    @staticmethod
    def send(sender_id: int, recipient_id: int, body: str, created_at: Optional[int] = None) -> int:
        if body is None:
            body = ""
        if len(body) > PAGER_CHAR_LIMIT:
            raise ValueError(f"Message too long (>{PAGER_CHAR_LIMIT} chars)")
        ts = created_at if created_at is not None else int(time.time())
        q = """
            INSERT INTO messages (sender_id, recipient_id, body, created_at, read)
            VALUES (?, ?, ?, ?, 0)
        """
        return execute_insert(q, (sender_id, recipient_id, body, ts))

    @staticmethod
    def get_inbox(user_id: int) -> List[Dict[str, Any]]:
        q = """
            SELECT m.*, s.name AS sender_name
            FROM messages m
            JOIN Student s ON m.sender_id = s.student_id
            WHERE m.recipient_id = ?
            ORDER BY m.created_at DESC, m.id DESC
        """
        rows = execute_query(q, (user_id,))
        return [dict(r) for r in rows]

    @staticmethod
    def get_outbox(user_id: int) -> List[Dict[str, Any]]:
        q = """
            SELECT m.*, r.name AS recipient_name
            FROM messages m
            JOIN Student r ON m.recipient_id = r.student_id
            WHERE m.sender_id = ?
            ORDER BY m.created_at DESC, m.id DESC
        """
        rows = execute_query(q, (user_id,))
        return [dict(r) for r in rows]

    @staticmethod
    def get_conversation(a_user_id: int, b_user_id: int, limit: int = 100) -> List[Dict[str, Any]]:
        q = """
            SELECT m.*, s.name AS sender_name, r.name AS recipient_name
            FROM messages m
            JOIN Student s ON m.sender_id = s.student_id
            JOIN Student r ON m.recipient_id = r.student_id
            WHERE (m.sender_id = ? AND m.recipient_id = ?)
               OR (m.sender_id = ? AND m.recipient_id = ?)
            ORDER BY m.created_at DESC, m.id DESC
            LIMIT ?
        """
        rows = execute_query(q, (a_user_id, b_user_id, b_user_id, a_user_id, limit))
        return [dict(r) for r in rows]

    @staticmethod
    def mark_read(message_id: int) -> bool:
        q = "UPDATE messages SET read = 1 WHERE id = ?"
        return execute_update(q, (message_id,)) > 0

    @staticmethod
    def mark_all_read(user_id: int, from_user_id: Optional[int] = None) -> int:
        if from_user_id is None:
            q = "UPDATE messages SET read = 1 WHERE recipient_id = ? AND read = 0"
            return execute_update(q, (user_id,))
        q = "UPDATE messages SET read = 1 WHERE recipient_id = ? AND sender_id = ? AND read = 0"
        return execute_update(q, (user_id, from_user_id))

    @staticmethod
    def delete(message_id: int, acting_user_id: int) -> bool:
        # allow delete if user is sender or recipient
        q = "DELETE FROM messages WHERE id = ? AND (sender_id = ? OR recipient_id = ?)"
        return execute_update(q, (message_id, acting_user_id, acting_user_id)) > 0

    @staticmethod
    def unread_count(user_id: int) -> int:
        q = "SELECT COUNT(*) FROM messages WHERE recipient_id = ? AND read = 0"
        rows = execute_query(q, (user_id,))
        return rows[0][0] if rows else 0
