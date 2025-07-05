import jwt
from datetime import datetime, timedelta, timezone
from jwt import ExpiredSignatureError, InvalidTokenError
import os
from dotenv import load_dotenv


class Tokeniz:

    def __init__(self):
        load_dotenv()
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ALGORITHM = os.getenv("ALGORITHM")
        self.TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRE_MINUTES", 30))

    def create_token(self, data: dict) -> str:
        payload = data.copy()
        now = datetime.now(timezone.utc) + timedelta(minutes=self.TOKEN_EXPIRE_MINUTES)
        payload["exp"] = now
        token = jwt.encode(payload, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token


    def decodetoken(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            return payload
        except ExpiredSignatureError:
            raise Exception("Token has expired")
        except InvalidTokenError:
            raise Exception("Invalid token")




# user_data = {
#     "id": 10,
#     "email": "test@example.com"
# }


# token = Tokeniz().create_token(user_data)
# print("JWT Token:", token)

# decoded = Tokeniz().decodetoken(token)
# print("Decoded payload:", decoded)