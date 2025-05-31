import psycopg2
from psycopg2.extras import RealDictCursor
import os 
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    return psycopg2.connect(
        dbname = os.getenv("dbname"),
        user = os.getenv("user"),
        password = os.getenv("password"),
        host = os.getenv("db_host"),
        port = os.getenv("db_port"),
        cursor_factory = RealDictCursor
    )

