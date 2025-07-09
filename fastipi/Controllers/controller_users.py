import random
import string
from fastapi import HTTPException
from decorators.decorator_product import dec
from dotenv import load_dotenv
from Utils.send_ver_mess import Mess as m
from datetime import datetime
from Tokenise.coding import Tokeniz as t
load_dotenv()  
# це тоже не треба, цим займеть токен
# verification_codes = {}
# Зробити temporary_users не головну а тільки у register
# temporary_users = {}
#покищо без солей

class ControllerUser:

    @staticmethod
    @dec
    #без токена(на вході нема токена)
    def register_user(full_name, email, passwords, birthday, cursor=None, db=None):
        temporary_users = {}
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        base_result = cursor.fetchone()
        if base_result:
            raise HTTPException(status_code=400, detail="User already exists")

        code = ''.join(random.choices(string.digits, k=6))
        # verification_codes[email] = code
        temporary_users = {
            "full_name": full_name,
            "email": email,
            "passwords": passwords,
            "birthday": birthday,
            "code": code
        }
        #Закодувати  temporary_users в JWT
        token = t().create_token(temporary_users)
        print("Token:", token)

        m().send_verification_email(email, code)
        del temporary_users
        return {
            "message": "Verification code sent to your email",
            "toekn" : token
            }
        

    @staticmethod
    @dec
    #Приймати і розкодовувати токен(перевірити коди юзера і системи)
    def verify_code(code, token, cursor=None, db=None):
        decoded = t().decodetoken(token)
        expected_code = decoded.get("code")
        if not expected_code or expected_code != code:
            raise HTTPException(status_code=400, detail="Invalid or expired code")

        decoded.pop("code", None)
        token = t().create_token(decoded)

        return {
            "message": "Code verified. Please provide birthday.",
            "token": token
        }

    @staticmethod
    @dec
    #на вхід йде токен з verify_code
    #в complete_registration приймати дод. інформацію(gender, phone)
    def complete_registration(gender, phone_number,token,cursor=None, db=None):

        decoded = t().decodetoken(token)
        
        required_fields = ["full_name", "email", "passwords", "birthday"]
        
        if not all(field in decoded for field in required_fields):
            raise HTTPException(status_code=400, detail="Invalid token payload")
        
        try:
            cursor.execute(
                """
                INSERT INTO users (full_name, email, passwords, birthday, gender, phone_number)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    decoded["full_name"],
                    decoded["email"],
                    decoded["passwords"],
                    decoded["birthday"],
                    gender,
                    phone_number
                )
            )
            db.commit()
        except Exception as e:
            if db:
                db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

        decoded["gender"] = gender
        decoded["phone_number"] = phone_number
        new_token = t().create_token(decoded)

        return {
            "message": "User successfully registered",
            "token": new_token
        }


    @staticmethod
    @dec
    # Токен не приймається
    def login(email, password, cursor=None, db=None):
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="No user with this email found")

        if user["passwords"] != password:
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

        #повертати не меседж а токен з його даним з бази(згенерувати)
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


        
        