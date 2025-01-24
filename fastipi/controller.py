from fastapi import HTTPException

class ControllerProducts:
    def __init__(self):
        self.products = {}

    def post_product(self,product):
        if self._is_product(product.id):
            raise HTTPException(status_code=400, detail="You have this product")
        self.products[product.id] = product

    def get_product(self, product_id):
        if not self._is_product(product_id):
            raise HTTPException(status_code=404, detail="Product not found") 
        return self.products[product_id]

    def put_product(self, product_id, product):
        if not self._is_product(product_id):
            raise HTTPException(status_code=404, detail="Product not found")
        self.products[product_id] = product       
    
    
    def del_product(self, product_id):
        if not self._is_product(product_id):
            raise HTTPException(status_code=404, detail="Product not found")
        del self.products[product_id]
    
    def _is_product(self, product_id):
        return product_id in self.products





controller = ControllerProducts()