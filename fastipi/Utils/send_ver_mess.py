from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from dotenv import load_dotenv
from fastapi import HTTPException


load_dotenv()  

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