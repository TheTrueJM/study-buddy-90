from .connection import get_connection, get_db_connection, execute_query, execute_update, execute_insert
from .schema import create_tables, init_database
from .student import Student
from .units import Units
from .assessments import Assessments
from .groups import Groups
from .group_member import GroupMember
from .unit_enrolment import UnitEnrolment
from .group_requests import GroupRequests

__all__ = [
    'get_connection', 'get_db_connection', 'execute_query', 'execute_update', 'execute_insert',
    'create_tables', 'init_database',
    'Student', 'Units', 'Assessments', 'Groups', 
    'GroupMember', 'UnitEnrolment', 'GroupRequests'
]

def initialize_database():
    init_database()
