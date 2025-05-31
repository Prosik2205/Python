import psycopg2
from psycopg2.extras import RealDictCursor
import json
import os 
from dotenv import load_dotenv

load_dotenv()
DB_PARAMS = json.loads(os.getenv("DB_PARAMS"))

def get_db_connection():
    return psycopg2.connect(
        dbname = DB_PARAMS["dbname"],
        user = DB_PARAMS["user"],
        password = DB_PARAMS["password"],
        host = DB_PARAMS["db_host"],
        port = DB_PARAMS["db_port"],
        cursor_factory = RealDictCursor
    )

