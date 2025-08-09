from fastapi import FastAPI, APIRouter

app = FastAPI()
router = APIRouter()

@router.get("/Students/", tags=["students"])
async def read_users():
    return None #Name str, Fax int, Pagor int, Previous Studies str, Photo 

@router.get("/Units/", tags=["units"])
async def read_users():
    return None #Name str, Code str, Description str

@router.get("/Assessments/", tags=["assessments"])
async def read_users():
    return None # Group Limit int, Duration int, Grade int, Group Formation Week str

@router.get("/Groups/", tags=["groups"])
async def read_users():
    return None #Members str, Group Size int,  

@router.get("/Messages/", tags=["messages"])
async def read_users(): 
    return None # User Group str, Messages, str

@router.get("/Enrolment/", tags=["enrolment"])
async def read_users():
    return None # Grade str, availability str, complete boolean

@router.get("/Reviews/", tags=["reviews"])
async def read_users():
    return None #Do later 

@router.get("/Group Requests/", tags=["group requests"])
async def read_users():
    return None # Group str, User str

