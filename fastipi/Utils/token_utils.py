from fastapi import Request, HTTPException
from tokenise.coding import Tokeniz as t


def extract_and_decode_token(request: Request):
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization token is missing or invalid")
    token = token[7:]
    return t().decodetoken(token)