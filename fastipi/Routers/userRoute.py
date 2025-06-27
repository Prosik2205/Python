from fastapi import APIRouter, Request, Depends, Form, Query
from Controllers.controller_users import ControllerUser as cu
from Validators.Validator_register import Registorvalidator 
from datetime import date
rv = Registorvalidator()
user = APIRouter(prefix="/users")



@user.post("/register")
def register_user(full_name: str = Form(...), email: str = Form(...),passwords: str = Form(...),birthday: date = Form(...)):
    rv.validate_user(full_name,email,passwords,birthday)
    return cu.register_user(full_name=full_name,email=email,passwords=passwords,birthday=birthday)


@user.post("/verify-code")
def verify_code(email: str = Form(...),code: str = Form(...)):
    return cu.verify_code(email, code)


@user.post("/complete-registration")
def complete_registration(
    email: str = Form(...),
    birthday: date  = Form(...)
):
    return cu.complete_registration(email, birthday)