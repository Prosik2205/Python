from fastapi import FastAPI, Request, HTTPException
from registrator import Registrator
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import os 
from dotenv import load_dotenv

load_dotenv()
# Need add CORS
# Add з яких айпішок можна стукатися на цей сервер
# Додати дефолтні роути такі як ("/") і на помилки

class IPFilterMiddleware(BaseHTTPMiddleware):
    ALLOWED_IPS = os.getenv("trust_ip") 

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host  
        if client_ip not in self.ALLOWED_IPS:
            raise HTTPException(status_code=403, detail="Access denied from this IP address")
        response = await call_next(request)
        return response


class FastServ:
    def create_app(self):
        app = FastAPI()
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:8000"],  
            allow_credentials=True,
            allow_methods=["*"],  
            allow_headers=["*"],  
        )
   
        app.add_middleware(IPFilterMiddleware)
        
        regisst = Registrator(app)
        app = regisst.registrator_all()
        return app

app = FastServ().create_app()
