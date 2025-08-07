from fastapi import HTTPException


class PlanValidator:
    def validate_id(self, id):
        if not isinstance(id, int) or id <= 0:
            raise HTTPException(status_code=400, detail="Invalid plan ID")

    def validate_name(self, name):
        if not name or not isinstance(name, str):
            raise HTTPException(status_code=400, detail="Invalid plan name")
