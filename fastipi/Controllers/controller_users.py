import random
import string
from fastapi import HTTPException
from decorators.decorator_product import dec
from dotenv import load_dotenv
from utils.send_ver_mess import Mess as m
from datetime import datetime
from tokenise.coding import Tokeniz as t
from tokenise.hashing import Hash as h
load_dotenv()  

class ControllerUser:

    @staticmethod
    @dec
    def register_user(full_name, email, passwords, birthday, cursor=None, db=None):
        temporary_users = {}
        hashed_password = h.hash_password(passwords)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        base_result = cursor.fetchone()
        if base_result:
            raise HTTPException(status_code=400, detail="User already exists")

        code = ''.join(random.choices(string.digits, k=6))
        temporary_users = {
            "full_name": full_name,
            "email": email,
            "passwords": hashed_password,
            "birthday": birthday,
            "code": code
        }
        token = t().create_token(temporary_users)
        # print("Token:", token)

        m().send_verification_email(email, code)
        del temporary_users
        return {
            "message": "Verification code sent to your email",
            "toekn" : token
            }
        

    @staticmethod
    @dec
    def verify_code(code, token, cursor=None, db=None):
        expected_code = token.get("code")
        
        if not expected_code or expected_code != code:
            raise HTTPException(status_code=400, detail="Invalid or expired code")

        token.pop("code", None)
        token = t().create_token(token)

        return {
            "message": "Code verified. Please provide birthday.",
            "token": token
        }

    @staticmethod
    @dec
    def complete_registration(gender, phone_number,token,cursor=None, db=None):

        required_fields = ["full_name", "email", "passwords", "birthday"]
        if not all(field in token for field in required_fields):
            raise HTTPException(status_code=400, detail="Invalid token payload")
        #ось цю перевірку теж перемістити у Router
        
        try:
            cursor.execute(
                """
                INSERT INTO users (full_name, email, passwords, birthday, gender, phone_number)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    token["full_name"],
                    token["email"],
                    token["passwords"],
                    token["birthday"],
                    gender,
                    phone_number
                )
            )
            db.commit()
        except Exception as e:
            if db:
                db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

        token["gender"] = gender
        token["phone_number"] = phone_number
        new_token = t().create_token(token)

        return {
            "message": "User successfully registered",
            "token": new_token
        }


    @staticmethod
    @dec
    def login(email, password, cursor=None, db=None):
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="No user with this email found")


        if not h.check_password(password, user["passwords"]):  #  ПЕРЕВІРКА ХЕШУ
            raise HTTPException(status_code=401, detail="Incorrect password")

        login_time = datetime.now()

        try:
            cursor.execute(
                "UPDATE users SET last_login = %s WHERE email = %s",
                (login_time, email)
            )
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"[DB ERROR] Failed to update last_login: {e}")


        payload = {k: user[k] for k in ["id", "full_name", "email", "birthday", "gender", "phone_number"]}

        token = t().create_token(payload)

        return {
            "message": "Successful login",
            "user": {
                "id": user["id"],
                "full_name": user["full_name"],
                "email": user["email"],
                "last_login": login_time.strftime("%Y-%m-%d %H:%M:%S")
            },
            "token":token
        }


        
        