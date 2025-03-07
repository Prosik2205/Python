import subprocess
import os 
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    port = os.getenv("port")
    host = os.getenv("host")
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
