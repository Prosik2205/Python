import json
import os
from datetime import datetime, timedelta, timezone, date
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError as InvalidTokenError
from dotenv import load_dotenv
import uuid


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
        #передавати в TOKEN_EXPIRE_MINUTES int
        self.TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRE_MINUTES", 30))

    def create_token(self, data: dict) -> str:
        payload = data.copy()

        # Додаємо час завершення дії токена
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.TOKEN_EXPIRE_MINUTES)
        payload["exp"] = int(expire.timestamp())

        # 🔐 Додаємо унікальний salt / jti
        payload["jti"] = uuid.uuid4().hex

        # Кодуємо payload
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






# token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmdWxsX25hbWUiOiJcdTA0MWZcdTA0MzVcdTA0NDBcdTA0MzVcdTA0MzJcdTA0NTZcdTA0NDBcdTA0M2FcdTA0MzAgXHUwNDEyXHUwNDQxXHUwNDRjXHUwNDNlXHUwNDMzXHUwNDNlIFx1MDQxN1x1MDQ0MFx1MDQzMFx1MDQzN1x1MDQ0MyIsImVtYWlsIjoiYmVpZ2Vzb3JlQG1lY2hhbmljc3BlZGlhLmNvbSIsInBhc3N3b3JkcyI6IiQyYiQxMiRuSEU4M1o0MXBTZjRzeExLbXZmVXh1WUlRdExLVS9pUGJpRXEvN1VscGpzMU1BakZJL2FnSyIsImJpcnRoZGF5IjoiMjAwMS0wMS0wMiIsImV4cCI6MTc1MzQ0OTYxMiwianRpIjoiNzdhZmEyYjhiYjQ1NGMxMGE4NWVjN2M4NzhhNDJkOTgifQ.HC5OuiVmy8PoZJ6vYvnQFrbTRFOzZei5wh_pj2VBOXg"

# decoded = Tokeniz().decodetoken(token)
# print("Decoded payload:", decoded)




# class Tokeniz:
#     def __init__(self):
#         load_dotenv()
#         self.SECRET_KEY = os.getenv("SECRET_KEY")
#         self.ALGORITHM = os.getenv("ALGORITHM")
#         self.TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRE_MINUTES", 30))

#     def create_token(self, data: dict) -> str:
#         payload = data.copy()

#         # Додаємо час завершення дії токена у форматі UNIX timestamp
#         expire = datetime.now(timezone.utc) + timedelta(minutes=self.TOKEN_EXPIRE_MINUTES)
#         payload["exp"] = int(expire.timestamp())

#         # Перетворення поля birthday у строку (ISO 8601), якщо воно є
#         if "birthday" in payload and isinstance(payload["birthday"], (datetime, date)):
#             payload["birthday"] = payload["birthday"].isoformat()

#         token = jwt.encode(payload, self.SECRET_KEY, algorithm=self.ALGORITHM)
#         return token

#     def decodetoken(self, token: str) -> dict:
#         try:
#             payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])

#             # Перетворення дати назад у формат datetime.date
#             if "birthday" in payload:
#                 try:
#                     payload["birthday"] = datetime.fromisoformat(payload["birthday"]).date()
#                 except Exception:
#                     print("[WARNING] Birthday parsing failed")

#             return payload

#         except ExpiredSignatureError:
#             raise Exception("Token has expired")
#         except InvalidTokenError:
#             raise Exception("Invalid token")