from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional

from database.schema import init_database
from routers import students, units, enrolments, groups, auth

app = FastAPI(title="Study Mates API")

app.include_router(students.router, prefix="/students", tags=["students"])
app.include_router(units.router, prefix="/units", tags=["units"])
app.include_router(enrolments.router, prefix="/enrolments", tags=["enrolments"])
app.include_router(groups.router, prefix="/Groups", tags=["Groups"])
app.include_router(auth.router, prefix="/Auth", tags=["Auth"])

@app.on_event("startup")
def startup() -> None:
    init_database()

name_input = "TestName"
password_input = "123Password"

# @app.post("/login")
# def login():
#     if False: 
#         raise Exception("Authentication Failed.")
#     return {
#         "success": verify_credentials(name_input, password_input)
#     }

# class SignUpBody(BaseModel):
#     student_id: int
#     name: str
#     password: str
#     avatar_url: Optional[str] = ""

# @app.post("/auth/signup", tags=["auth"])
# def signup(body: SignUpBody):
#     if not hasattr(Students, "exists_by_id") or not hasattr(Students, "create_with_id"):
#         raise HTTPException(status_code=500, detail="Student helper methods missing (exists_by_id/create_with_id)")
#     if Students.exists_by_id(body.student_id):
#         raise HTTPException(status_code=409, detail="Student ID already exists")

#     pager_n, fax_n = generate_contact_numbers(str(body.student_id))

#     new_id = Students.create_with_id(
#         student_id=body.student_id,
#         name=body.name,
#         password=body.password,
#         fax_n=fax_n,
#         pager_n=pager_n,
#         avatar_url=body.avatar_url or ""
#     )

#     row = Students.get_by_id(new_id)
#     if row and "password" in row:
#         del row["password"]
#     return {"ok": True, "student": row}


#database test
@app.get("/test-db")
def test_db():
    from database.connection import execute_query
    try:
        result = execute_query("SELECT name FROM sqlite_master WHERE type='table';", ())
        return {"tables": [row[0] for row in result]}
    except Exception as e:
        raise HTTPException(500, f"DB Error: {e}")

