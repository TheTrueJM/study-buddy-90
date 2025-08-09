from typing import Optional
import bcrypt
from .connection import execute_query

def verify_credentials(name: str, password: str) -> bool:
    """
    Returns True if there's a Student with this name whose bcrypt hash
    matches `password`. Otherwise False.
    """
    #name is not unique in the schema; this picks the first match.
    rows = execute_query(
        "SELECT id, password FROM Student WHERE name = ? LIMIT 1",
        (name,)
    )
    if not rows:
        return False

    stored_hash = rows[0]["password"]  # stored as bytes (BLOB)
    # Just in case the driver returns str in some envs:
    if isinstance(stored_hash, str):
        stored_hash = stored_hash.encode()

    try:
        return bcrypt.checkpw(password.encode(), stored_hash)
    except Exception:
        return False
    
    
