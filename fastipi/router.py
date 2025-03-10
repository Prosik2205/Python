from pydantic import BaseModel
from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse
from controller import ControllerProducts as CP
#Params методи передавються на get i delete
#Добавити файл Valifator_product для валідації даних які приймаються, наприклад чи price = float


prod = APIRouter(prefix="/products")

# Remove this  
# class Product(BaseModel):
#     id: int
#     name: str
#     price: float

@prod.post("/post_products")
async def create_product(request: Request):
    #product_data = body
    product_data = await request.json()
    
    # Отримаємо окремі значення для продукту
    _id = product_data.get("id")
    _name = product_data.get("name")
    _price = product_data.get("price")
    
    # Викликаємо метод для додавання продукту
    CP.post_product(id = _id ,name= _name, price= _price)
    
    return {"result": f"Product {_name} has been added"}





# Must look like @prod.get("/<some_name>")
# REMOVE  {product_id}
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
# @prod.get("/get/{product_id}")
# async def get_product(product_id: int):
#     return CP.get_product(product_id)




@prod.get("/get_product")  # шлях без параметрів в URL
async def get_product(request: Request, product_id: int = Query(alias="product_id")):
    res_controller = CP.get_product(product_id)
    
    # Перевіряємо тип відповіді res_controller і повертаємо відповідь
    if isinstance(res_controller, str):
        return JSONResponse(content={"product": res_controller}, status_code=200)
    elif isinstance(res_controller, list):
        return JSONResponse(content={"product": res_controller}, status_code=200)
    elif isinstance(res_controller, dict):
        return JSONResponse(content=res_controller, status_code=200)
    else:
        return JSONResponse(content={"error": "Invalid response format"}, status_code=400)














# WRONG must look like
# @prod.put("/udpate_product")
# async def update_product(request: Request)
#       body = await request.get() or json.get()
#       id, name, price = body.get("id"),body.get("name"),body.get("price")
#       result = controller.put_product(id,name,price)
#       return JSONResponse(content={"result":result}, status_code = 200)
       

# @prod.put("/put/{product_id}")
# async def update_product(product_id: int, product: Product):
#     CP.put_product(product_id, product)
#     return {"result": f"Product {product.name} has been updated"}

# # SAME LIKE FOR put method
# @prod.delete("/delete/{product_id}")
# async def delete_product(product_id: int):
#     CP.del_product(product_id)
#     return {"result": f"Product{product_id} has del" }




# @prod.post("/")
# async def create_product(product: Product):
#     CP.post_product(product)
#     return {"result": f"Product{product.name} has add" }

# @prod.get("/get/{product_id}")
# async def get_product(product_id: int):
#     return CP.get_product(product_id)