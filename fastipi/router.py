from pydantic import BaseModel
from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse
from controller import ControllerProducts as CP
#Params методи передавються на get i delete == id:int = Query(alias="id")):
#Добавити файл Validator_product для валідації даних які приймаються, наприклад чи price = float
from Validtor_product import ProductValidator as pv

prod = APIRouter(prefix="/products")



@prod.post("/post_products")
async def create_product(request: Request):
    product_data = await request.json()

    # Отримаємо окремі значення для продукту
    _id,_name,_price  = product_data.get("id"),product_data.get("name"),product_data.get("price")
    # Викликаємо метод для додавання продукту
    CP.post_product(id = _id ,name= _name, price= _price)
       
    return {"result": f"Product {_name} has been added"}


@prod.get("/get_product")  # шлях без параметрів в URL
async def get_product(request: Request, product_id: int = Query(alias="product_id")):
    res_controller = CP.get_product(product_id)
    
    # Перевіряємо тип відповіді res_controller і повертаємо відповідь
    if isinstance(res_controller, str):
        return JSONResponse(content={"product str": res_controller}, status_code=200)
    elif isinstance(res_controller, list):
        return JSONResponse(content={"product list": res_controller}, status_code=200)
    elif isinstance(res_controller, dict):
        return JSONResponse(content={"product dict":res_controller}, status_code=200)
    else:
        return JSONResponse(content={"error": "Invalid response format"}, status_code=400)



@prod.put("/update_product")
async def update_product(request: Request,id:int = Query(alias="id")):
    body = await request.json()
    name,price = body.get("name"),body.get("price")
    result = CP.put_product(id,name,price)
    return {"result": result}

@prod.delete("/del_product")  # шлях без параметрів в URL
async def del_product(request: Request, product_id: int = Query(alias="product_id")):
    res_controller = CP.del_product(product_id)#переправити для кращого виводу повідомлення
    return {"result": f"Product has been delete"}
