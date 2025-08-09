from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

from database.schema import init_database
from database.student import Student
from database.units import Units
from database.groups import Groups
from database.authentication import *
from database.assessments import Assessments
from database.unit_enrolment import UnitEnrolment
from database.group_requests import GroupRequests
from database.group_member import GroupMember
from database.pager_and_fax import generate_contact_numbers
from database.messages import Messages

app = FastAPI(title="Study Buddy API")

@app.on_event("startup")
def startup() -> None:
    init_database()

name_input = "owentest"
password_input = "owentest1234"

@app.post("/login")
def login():
    if False: 
        raise Exception("Authentication Failed.")
    return {
        "success": verify_credentials(name_input, password_input)
    }

class SignUpBody(BaseModel):
    student_id: int
    name: str
    password: str
    avatar_url: Optional[str] = ""

@app.post("/auth/signup", tags=["auth"])
def signup(body: SignUpBody):
    if not hasattr(Student, "exists_by_id") or not hasattr(Student, "create_with_id"):
        raise HTTPException(status_code=500, detail="Student helper methods missing (exists_by_id/create_with_id)")
    if Student.exists_by_id(body.student_id):
        raise HTTPException(status_code=409, detail="Student ID already exists")

    pager_n, fax_n = generate_contact_numbers(str(body.student_id))

    new_id = Student.create_with_id(
        student_id=body.student_id,
        name=body.name,
        password=body.password,
        fax_n=fax_n,
        pager_n=pager_n,
        avatar_url=body.avatar_url or ""
    )

    row = Student.get_by_id(new_id)
    if row and "password" in row:
        del row["password"]
    return {"ok": True, "student": row}

class StudentCreate(BaseModel):
    name: str
    password: str  
    fax_n: Optional[str] = ""
    pager_n: Optional[str] = ""
    avatar_url: Optional[str] = ""

class StudentUpdate(StudentCreate):
    pass

@app.get("/students", tags=["students"])
def list_students() -> List[Dict[str, Any]]:
    return Student.get_all()

@app.get("/students/{student_id}", tags=["students"])
def get_student(student_id: int):
    row = Student.get_by_id(student_id)
    if not row:
        raise HTTPException(status_code=404, detail="Student not found")
    row.pop("password", None)
    return row

@app.post("/students", tags=["students"])
def create_student(body: StudentCreate):
    new_id = Student.create(
        name=body.name,
        password=body.password,  
        fax_n=body.fax_n or "",
        pager_n=body.pager_n or "",
        avatar_url=body.avatar_url or "",
    )
    return {"id": new_id}

@app.put("/students/{student_id}", tags=["students"])
def update_student(student_id: int, body: StudentUpdate):
    ok = Student.update(
        student_id,
        body.name,
        body.password,  
        body.fax_n or "",
        body.pager_n or "",
        body.avatar_url or "",
    )
    if not ok:
        raise HTTPException(404, "Student not found")
    return {"ok": True}

@app.delete("/students/{student_id}", tags=["students"])
def delete_student(student_id: int):
    if not Student.delete(student_id):
        raise HTTPException(404, "Student not found")
    return {"ok": True}

@app.get("/students:search", tags=["students"])
def search_students(q: str = Query(..., min_length=1)):
    return Student.search_by_name(q)

class UnitCreate(BaseModel):
    code: str
    name: str
    description: Optional[str] = ""

class UnitUpdate(BaseModel):
    name: str
    description: Optional[str] = ""

@app.get("/units", tags=["units"])
def list_units():
    return Units.get_all()

@app.get("/units/{code}", tags=["units"])
def get_unit(code: str):
    row = Units.get_by_code(code)
    if not row:
        raise HTTPException(404, "Unit not found")
    return row

@app.post("/units", tags=["units"])
def create_unit(body: UnitCreate):
    if not Units.create(body.code, body.name, body.description or ""):
        raise HTTPException(400, "Unit already exists")
    return {"ok": True}

@app.put("/units/{code}", tags=["units"])
def update_unit(code: str, body: UnitUpdate):
    if not Units.update(code, body.name, body.description or ""):
        raise HTTPException(404, "Unit not found")
    return {"ok": True}

@app.delete("/units/{code}", tags=["units"])
def delete_unit(code: str):
    if not Units.delete(code):
        raise HTTPException(404, "Unit not found")
    return {"ok": True}

@app.get("/units:search", tags=["units"])
def search_units(q: str = Query(..., min_length=1)):
    return Units.search_by_name(q)

class AssessmentCreate(BaseModel):
    unit_code: str
    num: int
    size: Optional[int] = None
    due_week: Optional[int] = None
    grade: Optional[float] = None
    group_formation_week: Optional[int] = None

class AssessmentUpdate(BaseModel):
    size: Optional[int] = None
    due_week: Optional[int] = None
    grade: Optional[float] = None
    group_formation_week: Optional[int] = None

@app.get("/assessments", tags=["assessments"])
def list_assessments():
    return Assessments.get_all()

@app.get("/assessments/{code}", tags=["assessments"])
def get_assessment(unit_code: str):
    row = Assessments.get_by_unit(unit_code)
    if not row:
        raise HTTPException(404, "Assessment not found")
    return row

@app.post("/assessments", tags=["assessments"])
def create_assessment(body: AssessmentCreate):
    ok = AssessmentCreate(
        body.unit_code, body.num, body.size, body.due_week, body.grade, body.group_formation_week
    )
    if not ok:
        raise HTTPException(400, "Assessment already exists")
    return {"ok": True}

@app.put("/assessments/{code}", tags=["assessments"])
def update_assessment(unit_code: str, num: int, body: AssessmentUpdate):
    ok = AssessmentCreate(
        body.unit_code, body.num, body.size, body.due_week, body.grade, body.group_formation_week
    )
    if not ok:
        raise HTTPException(404, "Assessment not found.")
    return {"ok": True}

@app.delete("/assessments/{code}", tags=["assessments"])
def delete_assessment(unit_code: str, num: int):
    if not Assessments.delete(unit_code, num):
        raise HTTPException(404, "Assessment not found")
    return {"ok": True}

class GroupCreate(BaseModel):
    unit_code: str
    num: int
    # id will be auto-assigned

@app.get("/groups", tags=["groups"])
def list_groups():
    return Groups.get_all()

@app.get("/units/{unit_code}/assessments/{num}/groups", tags=["groups"])
def list_groups_for_assessment(unit_code: str, num: int):
    return Groups.get_by_assessment(unit_code, num)

@app.post("/groups", tags=["groups"])
def create_group(body: GroupCreate):
    next_id = Groups.get_next_group_id(body.unit_code, body.num)
    if not Groups.create(body.unit_code, body.num, next_id):
        raise HTTPException(400, "Group already exists")
    return {"unit_code": body.unit_code, "num": body.num, "id": next_id}

@app.delete("/groups/{unit_code}/{num}/{id}", tags=["groups"])
def delete_group(unit_code: str, num: int, id: int):
    if not Groups.delete(unit_code, num, id):
        raise HTTPException(404, "Group not found")
    return {"ok": True}

class GroupMemberCreate(BaseModel):
    group_id: int
    student_id: int

@app.get("/group-members", tags=["group_members"])
def list_all_group_memberships():
    return GroupMember.get_all_memberships()

@app.get("/groups/{group_id}/members", tags=["group_members"])
def members_in_group(group_id: int):
    return GroupMember.get_group_members(group_id)

@app.get("/students/{student_id}/groups", tags=["group_members"])
def groups_for_student(student_id: int):
    return GroupMember.get_student_groups(student_id)

@app.post("/group-members", tags=["group_members"])
def add_group_member(body: GroupMemberCreate):
    if not GroupMember.add_member(body.group_id, body.student_id):
        raise HTTPException(400, "Could not add member (may already exist)")
    return {"ok": True}

@app.delete("/groups/{group_id}/members/{student_id}", tags=["group_members"])
def remove_group_member(group_id: int, student_id: int):
    if not GroupMember.remove_member(group_id, student_id):
        raise HTTPException(404, "Member not found in group")
    return {"ok": True}

@app.get("/groups/{group_id}/members/count", tags=["group_members"])
def group_size(group_id: int):
    return {"count": GroupMember.get_group_size(group_id)}

@app.delete("/groups/{group_id}/members", tags=["group_members"])
def remove_all_members(group_id: int):
    removed_count = GroupMember.remove_all_members(group_id)
    return {"removed": removed_count}

@app.get("/units/{unit_code}/assessments/{num}/students-without-group", tags=["group_members"])
def students_without_group(unit_code: str, num: int):
    return GroupMember.get_students_without_group(unit_code, num)

class EnrolCreate(BaseModel):
    unit_code: str
    student_id: int
    grade: float = 0.0
    completed: bool = False
    availability: str = ""

class EnrolUpdate(BaseModel):
    grade: float
    completed: bool
    availability: str

@app.get("/enrolments", tags=["enrolments"])
def list_enrolments():
    return UnitEnrolment.get_all_enrolments()

@app.get("/units/{unit_code}/enrolments", tags=["enrolments"])
def students_in_unit(unit_code: str):
    return UnitEnrolment.get_students_in_unit(unit_code)

@app.get("/students/{student_id}/enrolments", tags=["enrolments"])
def units_for_student(student_id: int):
    return UnitEnrolment.get_student_units(student_id)

@app.get("/students/{student_id}/enrolments:active", tags=["enrolments"])
def active_enrolments(student_id: int):
    return UnitEnrolment.get_active_enrolments(student_id)

@app.get("/students/{student_id}/enrolments:completed", tags=["enrolments"])
def completed_enrolments(student_id: int):
    return UnitEnrolment.get_completed_enrolments(student_id)

@app.post("/enrolments", tags=["enrolments"])
def enroll_student(body: EnrolCreate):
    if not UnitEnrolment.enroll_student(
        body.unit_code, body.student_id, body.grade, body.completed, body.availability
    ):
        raise HTTPException(400, "Enrolment already exists?")
    return {"ok": True}

@app.put("/enrolments/{unit_code}/{student_id}", tags=["enrolments"])
def update_enrolment(unit_code: str, student_id: int, body: EnrolUpdate):
    if not UnitEnrolment.update_enrolment(unit_code, student_id, body.grade, body.completed, body.availability):
        raise HTTPException(404, "Enrolment not found")
    return {"ok": True}

@app.delete("/enrolments/{unit_code}/{student_id}", tags=["enrolments"])
def unenroll_student(unit_code: str, student_id: int):
    if not UnitEnrolment.unenroll_student(unit_code, student_id):
        raise HTTPException(404, "Enrolment not found")
    return {"ok": True}

class GroupRequestCreate(BaseModel):
    group_id: int
    student_id: int

@app.post("/group-requests", tags=["group_requests"])
def create_group_request(body: GroupRequestCreate):
    if GroupRequests.request_exists(body.group_id, body.student_id):
        raise HTTPException(400, "Request already exists")
    if not GroupRequests.create_request(body.group_id, body.student_id):
        raise HTTPException(400, "Could not create request")
    return {"ok": True}

@app.get("/groups/{group_id}/requests", tags=["group_requests"])
def requests_for_group(group_id: int):
    return GroupRequests.get_requests_for_group(group_id)

@app.post("/group-requests/{group_id}/{student_id}/accept", tags=["group_requests"])
def accept_group_request(group_id: int, student_id: int):
    if not GroupRequests.request_exists(group_id, student_id):
        raise HTTPException(404, "Request not found")
    if not GroupMember.add_member(group_id, student_id):
        raise HTTPException(400, "Could not add member to group (may already be in)")
    GroupRequests.delete_request(group_id, student_id)
    return {"ok": True, "message": "Request accepted and member added"}

@app.post("/group-requests/{group_id}/{student_id}/deny", tags=["group_requests"])
def deny_group_request(group_id: int, student_id: int):
    if not GroupRequests.request_exists(group_id, student_id):
        raise HTTPException(404, "Request not found")
    GroupRequests.delete_request(group_id, student_id)
    return {"ok": True, "message": "Request denied and removed"}

class SendMessageBody(BaseModel):
    sender_id: int
    recipient_pager: str
    body: str = Field(..., max_length=160)

@app.post("/messages", tags=["messages"])
def send_message(body: SendMessageBody):
    recipient = Student.get_by_pager(body.recipient_pager)
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient pager not found")
    try:
        msg_id = Messages.send(
            sender_id=body.sender_id,
            recipient_id=recipient["student_id"],
            body=body.body
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"ok": True, "message_id": msg_id}

@app.get("/users/{student_id}/inbox", tags=["messages"])
def get_inbox(student_id: int):
    return Messages.get_inbox(student_id)

@app.get("/users/{student_id}/outbox", tags=["messages"])
def get_outbox(student_id: int):
    return Messages.get_outbox(student_id)

@app.get("/users/{a_id}/conversation/{b_id}", tags=["messages"])
def get_conversation(a_id: int, b_id: int, limit: int = 50):
    return Messages.get_conversation(a_id, b_id, limit)

@app.post("/messages/{message_id}/read", tags=["messages"])
def mark_message_read(message_id: int):
    if not Messages.mark_read(message_id):
        raise HTTPException(status_code=404, detail="Message not found")
    return {"ok": True}

@app.delete("/messages/{message_id}", tags=["messages"])
def delete_message(message_id: int, acting_user_id: int):
    if not Messages.delete(message_id, acting_user_id):
        raise HTTPException(status_code=404, detail="Message not found or no permission")
    return {"ok": True}

@app.get("/users/{student_id}/unread-count", tags=["messages"])
def unread_count(student_id: int):
    return {"unread": Messages.unread_count(student_id)}


#database test
@app.get("/test-db")
def test_db():
    from database.connection import execute_query
    try:
        result = execute_query("SELECT name FROM sqlite_master WHERE type='table';", ())
        return {"tables": [row[0] for row in result]}
    except Exception as e:
        raise HTTPException(500, f"DB Error: {e}")

