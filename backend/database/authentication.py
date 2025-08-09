from .students import Students

def verify_credentials(username: str, password: str) -> bool:
    """
    Verify user credentials by username and password.
    This is a wrapper around Students.verify_credentials to match the main.py import.
    """
    # First find the student by name
    students = Students.search_by_name(username)
    if not students:
        return False
    
    # Find exact match
    student = next((s for s in students if s['name'] == username), None)
    if not student:
        return False
    
    # Verify password using student ID
    return Students.verify_credentials(student['id'], password)