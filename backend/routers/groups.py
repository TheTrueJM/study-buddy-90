from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from database import Groups, GroupMembers, GroupRequests, Messages



class GroupUpdate(BaseModel):
    name: str

class StudentAction(BaseModel):
    student_id: int

class CreateMessage(BaseModel):
    student_id: int
    body: str = Field(..., max_length=160)



router = APIRouter()


@router.get("/{id}/")
def get_group(id: int):
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
def list_member_requests(id: int):
    requests = Groups.get_requests(id)
    if not requests:
        raise HTTPException(404, "Group not found")
    return {"requests": requests}

@router.post("/{id}/requests/")
def add_member_request(id: int, request: StudentAction):
    if not GroupRequests.create_request(id, request.student_id):
        raise HTTPException(400, "Group request already exists")
    return {"request": request}, 201

@router.delete("/{id}/requests:deny/")
def delete_member_request(id: int, request: StudentAction):
    if not GroupRequests.delete_request(id, request.student_id):
        raise HTTPException(404, "Group request not found")
    return None, 204

@router.put("/{id}/requests:accept/")
def accept_request_as_member(id: int, member_request: StudentAction):
    if not GroupRequests.delete_request(id, member_request.student_id):
        raise HTTPException(404, "Group request not found")
    if not GroupMembers.add_member(id, member_request.student_id):
        raise HTTPException(400, "Group member already exists")
    return {"member": member_request}, 201


@router.get("/{id}/members/")
def list_members(id: int):
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
def get_size_count(id: int):
    count = Groups.get_current_size(id)
    if not count:
        raise HTTPException(404, "Group not found")
    return {"count": count}


@router.get("/{id}/messages/")
def list_messages(id: int):
    messages = Messages.get_group_messages(id)
    if not messages:
        raise HTTPException(404, "Group not found")
    return {"messages": messages}

@router.post("/{id}/messages/")
def create_message(id: int, message: CreateMessage):
    if not Messages.send(id, message.student_id, message.body):
        raise HTTPException(400, "Failed to create message")
    return {"message": message}, 201

@router.delete("/{id}/messages/{message_id}")
def delete_message(id: int, message_id: int, member: StudentAction):
    if not Messages.delete(message_id, member.student_id):
        raise HTTPException(404, "Message not found or no permission")
    return None, 204