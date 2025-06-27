import psycopg2  
from fastapi import HTTPException
from decorators.decorator_product import dec

class ControllerProducts:    

    @staticmethod
    @dec
    def post_product(id, name, price, cursor=None, db=None):
        sql = """
            INSERT INTO products (id, name, price) 
            VALUES (%s, %s, %s) 
            RETURNING *;
        """
        try:
            cursor.execute(sql, (id, name, price))
            res = cursor.fetchone()
        except psycopg2.IntegrityError:
            if db:
                db.rollback()
            raise HTTPException(status_code=400, detail="Product with this ID already exists")
        return res

        
    @staticmethod
    @dec
    def get_product(product_id, cursor=None, db=None):
        sql = "SELECT id, name, price::float AS price FROM products WHERE id = %s;"
        cursor.execute(sql, (product_id,))
        product = cursor.fetchone()
        if not product:
                raise HTTPException(status_code=404, detail="Product not found")
        return product
       

    @staticmethod
    @dec
    def put_product(product_id,_name,_price, cursor=None, db=None):
        sql = """
            UPDATE products SET name = %s, price = %s WHERE id = %s RETURNING *;
        """
        cursor.execute(sql, (_name, _price, product_id,))
        updated_product = cursor.fetchone()
        if not updated_product:
                raise HTTPException(status_code=404, detail="Product not found")
        return updated_product


    @staticmethod
    @dec
    def del_product(product_id, cursor=None, db=None):
        sql = "DELETE FROM products WHERE id = %s RETURNING *;"
        cursor.execute(sql, (product_id,))
        deleted_product = cursor.fetchone()
        if not deleted_product:
                raise HTTPException(status_code=404, detail="Product not found")
        return deleted_product
        






    
# @staticmethod
#     def post_product(self, product):
#         try:
#             self.cur.execute("INSERT INTO products (id, name, price) VALUES (%s, %s, %s) RETURNING *;", 
#                              (product.id, product.name, product.price))
#             self.conn.commit()
#         except psycopg2.IntegrityError: Краще стандартні помилки   except Exception as e:
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
