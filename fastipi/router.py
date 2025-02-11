
from pydantic import BaseModel
from fastapi import APIRouter
from controller import controller
# IMPORT MUST BE LIKE from controller import ControllerProducts 
# Add prefix for thir route
prod = APIRouter()

# Remove this bullshit 
class Product(BaseModel):
    id: int
    name: str
    price: float

@prod.post("/")
async def create_product(product: Product):
    controller.post_product(product)
    return {"result": f"Product{product.name} has add" }

# Must look like @prod.get("/<some_name>")
# REMOVE FUCKING {product_id}
# WRONG GET METHOD WRITE ONLY LIKE
# @prod.get("/get_product>") 
# async def get_product (request: Request, product_id:int = Query(alias="product_id")
# res_controller = ControllerProducts.get_product(product_id)
# res_controller can be "Just stirng" or ["asdjl","halkdsjf"] or 
# {
# "product":"<some_name_for_example>",
#  "product_id":<some_id>
#}
# return JSONResponse(content={"product":res_controller},status_code = 200) 
@prod.get("/get/{product_id}")
async def get_product(product_id: int):
    return controller.get_product(product_id)

# WRONG must look like
# @prod.put("/udpate_product")
# async def update_product(request: Request)
#       body = await request.get() or json.get()
#       id, name, price = body.get("id"),body.get("name"),body.get("price")
#       result = controller.put_product(id,name,price)
#       return JSONResponse(content={"result":result}, status_code = 200)
       

@prod.put("/put/{product_id}")
async def update_product(product_id: int, product: Product):
    controller.put_product(product_id, product)
    return {"result": f"Product {product.name} has been updated"}

# SAME LIKE FOR put method
@prod.delete("/delete/{product_id}")
async def delete_product(product_id: int):
    controller.del_product(product_id)
    return {"result": f"Product{product_id} has del" }
