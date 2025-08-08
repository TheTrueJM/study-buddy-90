# Database
tables:
Student -> [name, fax_n, pager_n, id (pk), avatar_url]
Units -> [name, code (pk), description]
Assesments -> [unit_code (ck), num (ck), size, due_week, grade, group_formation_week]`
groups -> [unit_code (ck), num (ck), id (ck)]
group_member -> [group_id (ck), student_id (ck)]
unit_enrolment -> [unit_code (ck), student_id (ck), grade, completed, availability]
group_requests -> [group_id (ck), student_id (ck)]

## Specifics:
- no ORM, pure SQL
- Sqlite local Database
- create tables if not exists
- stay minimal, dont add extra stuff
