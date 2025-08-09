from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional

from database.schema import init_database
from database.student import Student
from database.messages import Messages
from database.authentication import *
from database.pager_and_fax import generate_contact_numbers
from routers import students, units, enrolments, groups, auth

app = FastAPI(title="Study Mates API")

app.include_router(students.router, prefix="/students2", tags=["students2"])
app.include_router(units.router, prefix="/units", tags=["units"])
app.include_router(enrolments.router, prefix="/enrolments", tags=["enrolments"])
app.include_router(groups.router, prefix="/Groups", tags=["Groups"])
app.include_router(auth.router, prefix="/Auth", tags=["Auth"])

@app.on_event("startup")
def startup() -> None:
    init_database()

name_input = "TestName"
password_input = "123Password"

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
    if not hasattr(Students, "exists_by_id") or not hasattr(Students, "create_with_id"):
        raise HTTPException(status_code=500, detail="Student helper methods missing (exists_by_id/create_with_id)")
    if Students.exists_by_id(body.student_id):
        raise HTTPException(status_code=409, detail="Student ID already exists")

    pager_n, fax_n = generate_contact_numbers(str(body.student_id))

    new_id = Students.create_with_id(
        student_id=body.student_id,
        name=body.name,
        password=body.password,
        fax_n=fax_n,
        pager_n=pager_n,
        avatar_url=body.avatar_url or ""
    )

    row = Students.get_by_id(new_id)
    if row and "password" in row:
        del row["password"]
    return {"ok": True, "student": row}


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

