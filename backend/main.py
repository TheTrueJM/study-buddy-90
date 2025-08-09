from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from database.schema import init_database
from database.student import Student
from database.units import Units
from database.assessments import Assessments
from database.groups import Groups
from database.unit_enrolment import UnitEnrolment
from database.group_requests import GroupRequests
from database.team_posts import TeamPosts
from database.authentication import verify_credentials

app = FastAPI(title="Study Buddy API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5174",  # Vite dev server default port
        "http://localhost:3000",  # Common React dev server port
        "http://127.0.0.1:5174",  # Alternative localhost
        "http://127.0.0.1:3000",  # Alternative localhost
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

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
    return {"ok": True}@app.delete("/students/{student_id}", tags=["students"])

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
    size: int
    due_week: int
    grade: float
    group_formation_week: Optional[int] = None

class AssessmentUpdate(BaseModel):
    size: int
    due_week: int
    grade: float
    group_formation_week: Optional[int] = None

@app.get("/assessments", tags=["assessments"])
def list_assessments():
    return Assessments.get_all()

@app.get("/units/{unit_code}/assessments", tags=["assessments"])
def list_unit_assessments(unit_code: str):
    return Assessments.get_by_unit(unit_code)

@app.get("/units/{unit_code}/assessments/{num}", tags=["assessments"])
def get_assessment(unit_code: str, num: int):
    row = Assessments.get_by_key(unit_code, num)
    if not row:
        raise HTTPException(404, "Assessment not found")
    return row

@app.post("/assessments", tags=["assessments"])
def create_assessment(body: AssessmentCreate):
    if not Assessments.create(body.unit_code, body.num, body.size, body.due_week, body.grade, body.group_formation_week):
        raise HTTPException(400, "Assessment already exists")
    return {"ok": True}

@app.put("/units/{unit_code}/assessments/{num}", tags=["assessments"])
def update_assessment(unit_code: str, num: int, body: AssessmentUpdate):
    if not Assessments.update(unit_code, num, body.size, body.due_week, body.grade, body.group_formation_week):
        raise HTTPException(404, "Assessment not found")
    return {"ok": True}

@app.delete("/units/{unit_code}/assessments/{num}", tags=["assessments"])
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

class TeamPostCreate(BaseModel):
    student_id: int
    unit_code: str
    looking_for_team: bool = True
    open_to_messages: bool = True
    note: str = ""

@app.get("/team-posts", tags=["team_posts"])
def list_team_posts():
    return TeamPosts.get_all_posts()

@app.get("/team-posts/looking-for-team", tags=["team_posts"])
def list_looking_for_team():
    return TeamPosts.get_looking_for_team_posts()

@app.post("/team-posts", tags=["team_posts"])
def create_team_post(body: TeamPostCreate):
    post_id = TeamPosts.create_post(
        body.student_id,
        body.unit_code,
        body.looking_for_team,
        body.open_to_messages,
        body.note
    )
    if post_id == 0:
        raise HTTPException(400, "Failed to create post")
    return {"id": post_id}

@app.delete("/team-posts/{post_id}", tags=["team_posts"])
def delete_team_post(post_id: int):
    if not TeamPosts.delete_post(post_id):
        raise HTTPException(404, "Post not found")
    return {"ok": True}

class authParams(BaseModel):
   pass

@app.post("/auth", tags=["auth"])
def auth(body: authParams):
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
