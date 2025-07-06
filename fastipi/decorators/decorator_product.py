from functools import wraps
from fastapi import HTTPException
from db import get_db_connection  



def dec(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        db, cursor = None, None
        try:
            db, cursor = get_db_connection()
            result = func(*args, **kwargs, cursor=cursor, db=db,)
            db.commit()
            # print("Decorator works")
            return result
        except Exception as e:
            if db:
                db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {e}")
        finally:
            if db:
                db.close()
    return wrapper

    


