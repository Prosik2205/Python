import random
import string
from fastapi import HTTPException
from decorators.decorator_product import dec
from dotenv import load_dotenv
from Utils.send_ver_mess import Mess as m
from datetime import datetime
from token.coding import Tokeniz as t#Переіменувати token в шось інше
load_dotenv()  
# це тоже не треба, цим займеть токен
verification_codes = {}
# Зробити temporary_users не головну а тільки у register
temporary_users = {}
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
        temporary_users[email] = {
            "full_name": full_name,
            "email": email,
            "passwords": passwords,
            "birthday": birthday,
            "code": code
        }
        #Закодувати  temporary_users в JWT
        token = t().create_token(temporary_users)

        # token = jwt.encode(temporary_users)
        # sve(email, code)
        # # return {"message": "Verification code sent to your email"}
        # return token
        # delete temporary_users

        m().send_verification_email(email, code)
        return token
        return {"message": "Verification code sent to your email"}
        

    @staticmethod
    @dec
    #Приймати і розкодовувати токен(перевірити коди юзера і системи)
    def verify_code(email, code, token ,cursor=None, db=None):
        # expected_code = verification_codes.get(email)
        expected_code = token.get(code)
        if not expected_code or expected_code != code:
            raise HTTPException(status_code=400, detail="Invalid or expired code")
        return {"message": "Code verified. Please provide birthday."}
        #перегенерувати токен без кода
        # return token

    @staticmethod
    @dec
    #на вхід йде токен з verify_code
    #в complete_registration приймати дод. інформацію(sex, phone)
    def complete_registration(email, birthday, cursor=None, db=None):
        user_data = temporary_users.get(email)
        if not user_data:
            raise HTTPException(status_code=400, detail="No user data found. Please register first.")
        
        if user_data["birthday"] != birthday:
            raise HTTPException(status_code=400, detail="Birthday does not match")
        
        try:
            cursor.execute(
                "INSERT INTO users (full_name, email, passwords, birthday) VALUES (%s, %s, %s, %s)",
                (user_data["full_name"], email, user_data["passwords"], birthday)
            )
            db.commit()
        except Exception as e:
            if db:
                db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

        del verification_codes[email]
        del temporary_users[email]
        #повертати токен з новими даними юзера і перезаписати токен

        return {"message": "User successfully registered"}


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

        #повертати не меседж а токен з його даним з бази(згенерувати)
        return {
            "message": "Successful login",
            "user": {
                "id": user["id"],
                "full_name": user["full_name"],
                "email": user["email"],
                "last_login": login_time.strftime("%Y-%m-%d %H:%M:%S")
            }
        }


        
        