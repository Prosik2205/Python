from pydantic import BaseModel
from fastapi import APIRouter, Request, Depends, Form, Query
from fastapi.responses import JSONResponse
from Controllers.controller_users import ControllerUser as CU
from Validators.Validator_register import RegistorValidator 
from datetime import date
import requests
from db import get_db_connection  
RV = RegistorValidator()
user = APIRouter(prefix="/users")



@user.post("/register")
def register_user(full_name: str = Form(...), email: str = Form(...),passwords: str = Form(...),birthday: date = Form(...)):
    RV.validate_user(full_name,email,passwords,birthday)
    return CU.register_user(full_name=full_name,email=email,passwords=passwords,birthday=birthday)


@user.post("/verify-code")
def verify_code(email: str = Form(...),code: str = Form(...)):
    return CU.verify_code(email, code)


@user.post("/complete-registration")
def complete_registration(
    email: str = Form(...),
    birthday: date  = Form(...)
):
    return CU.complete_registration(email, birthday)