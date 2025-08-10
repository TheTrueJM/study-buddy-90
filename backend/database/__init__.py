from .connection import get_connection, get_db_connection, execute_query, execute_update, execute_insert
from .schema import create_tables, init_database
from .students import Students
from .units import Units
from .assessments import Assessments
from .enrolments import Enrolments
from .groups import Groups
from .group_requests import GroupRequests
from .group_member import GroupMembers
from .messages import Messages


__all__ = [
    'get_connection', 'get_db_connection', 'execute_query', 'execute_update', 'execute_insert',
    'create_tables', 'init_database',
    'Students', 'Units', 'Assessments', 'Enrolments'
    'Groups', 'GroupRequests', 'GroupMembers', 'Messages'
]

def initialize_database():
    init_database()