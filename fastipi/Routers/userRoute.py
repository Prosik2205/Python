from fastapi import APIRouter, Query, Request
from Controllers.controller_users import ControllerUser as cu
from Validators.Validator_register import RegistorValidator as rv
from datetime import date
user = APIRouter(prefix="/users")


@user.post("/register")
# def register_user(full_name: str = Query(alias="full_name"), email: str = Query(alias="email"), passwords: str = Query(alias="passwords"),birthday: date = Query(alias="birthday")):
async def register_user(request: Request):
    user_data = await request.json()
    full_name,email,passwords,birthday = user_data.get("full_name"),user_data.get("email"),user_data.get("passwords"),user_data.get("birthday")
    birthday = date.fromisoformat(birthday)
    rv().validate_user(full_name,email,passwords,birthday)
    return cu.register_user(full_name=full_name,email=email,passwords=passwords,birthday=birthday)


@user.post("/verify-code")
async def verify_code(request: Request):
    user_data = await request.json()
    email,code = user_data.get("email"),user_data.get("code")
    return cu.verify_code(email, code)


@user.post("/complete-registration")
async def complete_registration(request: Request):
    user_data = await request.json()
    email,birthday = user_data.get("email"),user_data.get("birthday")
    birthday = date.fromisoformat(birthday)
    return cu.complete_registration(email, birthday)



@user.post("/login")
async def login_user(request: Request):
    user_data = await request.json()
    email,passwords = user_data.get("email"),user_data.get("passwords")
    rv().validate_email(email)
    return cu.login(email, passwords)