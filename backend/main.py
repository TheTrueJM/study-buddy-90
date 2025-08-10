from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5174",
        "http://localhost:3000",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup() -> None:
    init_database()

#database test
@app.get("/test-db")
def test_db():
    from database.connection import execute_query
    try:
        result = execute_query("SELECT name FROM sqlite_master WHERE type='table';", ())
        return {"tables": [row[0] for row in result]}
    except Exception as e:
        raise HTTPException(500, f"DB Error: {e}")

