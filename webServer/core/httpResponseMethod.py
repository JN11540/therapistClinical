from fastapi.responses import JSONResponse
 
 
class HttpResponseMethod:
 
    @staticmethod
    def _build_content(result: bool, data: object, message: str) -> dict:
        return {
            "result": result,
            "data": data,
            "message": message,
        }
 
    @staticmethod
    async def ok(data: object = None, message: str = "Success") -> JSONResponse:
        return JSONResponse(
            status_code=200,
            content=HttpResponseMethod._build_content(True, data, message),
        )
 
    @staticmethod
    async def bad_request(data: object = None, message: str = "Bad Request") -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content=HttpResponseMethod._build_content(False, data, message),
        )

    @staticmethod
    async def not_found(data: object = None, message: str = "Not Found") -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content=HttpResponseMethod._build_content(False, data, message),
        )

    @staticmethod
    async def internal_server_error(data: object = None, message: str = "Internal Server Error") -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content=HttpResponseMethod._build_content(False, data, message),
        )