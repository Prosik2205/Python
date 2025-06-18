from pydantic import BaseModel
from fastapi import APIRouter, Request, Depends, Form, Query
from fastapi.responses import JSONResponse
from Controllers.controller_users import ControllerUser as CU
from Validators.Validator_response import Responce as resp
from datetime import date
from db import get_db_connection  
user = APIRouter(prefix="/users")

# @user.post("/post_signUp")
# async def signup(request: Request):
#     write_info = await request.json()
#     full_name, email, passwords = write_info.get("full_name"),write_info.get("email"),write_info.get("passwords")
#     CU.post_signUp(full_name, email, passwords)
#     return{"result":f"User{first_name}{second_name} has been added"}



@user.post("/register")
def register_user(
    full_name: str = Form(...),
    email: str = Form(...),
    passwords: str = Form(...),
    birthday: date = Form(...)

):
    return CU.register_user(
    full_name=full_name,
    email=email,
    passwords=passwords,
    birthday=birthday
)


@user.post("/verify-code")
def verify_code(
    email: str = Form(...),
    code: str = Form(...)
):
    return CU.verify_code(email, code)


@user.post("/complete-registration")
def complete_registration(
    email: str = Form(...),
    birthday: date  = Form(...)
):
    return CU.complete_registration(email, birthday)