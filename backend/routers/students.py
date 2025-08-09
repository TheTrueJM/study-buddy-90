from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from database import Students, Enrolments, GroupMembers, GroupRequests



class StudentCreate(BaseModel):
    id: int
    name: str
    password: str  
    fax_num: Optional[str] = ""
    pager_num: Optional[str] = ""
    avatar_url: Optional[str] = ""

class StudentUpdate(BaseModel):
    name: str
    fax_num: Optional[str] = ""
    pager_num: Optional[str] = ""
    avatar_url: Optional[str] = ""

class StudentUpdatePassword(BaseModel):
    cur_password: str
    new_password: str



router = APIRouter()

@router.get("/")
def list_students() -> List[Dict[str, Any]]:
    return {"students": Students.get_all()}

@router.get("/{id}")
def get_student_by_id(id: int):
    student = Students.get_by_id(id)
    if not student:
        raise HTTPException(404, "Student not found")
    return {"student": student}


@router.post("/")
def create_student(student: StudentCreate):
    if not Students.create(
        id=student.id,
        name=student.name,
        password=student.password,
        fax_num=student.fax_num or "",
        pager_num=student.pager_num or "",
        avatar_url=student.avatar_url or "",
    ):
        raise HTTPException(400, "Student ID already exists")
    return {"student": student}, 201


@router.put("/{id}/")
def update_student(id: int, student: StudentUpdate):
    if not Students.update(
        id=id,
        name=student.name,
        fax_num=student.fax_num or "",
        pager_num=student.pager_num or "",
        avatar_url=student.avatar_url or "",
    ):
        raise HTTPException(404, "Student ID not found")
    return {"student": student}

@router.put("/{id}/update-password/")
def update_student(id: int, student: StudentUpdatePassword):
    if not Students.update(
        id=id,
        cur_password=student.cur_password,
        new_password=student.new_password,
    ):
        raise HTTPException(404, "Student ID not found")
    return {"student": student}

@router.delete("/students/{student_id}", tags=["students"])
def delete_student(student_id: int):
    if not Students.delete(student_id):
        raise HTTPException(404, "Student not found")
    return None, 204


@router.get(":search/")
def search_students(q: str = Query(..., min_length=1)):
    return {"students": Students.search_by_name(q)}


@router.get("/{id}/enrolments/")
def units_for_student(id: int):
    return {"enrolments": Enrolments.get_student_enrolments(id)}

@router.get("/{id}/enrolments:active/")
def active_enrolments(id: int):
    return {"active enrolments": Enrolments.get_active_enrolments(id)}

@router.get("/{id}/enrolments:completed/")
def completed_enrolments(id: int):
    return {"completed enrolments": Enrolments.get_completed_enrolments(id)}


@router.get("/{id}/groups")
def list_groups():
    return {"Groups": Students.get_groups()}

@router.get("/{id}/requests")
def list_requests():
    return {"Groups": Students.get_requests()}