from fastapi.responses import JSONResponse


class Responce:
    def res_get(get_res):
        if isinstance(get_res, str):
            return JSONResponse(content={"product str": get_res}, status_code=200)
        elif isinstance(get_res, list):
            return JSONResponse(content={"product list": get_res}, status_code=200)
        elif isinstance(get_res, dict):
            return JSONResponse(content={"product dict":get_res}, status_code=200)
        else:
            return JSONResponse(content={"error": "Invalid response format"}, status_code=400)
        
        




