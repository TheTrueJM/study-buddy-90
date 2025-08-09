from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from database.schema import init_database
from database.student import Student
from database.units import Units
from database.groups import Groups
from database.unit_enrolment import UnitEnrolment
from database.group_requests import GroupRequests

app = FastAPI(title="Study Buddy API")

@app.on_event("startup")
def startup() -> None:
    init_database()

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
        raise HTTPException(404, "Student not found")
    return row

@app.post("/students", tags=["students"])
def create_student(body: StudentCreate):
    new_id = Student.create(
        name=body.name,
        password=(body.password.encode() if isinstance(body.password, str) else body.password),
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
        (body.password.encode() if isinstance(body.password, str) else body.password),
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

@app.get("/group-requests", tags=["group_requests"])
def list_group_requests():
    return GroupRequests.get_all_requests()

@app.get("/groups/{group_id}/requests", tags=["group_requests"])
def requests_for_group(group_id: int):
    return GroupRequests.get_requests_for_group(group_id)

@app.get("/students/{student_id}/group-requests", tags=["group_requests"])
def requests_by_student(student_id: int):
    return GroupRequests.get_requests_by_student(student_id)

@app.post("/group-requests", tags=["group_requests"])
def create_group_request(body: GroupRequestCreate):
    if not GroupRequests.create_request(body.group_id, body.student_id):
        raise HTTPException(400, "Request already exists?")
    return {"ok": True}

@app.delete("/group-requests/{group_id}/{student_id}", tags=["group_requests"])
def delete_group_request(group_id: int, student_id: int):
    if not GroupRequests.delete_request(group_id, student_id):
        raise HTTPException(404, "Request not found")
    return {"ok": True}

#database test
@app.get("/test-db")
def test_db():
    from database.connection import execute_query
    try:
        result = execute_query("SELECT name FROM sqlite_master WHERE type='table';", ())
        return {"tables": [row[0] for row in result]}
    except Exception as e:
        raise HTTPException(500, f"DB Error: {e}")
