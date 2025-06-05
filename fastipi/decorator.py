from functools import wraps
from fastapi import HTTPException
from db import get_db_connection  



def post_dec(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        db, cursor = None, None
        try:
            db, cursor = get_db_connection()
            result = func(*args, cursor=cursor, db=db, **kwargs)
            db.commit()
            return result
        except Exception as e:
            if db:
                db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {e}")
        finally:
            if db:
                db.close()
    return wrapper

    


