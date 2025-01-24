import subprocess

if __name__ == '__main__':
    port = "8000"
    host = "127.0.0.1"
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
