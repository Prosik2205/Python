from fastapi import APIRouter,  Request, Depends, HTTPException
from Controllers.controller_users import ControllerUser as cu
from Validators.Validator_register import RegistorValidator as rv
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import date
user = APIRouter(prefix="/users")
security = HTTPBearer()


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

    token = request.headers.get("Authorization")
    #Цю перевірку можна зробити в окремому файлі і т.д.    
    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization token is missing or invalid")        
    token = token[7:]
    #decoded = t().decodetoken(token)
    data = await request.json()
    code = data.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Code is required")
    
    return cu.verify_code(code=code, token=token)



#Токен приймається з Request з Headers,  не робити через HTTPAuthorizationCredentials і token.credentials
@user.post("/complete-registration")
async def complete_registration(request: Request):
    token = request.headers.get("Authorization")

    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization token is missing or invalid")  
    
    token = token[7:]
    #decoded = t().decodetoken(token)

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








# #Токен приймається з Request з Headers,  не робити через HTTPAuthorizationCredentials і token.credentials\
# @user.post("/verify-code")
# async def verify_code(request: Request, token: HTTPAuthorizationCredentials = Depends(security)):
#     #зарзу після : прийом і обробка токена
#     #token = request.headers.get("Authorization")
#     #token = token[7:](Забираємо перші 7 символів , бо там буде інше пердаватись)
#     #decoded = t().decodetoken(token)
#     data = await request.json()
#     code = data.get("code")

#     if not code:
#         raise HTTPException(status_code=400, detail="Code is required")

#     return cu.verify_code(code=code, token=token.credentials)