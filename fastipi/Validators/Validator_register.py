from fastapi import HTTPException
import re
from datetime import date

class RegistorValidator:
    def vaidate_name(self,name):
        pattern = r"^[А-ЯІЄЇҐ][а-яіїєґ’\-]+ [А-ЯІЄЇҐ][а-яіїєґ’\-]+ [А-ЯІЄЇҐ][а-яіїєґ’\-]+$"
        if not re.match(pattern, name):
            raise HTTPException(detail="Not valibale Full Name, must containe Ukraine letters(until)",status_code=400)
        
    def validate_email(self,email):
        pattern = r"\w+@\w+\.com$"
        if not re.match(pattern, email):
            raise HTTPException(detail="Not valibale Email",status_code=400)

    def validate_password(self,password):
        pattern = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$"
        if not re.match(pattern, password):
            raise HTTPException(detail="Not valibale Password, must contain at least 8 characters, at least 1 letter and 1 number",status_code=400)
        
    def validate_birthday(self, birthday):
        if not isinstance(birthday, date):
            raise HTTPException(status_code=400, detail="The date must be of type Date")

        if birthday > date.today():
            raise HTTPException(status_code=400, detail="The date cannot be in the future")

        if birthday.year < 1950:
            raise HTTPException(status_code=400, detail="Date of birth is too old")
        
    def validate_phone_number(self, phone_number):
       pattern = r'^\+380\d{9}$'
       if not re.match(pattern, phone_number):
           raise HTTPException(
               status_code=400,
               detail="Not valid phone number. Must start with +380 and contain exactly 12 digits"
           )

    def validate_gender(self, gender):
        valid_genders = {"male", "female", "other"}
        if gender.lower() not in valid_genders:
            raise HTTPException(
                status_code=400,
                detail="Not valid gender. Must be one of: 'male', 'female', 'other'"
            )


    def validate_user(self, name=None, email=None, password=None, birthday=None, phone_number=None, gender=None):
        if name is not None:
            self.vaidate_name(name)

        if email is not None:
            self.validate_email(email)

        if password is not None:
            self.validate_password(password)

        if birthday is not None:
            self.validate_birthday(birthday)

        if phone_number is not None:
            self.validate_phone_number(phone_number)
        
        if gender is not None:
            self.validate_gender(gender)
        
