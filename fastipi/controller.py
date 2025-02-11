import psycopg2  
from psycopg2.extras import RealDictCursor
from fastapi import HTTPException
from db import get_db_connection  

# All def must be @staticmethod (post_product for example)
class ControllerProducts:
    # CAN BE but better in all function do call
    def __init__(self):
        self.conn = get_db_connection()  
        self.cur = self.conn.cursor()
    
    @staticmethod
    def post_product(self, product):
        # sql = """
        #     SELECT * FROM pussy WHERE pussy = "small"
        # """
        # try:
            # db,cursor = get_db_connection()
            # cursor.execute(sql,(<some_params>,))
            # res = cursor.fetchone() or cursor.fetchall()
        # except Exception as e:
        #   db.rollback()
        #   raise Exception(f"Problem with base {e}")
        # db.commit() if INSERT OR DELETE OR UPDATE
        # db.close()
        # return res

        try:
            self.cur.execute("INSERT INTO products (id, name, price) VALUES (%s, %s, %s) RETURNING *;", 
                             (product.id, product.name, product.price))
            self.conn.commit()
        except psycopg2.IntegrityError:
            self.conn.rollback()
            raise HTTPException(status_code=400, detail="Product with this ID already exists")

    def get_product(self, product_id):
        self.cur.execute("SELECT * FROM products WHERE id = %s;", (product_id,))
        product = self.cur.fetchone()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    def put_product(self, product_id, product):
        self.cur.execute("UPDATE products SET name = %s, price = %s WHERE id = %s RETURNING *;", 
                         (product.name, product.price, product_id))
        updated_product = self.cur.fetchone()
        self.conn.commit()
        if not updated_product:
            raise HTTPException(status_code=404, detail="Product not found")

    def del_product(self, product_id):
        self.cur.execute("DELETE FROM products WHERE id = %s RETURNING *;", (product_id,))
        deleted_product = self.cur.fetchone()
        self.conn.commit()
        if not deleted_product:
            raise HTTPException(status_code=404, detail="Product not found")
# THIS REMOVE 
# IF YOT TELL WHY I SAY LOOK TO ROUTER
controller = ControllerProducts()
