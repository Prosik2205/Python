import subprocess
import os 
import json
from dotenv import load_dotenv
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

load_dotenv()
DB_PARAMS = json.loads(os.getenv("DB_PARAMS"))

if __name__ == '__main__':
    port = DB_PARAMS["port"]
    host = DB_PARAMS["host"]
    from server import FastServ
    server = FastServ()
    module_name = "server:app"
    workers = 1
    uvicorn_com = [
        "uvicorn",
        module_name,
        "--host", host,
        "--port", str(port),
        "--host", str(host),
        "--workers", str(workers),
    ]
    subprocess.run(uvicorn_com)
