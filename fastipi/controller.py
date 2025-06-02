import psycopg2  
from psycopg2.extras import RealDictCursor
from fastapi import HTTPException
from db import get_db_connection  
#Create custom class Exeption|   HTTPException -> original Exeption.rest_exeption, і окрема функція Exeption.db_exeption коли стукаюсь до бази

class ControllerProducts:
    # CAN BE but better in all function do call
    # def __init__(self):
    #     self.conn = get_db_connection()  
    #     self.cur = self.conn.cursor()
    
    @staticmethod
    def post_product(id,name,price):
        sql = """
            INSERT INTO products (id, name, price) 
            VALUES (%s, %s, %s) 
            RETURNING *;
        """
        db = None  
        try:
            db = get_db_connection() #add 
            cursor = db.cursor() #add
            cursor.execute(sql, (id, name, price,))
            res = cursor.fetchone()
            db.commit()
        except psycopg2.IntegrityError:
            if db:
                db.rollback()
            raise HTTPException(status_code=400, detail="Product with this ID already exists")
        except Exception as e:
            if db:
                db.rollback()
            raise Exception(f"Problem with base {e}")
        finally:
            if db:
                db.close()
        
        return res
        
    @staticmethod
    def get_product(product_id):
        sql = "SELECT id, name, price::float AS price FROM products WHERE id = %s;"
        db = None
        try:
            db = get_db_connection()
            cursor = db.cursor()
            cursor.execute(sql, (product_id,))
            product = cursor.fetchone()
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")
            return product
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {e}")
        finally:
            if db:
                db.close()

    @staticmethod
    def put_product(product_id, product):
        sql = """
            UPDATE products SET name = %s, price = %s WHERE id = %s RETURNING *;
        """
        db = None
        try:
            db = get_db_connection()
            cursor = db.cursor()
            cursor.execute(sql, (product.name, product.price, product_id))
            updated_product = cursor.fetchone()
            db.commit()
            if not updated_product:
                raise HTTPException(status_code=404, detail="Product not found")
            return updated_product
        except Exception as e:
            if db:
                db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {e}")
        finally:
            if db:
                db.close()

    @staticmethod
    def del_product(product_id):
        sql = "DELETE FROM products WHERE id = %s RETURNING *;"
        db = None
        try:
            db = get_db_connection()
            cursor = db.cursor()
            cursor.execute(sql, (product_id,))
            deleted_product = cursor.fetchone()
            db.commit()
            if not deleted_product:
                raise HTTPException(status_code=404, detail="Product not found")
            return deleted_product
        except Exception as e:
            if db:
                db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {e}")
        finally:
            if db:
                db.close()





 # CAN BE but better in all function do call
    # def __init__(self):
    #     self.conn = get_db_connection()  
    #     self.cur = self.conn.cursor()
    
# @staticmethod
#     def post_product(self, product):
#         try:
#             self.cur.execute("INSERT INTO products (id, name, price) VALUES (%s, %s, %s) RETURNING *;", 
#                              (product.id, product.name, product.price))
#             self.conn.commit()
#         except psycopg2.IntegrityError:
#             self.conn.rollback()
#             raise HTTPException(status_code=400, detail="Product with this ID already exists")

# @staticmethod
#     def get_product(self, product_id):
#         self.cur.execute("SELECT * FROM products WHERE id = %s;", (product_id,))
#         product = self.cur.fetchone()
#         if not product:
#             raise HTTPException(status_code=404, detail="Product not found")
#         return product
    
#     @staticmethod
#     def put_product(self, product_id, product):
#         self.cur.execute("UPDATE products SET name = %s, price = %s WHERE id = %s RETURNING *;", 
#                          (product.name, product.price, product_id))
#         updated_product = self.cur.fetchone()
#         self.conn.commit()
#         if not updated_product:
#             raise HTTPException(status_code=404, detail="Product not found")
        
#     @staticmethod
#     def del_product(self, product_id):
#         self.cur.execute("DELETE FROM products WHERE id = %s RETURNING *;", (product_id,))
#         deleted_product = self.cur.fetchone()
#         self.conn.commit()
#         if not deleted_product:
#             raise HTTPException(status_code=404, detail="Product not found")
