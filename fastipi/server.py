from fastapi import FastAPI, Request, HTTPException
from registrator import Registrator
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import os 
from dotenv import load_dotenv

load_dotenv()
# Додати дефолтні роути такі як ("/") і на помилки

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
        regisst = Registrator(app)
        app = regisst.registrator_all()

        @app.get("/")
        async def root():
            return ("Welcome to the HELL")
        

        return app

app = FastServ().create_app()
