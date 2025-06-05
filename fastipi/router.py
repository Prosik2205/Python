from pydantic import BaseModel
from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse
from controller import ControllerProducts as CP
from Validators.Validtor_product import ProductValidator
from Validators.Validator_response import Responce as resp
prod = APIRouter(prefix="/products")
pv = ProductValidator()


@prod.post("/post_products")
async def create_product(request: Request):
    product_data = await request.json()
    _id,_name,_price  = product_data.get("id"),product_data.get("name"),product_data.get("price")
    pv.validate_product(_id,_name,_price)
    CP.post_product(id = _id ,name = _name, price = _price)
    return {"result": f"Product {_name} has been added"}


@prod.get("/get_product")  
async def get_product(request: Request, product_id: int = Query(alias="product_id")):
    pv.validate_id(product_id)
    res_controller = CP.get_product(product_id)
    return(resp.res_get(res_controller))
    
    


@prod.put("/update_product")
async def update_product(request: Request,id:int = Query(alias="id")):
    body = await request.json()
    name,price = body.get("name"),body.get("price")
    pv.validate_product(id,name,price)
    result = CP.put_product(id,name,price)
    return {"result": result}


@prod.delete("/del_product")  
async def del_product(request: Request, product_id: int = Query(alias="product_id")):
    pv.validate_id(product_id)
    res_controller = CP.del_product(product_id)
    product_name = res_controller['name'] if isinstance(res_controller, dict) else res_controller[1]
    return {"result": f"Product: '{product_name}' has been delete"}
