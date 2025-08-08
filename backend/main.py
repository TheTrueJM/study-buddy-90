from fastapi import FastAPI
from database import (
    initialize_database, Student, Units, Assessments,
    Groups, GroupMember, UnitEnrolment, GroupRequests
)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    initialize_database()

@app.get("/")
async def root():
    return {"message": "Hello World"}
