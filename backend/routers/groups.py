from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from database import Groups, GroupMembers, GroupRequests



class GroupUpdate(BaseModel):
    name: str

class StudentAction(BaseModel):
    student_id: int



router = APIRouter()


@router.get("/{id}")
def get_group_by_id(id: int):
    group = Groups.get_by_id(id)
    if not group:
        raise HTTPException(404, "Group not found")
    return {"group": group}

@router.put("/{id}/")
def update_group(id: int, group: GroupUpdate):
    if not Groups.update(id, group.name):
        raise HTTPException(404, "Group not found")
    return {"group": group}

@router.delete("/{id}/")
def delete_group(id: int):
    if not Groups.delete(id):
        raise HTTPException(404, "Group not found")
    return None, 204


@router.get("/{id}/requests/")
def get_requests(id: int):
    requests = Groups.get_requests(id)
    if not requests:
        raise HTTPException(404, "Group not found")
    return {"requests": requests}

@router.post("/{id}/requests/")
def add_request(id: int, request: StudentAction):
    if not GroupRequests.create_request(id, request.student_id):
        raise HTTPException(400, "Group request already exists")
    return {"request": request}, 201

@router.delete("/{id}/requests:deny/")
def delete_request(id: int, request: StudentAction):
    if not GroupRequests.delete_request(id, request.student_id):
        raise HTTPException(404, "Group request not found")
    return None, 204

@router.put("/{id}requests:accept/")
def accept_member_request(id: int, member_request: StudentAction):
    if not GroupRequests.delete_request(id, member_request.student_id):
        raise HTTPException(404, "Group request not found")
    if not GroupMembers.add_member(id, member_request.student_id):
        raise HTTPException(400, "Group member already exists")
    return {"member": member_request}, 201


@router.get("/{id}/members/")
def get_members(id: int):
    members = Groups.get_members(id)
    if not members:
        raise HTTPException(404, "Group not found")
    return {"members": members}

@router.delete("/{id}/members/")
def remove_member(id: int, member: StudentAction):
    if not GroupMembers.remove_member(id, member.student_id):
        raise HTTPException(404, "Group member not found")
    return None, 204


@router.get("/{id}/members/count")
def get_group_by_id(id: int):
    count = Groups.get_current_size(id)
    if not count:
        raise HTTPException(404, "Group not found")
    return {"count": count}