from fastapi import FastAPI, APIRouter

app = FastAPI()
router = APIRouter()

# creating new -> <table_name>.create(...), true or false return
# getting all -> <table_name>.get_all(), returns list of dictionaries
# update -> <table_name>.update(<attrs, must be all attrs but i will try to change it later)
# deleting -> <table_name>.delete(attr), returns bool

@router.get("/Students/", tags=["students"])
async def read_students():
    return Student.get_all() #Name str, Fax int, Pagor int, Previous Studies str, Enrolments Str, Photo 
    # return Student.get_all()

@router.get("/Login/", tags=["login"])
async def read_login():
    return None # Name str, Password str encrypted

@router.get("/Signup", tags=["signup"])
async def read_signup():
    return None # Name str, Password str, Fax str


@router.get("/Units/", tags=["units"])
async def read_units():
    return Units.get_all() #Name str, Code str, Description str
    # return 

@router.get("/Assessments/", tags=["assessments"])
async def read_assessments():
    return Assessments.get_all()# Group Limit int, Duration int, Grade int, Group Formation Week str

@router.get("/Groups/", tags=["groups"])
async def read_groups():
    return Groups.get_all() #Members str, Group Size int,  

@router.get("/Messages/", tags=["messages"])
async def read_messages(): 
    return Messages.get_all() # User Group str, Messages, str

@router.get("/Enrolment/", tags=["enrolment"])
async def read_enrolment():
    return Enrolment.get_all() # Grade str, availability str, complete boolean

@router.get("/Reviews/", tags=["reviews"])
async def read_reviews():
    return None #Do later 

@router.get("/Group Requests/", tags=["group_requests"])
async def read_group_requests():
    return Group_Requests.get_all() # Group str, User str

