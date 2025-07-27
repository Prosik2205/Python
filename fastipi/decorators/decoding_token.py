from fastapi import Request, HTTPException
from functools import wraps
from tokenise.coding import Tokeniz as t

def token_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Отримуємо Request з *args або kwargs        
        request: Request = kwargs.get("request")
        # Витягуємо та декодуємо токен
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authorization token is missing or invalid")
        token = token[7:]

        try:
            decoded_token = t().decodetoken(token)
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Token is invalid or expired")
        
        # Передаємо в основну функцію
        kwargs["token"] = decoded_token
        return await func(*args, **kwargs)

    return wrapper
