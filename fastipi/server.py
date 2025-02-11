from fastapi import FastAPI
from registrator import Registrator

# Need add CORS
# Add з яких айпішок можна стукатися на цей сервер
# Додати дефолтні роути такі як ("/") і на помилки
class FastServ:
    def create_app(self):
        app = FastAPI()
        regisst = Registrator(app)
        app = regisst.registrator_all()
        return app

app = FastServ().create_app()
