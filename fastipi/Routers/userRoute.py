from fastapi import APIRouter,  Request, Depends, HTTPException
from controllers.controller_users import ControllerUser as cu
from validators.validator_register import RegistorValidator as rv
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import date
from tokenise.coding import Tokeniz as t
from decorators.decoding_token import token_required
user = APIRouter(prefix="/users")
security = HTTPBearer()


#Зробити декодування токена через декоратор
#Добавити код для створеня sql таблиць і редагувати створенний

@user.post("/register")
# def register_user(full_name: str = Query(alias="full_name"), email: str = Query(alias="email"), passwords: str = Query(alias="passwords"),birthday: date = Query(alias="birthday")):
async def register_user(request: Request):
    user_data = await request.json()
    full_name,email,passwords,birthday = user_data.get("full_name"),user_data.get("email"),user_data.get("passwords"),user_data.get("birthday")
    birthday = date.fromisoformat(birthday)
    rv().validate_user(full_name,email,passwords,birthday)
    return cu.register_user(full_name=full_name,email=email,passwords=passwords,birthday=birthday)


@user.post("/verify-code")
@token_required
async def verify_code(request: Request, token: dict):


    data = await request.json()
    code = data.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Code is required")
    
    return cu.verify_code(code=code, token=token)



@user.post("/complete-registration")
@token_required
async def complete_registration(request: Request, token: dict):


    user_data = await request.json()
    gender = user_data.get("gender")
    phone_number = user_data.get("phone_number")

    rv().validate_gender(gender)
    rv().validate_phone_number(phone_number)

    return cu.complete_registration(gender = gender, phone_number = phone_number, token=token)



@user.post("/login")
async def login_user(request: Request):
    user_data = await request.json()
    email,passwords = user_data.get("email"),user_data.get("passwords")
    rv().validate_email(email)
    return cu.login(email, passwords)






