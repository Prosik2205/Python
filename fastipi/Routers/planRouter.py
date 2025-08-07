from fastapi import APIRouter, Request, Query
from controllers.controller_plans import ControllerPlans as cp
from validators.validator_plan import PlanValidator
from validators.validator_response import Responce as resp

plan = APIRouter(prefix="/plan")
pv = PlanValidator()


@plan.post("/create_plan")
async def create_plan(request: Request):
    data = await request.json()
    name = data.get("name")
    description = data.get("description")
    pv.validate_name(name)
    res = cp.create_plan({"name": name, "description": description})
    return {"result": f"Plan '{name}' has been created"}


@plan.get("/get_plan")
async def get_plan(request: Request, plan_id: int = Query(alias="plan_id")):
    pv.validate_id(plan_id)
    res = cp.get_plan(plan_id)
    return resp.res_get(res)


@plan.get("/get_all_plans")
async def get_all_plans(request: Request):
    res = cp.get_all_plans()
    return resp.res_list(res)


@plan.put("/update_plan")
async def update_plan(request: Request, id: int = Query(alias="id")):
    data = await request.json()
    name = data.get("name")
    description = data.get("description")
    pv.validate_name(name)
    res = cp.update_plan(id, {"name": name, "description": description})
    return {"result": f"Plan '{name}' has been updated"}


@plan.delete("/delete_plan")
async def delete_plan(request: Request, plan_id: int = Query(alias="plan_id")):
    pv.validate_id(plan_id)
    res = cp.delete_plan(plan_id)
    plan_name = res['name'] if isinstance(res, dict) else res[1]
    return {"result": f"Plan '{plan_name}' has been deleted"}
