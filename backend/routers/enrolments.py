from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from database.enrolments import Enrolments



class EnrolCreate(BaseModel):
    unit_code: str
    student_id: int
    grade: float = 0.0
    availability: str = ""
    complete: bool = False

class EnrolUpdate(BaseModel):
    grade: float
    availability: str
    complete: bool



router = APIRouter()


@router.get("/")
def list_enrolments():
    return {"enrolments": Enrolments.get_all_enrolments()}

@router.post("/")
def enroll_student(enrolment: EnrolCreate):
    if not Enrolments.enroll_student(enrolment.unit_code, enrolment.student_id, enrolment.grade, enrolment.availability, enrolment.complete):
        raise HTTPException(400, "Enrolment already exists")
    return {"enrolment": enrolment}, 201

@router.put("/{unit_code}/{student_id}/")
def update_enrolment(unit_code: str, student_id: int, enrolment: EnrolUpdate):
    if not Enrolments.update(unit_code, student_id, enrolment.grade, enrolment.availability, enrolment.complete):
        raise HTTPException(404, "Enrolment not found")
    return {"enrolment": enrolment}

@router.delete("/{unit_code}/{student_id}/")
def unenroll_student(unit_code: str, student_id: int):
    if not Enrolments.delete(unit_code, student_id):
        raise HTTPException(404, "Enrolment not found")
    return None, 204