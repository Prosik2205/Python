from fastapi import HTTPException
from decorators.decorator_product import connecting
import psycopg2


class ControllerPlans:

    @staticmethod
    @connecting
    def create_plan(data, cursor=None, db=None):
        name = data.get("name")
        description = data.get("description")

        if not name:
            raise HTTPException(status_code=400, detail="Name is required")

        sql = """
            INSERT INTO plan (name, description)
            VALUES (%s, %s)
            RETURNING *;
        """
        try:
            cursor.execute(sql, (name, description))
            created_plan = cursor.fetchone()
        except psycopg2.IntegrityError:
            if db:
                db.rollback()
            raise HTTPException(status_code=400, detail="Plan with this name already exists")
        
        return created_plan

    @staticmethod
    @connecting
    def get_all_plans(cursor=None, db=None):
        sql = "SELECT id, name, description FROM plan;"
        cursor.execute(sql)
        return cursor.fetchall()

    @staticmethod
    @connecting
    def get_plan(plan_id, cursor=None, db=None):
        sql = "SELECT id, name, description FROM plan WHERE id = %s;"
        cursor.execute(sql, (plan_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Plan not found")
        return result

    @staticmethod
    @connecting
    def update_plan(plan_id, data, cursor=None, db=None):
        name = data.get("name")
        description = data.get("description")

        sql = """
            UPDATE plan SET name = %s, description = %s
            WHERE id = %s
            RETURNING *;
        """
        cursor.execute(sql, (name, description, plan_id))
        updated_plan = cursor.fetchone()
        if not updated_plan:
            raise HTTPException(status_code=404, detail="Plan not found")
        return updated_plan

    @staticmethod
    @connecting
    def delete_plan(plan_id, cursor=None, db=None):
        sql = "DELETE FROM plan WHERE id = %s RETURNING *;"
        cursor.execute(sql, (plan_id,))
        deleted_plan = cursor.fetchone()
        if not deleted_plan:
            raise HTTPException(status_code=404, detail="Plan not found")
        return deleted_plan
