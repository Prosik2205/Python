
from pydantic import BaseModel
from fastapi import APIRouter
from controller import controller

prod = APIRouter()

class Product(BaseModel):
    id: int
    name: str
    price: float

@prod.post("/")
async def create_product(product: Product):
    controller.post_product(product)
    return {"result": f"Product{product.name} has add" }


@prod.get("/get/{product_id}")
async def get_product(product_id: int):
    return controller.get_product(product_id)


@prod.put("/put/{product_id}")
async def update_product(product_id: int, product: Product):
    controller.put_product(product_id, product)
    return {"result": f"Product {product.name} has been updated"}


@prod.delete("/delete/{product_id}")
async def delete_product(product_id: int):
    controller.del_product(product_id)
    return {"result": f"Product{product_id} has del" }
