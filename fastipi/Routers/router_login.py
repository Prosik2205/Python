from pydantic import BaseModel
from fastapi import APIRouter, Request, Depends, Form, Query
from fastapi.responses import JSONResponse
from Controllers.controller_users import ControllerUser as CU
from Validators.Validator_response import Responce as resp
user = APIRouter(prefix="/users")

# @user.post("/post_signUp")
# async def signup(request: Request):
#     write_info = await request.json()
#     first_name, second_name, father_name, email, password = write_info.get("first_name"),write_info.get("second_name"),write_info.get("father_name"),write_info.get("email"),write_info.get("password")
#     CU.post_signUp(first_name, second_name, father_name, email, password)
#     return{"result":f"User{first_name}{second_name} has been added"}



@user.post("/register")

def register_user(
    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    cursor=None, db=None
):
    return CU.register_user(full_name, email, password, cursor, db)


@user.post("/verify-code")
def verify_email_code(email: str = Form(...), code: str = Form(...)):
    return CU.verify_code(email, code)


@user.post("/complete-registration")
def complete_registration(
    email: str = Form(...),
    birthday: str = Form(...),
    cursor=None, db=None
):
    return CU.complete_registration(email, birthday, cursor, db)