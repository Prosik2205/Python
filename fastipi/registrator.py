from routers.router import prod
from routers.userRoute import user
from routers.planRouter import plan

class Registrator:
    def __init__(self,app):
        self.app = app
    
    def registrator_all(self):
        self.app.include_router(user)
        self.app.include_router(prod)
        self.app.include_router(plan)
        return self.app