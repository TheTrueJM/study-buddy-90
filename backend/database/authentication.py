from typing import Optional
import bcrypt
from .connection import execute_query

def verify_credentials(student_id: int, password: str) -> bool:
    """
    Returns True if there's a Student with this name whose bcrypt hash
    matches `password`. Otherwise False.
    """
    rows = execute_query(
        "SELECT student_id, password FROM Student WHERE student_id = ? LIMIT 1",
        (student_id,)
    )
    if not rows:
        return False

    stored_hash = rows[0]["password"]  
    if isinstance(stored_hash, str):
        stored_hash = stored_hash.encode()

    try:
        return bcrypt.checkpw(password.encode(), stored_hash)
    except Exception:
        return False
    
    
