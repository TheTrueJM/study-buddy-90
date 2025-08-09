from fastapi import FastAPI, APIRouter

app = FastAPI()
router = APIRouter()

@router.get("/Students/", tags=["students"])
async def read_users():
    return None #Name str, Fax int, Pagor int, Previous Studies str, Enrolments Str, Photo 

@router.get("/Login/", tags=["login"])
async def read_login():
    return None # Name str, Password str encrypted

@router.get("/Signup", tags=["signup"])
async def read_signup():
    return None # Name str, Password str, Fax str


@router.get("/Units/", tags=["units"])
async def read_units():
    return None #Name str, Code str, Description str

@router.get("/Assessments/", tags=["assessments"])
async def read_assessments():
    return None # Group Limit int, Duration int, Grade int, Group Formation Week str

@router.get("/Groups/", tags=["groups"])
async def read_groups():
    return None #Members str, Group Size int,  

@router.get("/Messages/", tags=["messages"])
async def read_messages(): 
    return None # User Group str, Messages, str

@router.get("/Enrolment/", tags=["enrolment"])
async def read_enrolment():
    return None # Grade str, availability str, complete boolean

@router.get("/Reviews/", tags=["reviews"])
async def read_reviews():
    return None #Do later 

@router.get("/Group Requests/", tags=["group_requests"])
async def read_group_requests():
    return None # Group str, User str

