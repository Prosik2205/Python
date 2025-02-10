from fastapi import FastAPI
from registrator import Registrator

class FastServ:
    def create_app(self):
        app = FastAPI()
        regisst = Registrator(app)
        app = regisst.registrator_all()
        return app

app = FastServ().create_app()
