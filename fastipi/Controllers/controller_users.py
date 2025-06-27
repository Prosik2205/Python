import random
import string
from fastapi import HTTPException
from decorators.decorator_product import dec
from dotenv import load_dotenv
from Utils.send_ver_mess import send_verification_email as sve

load_dotenv()  
verification_codes = {}
temporary_users = {}

class ControllerUser:

    @staticmethod
    @dec
    def register_user(full_name, email, passwords, birthday, cursor=None, db=None):
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="User already exists")

        code = ''.join(random.choices(string.digits, k=6))
        verification_codes[email] = code
        temporary_users[email] = {
            "full_name": full_name,
            "email": email,
            "passwords": passwords,
            "birthday": birthday
        }

        sve(email, code)
        return {"message": "Verification code sent to your email"}

    @staticmethod
    @dec
    def verify_code(email, code, cursor=None, db=None):
        expected_code = verification_codes.get(email)
        if not expected_code or expected_code != code:
            raise HTTPException(status_code=400, detail="Invalid or expired code")
        return {"message": "Code verified. Please provide birthday."}

    @staticmethod
    @dec
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

        return {"message": "User successfully registered"}
