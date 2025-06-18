import random
import string
import psycopg2  
from psycopg2.extras import RealDictCursor
from fastapi import HTTPException
from decorators.decorator_product import dec

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from dotenv import load_dotenv

load_dotenv()  
verification_codes = {}
temporary_users = {}

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")

def send_verification_email(email, code):
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=email,
        subject="Verification Code",
        html_content=f"<strong>Your verification code is: {code}</strong>"
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
        print(f"[SendGrid] Email sent to {email}")
    except Exception as e:
        print(f"[SendGrid ERROR] {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to send verification email")


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

        send_verification_email(email, code)
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
