from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from dotenv import load_dotenv
from fastapi import HTTPException


class Mess:
    def __init__(self):
        load_dotenv()  
        self.api_key = os.getenv("SENDGRID_API_KEY")
        self.from_email = os.getenv("FROM_EMAIL")

    def send_verification_email(self, email, code):
        message = Mail(
            from_email=self.from_email,
            to_emails=email,
            subject="Verification Code",
            html_content=f"<strong>Your verification code is: {code}</strong>"
        )
        try:
            sg = SendGridAPIClient(self.api_key)
            sg.send(message)
            print(f"[SendGrid] Email sent to {email}")
        except Exception as e:
            print(f"[SendGrid ERROR] {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to send verification email")