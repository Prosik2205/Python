from fastapi import HTTPException

class ProductValidator:
    def validate_id(self,id):
        if not isinstance(id,int):
            raise HTTPException(detail="ID must be integer type",status_code=400)
        
    def validate_name(self,name):
        pass

    def validate_price(self,price):
        pass

    def validate_product(self,id=None,name=None,price=None):
        if id is not None:
            self.validate_id(id)

        if name is not None:
            self.validate_name(name)

        if price is not None:
            self.validate_price(price)