from Routers.router import prod
from Routers.userRoute import user

class Registrator:
    def __init__(self,app):
        self.app = app
    
    def registrator_all(self):
        self.app.include_router(user)
        self.app.include_router(prod)
        return self.app