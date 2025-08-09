from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional

from database import Students



class SignUpStudent(BaseModel):
    id: int
    name: str
    password: str
    avatar_url: Optional[str] = ""

class LoginStudent(BaseModel):
    id: int
    password: str



router = APIRouter()


@router.post("/signup/")
def signup(student: SignUpStudent):
    if Students.get_by_id(student.id):
        raise HTTPException(status_code=409, detail="Student ID already exists")

    pager_num, fax_num = Students.generate_contact_numbers(str(student.id))

    if not Students.create(
        id=student.id, name=student.name, password=student.password,
        fax_num=fax_num, pager_num=pager_num, avatar_url=student.avatar_url or ""
    ):
        raise HTTPException(400, "Failed to sign up student")
    return {"student": Students.get_by_id(student.id)}, 201

@router.post("/login/")
def login(student: LoginStudent):
    if not Students.verify_credentials(student.id, student.password):
        raise HTTPException(400, "Incorrect username or password")
    return {"success": True}