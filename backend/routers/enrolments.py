from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from database.enrolments import Enrolments



class EnrolCreate(BaseModel):
    unit_code: str
    grade: float = 0.0
    availability: str = ""
    complete: bool = False

class EnrolUpdate(BaseModel):
    grade: float
    availability: str
    complete: bool



router = APIRouter()


@router.get("/{student_id}/")
def list_student_enrolments(student_id: int):
    return {"enrolments": Enrolments.get_student_enrolments(student_id)}

@router.post("/{student_id}/")
def enroll_student(student_id: int, enrolment: EnrolCreate):
    if not Enrolments.enroll_student(enrolment.unit_code, student_id, enrolment.grade, enrolment.availability, enrolment.complete):
        raise HTTPException(400, "Enrolment already exists")
    return {"enrolment": Enrolments.get_enrolment(enrolment.unit_code, student_id)}, 201

@router.put("/{student_id}/{unit_code}/")
def update_enrolment(student_id: int, unit_code: str, enrolment: EnrolUpdate):
    if not Enrolments.update(unit_code, student_id, enrolment.grade, enrolment.availability, enrolment.complete):
        raise HTTPException(404, "Enrolment not found")
    return {"enrolment": Enrolments.get_enrolment(unit_code, student_id)}

@router.delete("/{student_id}/{unit_code}/")
def unenroll_student(student_id: int, unit_code: str):
    if not Enrolments.delete(unit_code, student_id):
        raise HTTPException(404, "Enrolment not found")
    return None, 204