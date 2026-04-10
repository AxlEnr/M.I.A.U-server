from rest_framework.response import Response as ResponseRest

#Estándar para mostrar errores
class ApiResponse():

    @staticmethod
    def error(message: str, http_code: int, data: any = None): 
        return ResponseRest({
            "success": False,
            "data": None,
            "error": {
                "code": http_code,
                "message": message,
                "data": data
            }
        }, status=http_code)
    
    @staticmethod
    def success(data: any, http_code: int = 200):
        return ResponseRest({
            "success": True,
            "data": data,
            "error": None
        }, status=http_code)