import os
from django.db import connection
from django.http import JsonResponse
from .exceptions import BusinessError

def dapau(request, error: str = None):
    """
    Retorna um erro real para ajudar nos testes
    """
    if error and error.upper() == "BUSINESS":
        raise BusinessError("BusinessError")
    raise Exception("break on purpose")



def status(request):
    """
    Retorna o estado atual da aplicação
    """
    cursor = connection.cursor()
    cursor.execute("""SELECT 1+1""")
    row = cursor.fetchone()
    git_hash = os.getenv("GIT_HASH", "?")
    return JsonResponse(
        {
            "status": "ok",
            "db": "ok" if row == (2,) else "error",
            "git_hash": git_hash,
        }
    )
