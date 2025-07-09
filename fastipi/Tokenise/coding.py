import jwt
import json
import os
from datetime import datetime, timedelta, timezone, date
from jwt import ExpiredSignatureError, InvalidTokenError
from dotenv import load_dotenv

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)


class Tokeniz:

    def __init__(self):
        load_dotenv()
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ALGORITHM = os.getenv("ALGORITHM")
        self.TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRE_MINUTES", 30))

    def create_token(self, data: dict) -> str:
        payload = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.TOKEN_EXPIRE_MINUTES)
        payload["exp"] = int(expire.timestamp()) 

        encoded_payload = json.loads(json.dumps(payload, cls=CustomEncoder))

        token = jwt.encode(encoded_payload, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token


    def decodetoken(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])

            
            if "birthday" in payload:
                birthday_str = payload["birthday"]
                payload["birthday"] = datetime.fromisoformat(birthday_str).date()
            else:
                print("SMTH WRONG WITH DECODING DATE")
                

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

# token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NywiZnVsbF9uYW1lIjoiXHUwNDFmXHUwNDM1XHUwNDQwXHUwNDM1XHUwNDMyXHUwNDU2XHUwNDQwXHUwNDNhXHUwNDMwIFx1MDQyMlx1MDQzZVx1MDQzYVx1MDQzNVx1MDQzZFx1MDQzMCBcdTA0MTRcdTA0NTZcdTA0M2JcdTA0M2UiLCJlbWFpbCI6IjM4MzZzY2FybGV0QHB1bmtwcm9vZi5jb20iLCJiaXJ0aGRheSI6IjIwMDEtMDEtMDIiLCJnZW5kZXIiOiJtYWxlIiwicGhvbmVfbnVtYmVyIjoiKzM4MDY2MDgxMjQyMiIsImV4cCI6MTc1MjA2NDczMn0.L82vSZQ7sztnNI5wmYsMh7bznUutDq9CrRJ5a-qZZpo"

# decoded = Tokeniz().decodetoken(token)
# print("Decoded payload:", decoded)