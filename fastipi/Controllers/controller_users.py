import random
import string
import psycopg2  
from psycopg2.extras import RealDictCursor
from fastapi import HTTPException
from decorators.decorator_product import dec

verification_codes = {}

class ControllerUser:

    # @staticmethod
    # @dec
    # def post_signUp(full_name, email, password, cursor=None, db=None):
    #     sql = """
    #         INSERT INTO products (full_name, email, password) 
    #         VALUES (%s, %s, %s, %s, %s) 
    #         RETURNING *;
    #     """
    #     try:
    #         cursor.execute(sql,(full_name, email, password))
    #         res = cursor.fetchone()
    #     except psycopg2.IntegrityError:
    #         if db:
    #             db.rollback()
    #         raise HTTPException(status_code=400, detail="User has been created with this email")
    #     return res   
    # 
    @staticmethod
    @dec
    def register_user(full_name, email, password, cursor=None, db=None):

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="User already exists")

        # Зберігаємо тимчасово
        code = ''.join(random.choices(string.digits, k=6))
        verification_codes[email] = code

        print(f"Verification code for {email}: {code}")

        return {"message": "Verification code sent to your email"} 
    
    @staticmethod
    @dec
    def verify_code(email, code):
        real_code = verification_codes.get(email)
        if not real_code or real_code != code:
            raise HTTPException(status_code=400, detail="Invalid or expired verification code")

        return {"message": "Email verified successfully"}
    

    @staticmethod
    @dec
    def complete_registration(email, birthday, cursor=None, db=None):
        cursor.execute("UPDATE users SET birthday = %s WHERE email = %s RETURNING *", (birthday, email))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return {"message": "Registration completed", "user": user}
