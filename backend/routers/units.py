from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional

from database import Units, Assessments, Enrolments, Groups



class UnitCreate(BaseModel):
    code: str
    name: str
    description: Optional[str] = ""

class UnitUpdate(BaseModel):
    name: str
    description: Optional[str] = ""


class AssessmentCreate(BaseModel):
    num: int
    grade: Optional[float] = None
    due_week: Optional[int] = None
    group_size: Optional[int] = None
    group_formation_week: Optional[int] = None

class AssessmentUpdate(BaseModel):
    grade: Optional[float] = None
    due_week: Optional[int] = None
    group_size: Optional[int] = None
    group_formation_week: Optional[int] = None


class GroupCreate(BaseModel):
    name: str



router = APIRouter()


@router.get("/")
def list_units():
    return {"units": Units.get_all()}

@router.get("/{code}/")
def get_unit(code: str):
    unit = Units.get_by_code(code)
    if not unit:
        raise HTTPException(404, "Unit not found")
    return {"unit": unit}


@router.post("/")
def create_unit(unit: UnitCreate):
    if not Units.create(unit.code, unit.name, unit.description or ""):
        raise HTTPException(400, "Unit already exists")
    return {"unit": unit}, 201


@router.put("/{code}/")
def get_unit(code: str, unit_details: UnitUpdate):
    unit = Units.update(code, unit_details.name, unit_details.description or "")
    if not unit:
        raise HTTPException(404, "Unit not found")
    return {"unit": unit}

@router.delete("/{code}/")
def create_unit(code: str):
    if not Units.delete(code):
        raise HTTPException(404, "Unit not found")
    return None, 204


@router.get(":search/", tags=["units"])
def search_units(query: str = Query(..., min_length=1)):
    return {"units": Units.search_by_name(query)}


@router.get("/{code}/enrolments/")
def unit_students(unit_code: str):
    return {"student enrolments": Enrolments.get_unit_students(unit_code)}


@router.get("/{code}/assessments")
def get_unit_assessment(code: str):
    unit_assessments = Assessments.get_by_unit(code)
    if not unit_assessments:
        raise HTTPException(404, "Assessments not found")
    return {"assessments": unit_assessments}

@router.get("/{code}/assessments/{num}/")
def get_assessment(unit_code: str, num: int):
    assessment = Assessments.get_by_key(unit_code, num)
    if not assessment:
        raise HTTPException(404, "Assessment not found")
    return {"assessment": assessment}

@router.post("/{code}/assessments/")
def create_assessment(code: str, assessment: AssessmentCreate):
    if not Assessments.create(
        code, assessment.num, assessment.grade, assessment.due_week, assessment.group_size, assessment.group_formation_week
    ):
        raise HTTPException(400, "Assessment already exists")
    return {"assessment": assessment}, 201

@router.put("/{code}/assessments/{num}/")
def update_assessment(unit_code: str, num: int, assessment: AssessmentUpdate):
    if not Assessments.update(
        unit_code, num, assessment.grade, assessment.due_week, assessment.group_size, assessment.group_formation_week
    ):
        raise HTTPException(404, "Assessment not found.")
    return {"assessment": assessment}

@router.delete("/{code}/assessments/{num}/")
def delete_assessment(unit_code: str, num: int):
    if not Assessments.delete(unit_code, num):
        raise HTTPException(404, "Assessment not found")
    return None, 204


@router.get("/{code}/assessments/{num}/groups/")
def list_groups():
    return {"Groups": Groups.get_all()}

@router.post("/{code}/assessments/{num}/groups/")
def create_group(code: int, num: int, group: GroupCreate):
    new_group = Groups.create(code, num, group.name)
    if not new_group:
        raise HTTPException(400, "Group already exists")
    return {"Group": new_group}, 201