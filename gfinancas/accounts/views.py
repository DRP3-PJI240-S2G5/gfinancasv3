# coding: utf-8
import logging
import json
from django.contrib import auth
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods
from ..commons.django_views_utils import ajax_login_required

logger = logging.getLogger(__name__)



@csrf_exempt
def login(request):
    """
    Login do usuário e criação de uma nova sessão
    """
    logger.info("API login")
    body = json.loads(request.body)
    username = body["username"]
    password = body["password"]
    user_authenticaded = auth.authenticate(username=username, password=password)
    user_dict = None
    if user_authenticaded is not None:
        if user_authenticaded.is_active:
            auth.login(request, user_authenticaded)
            user_dict = user_authenticaded.to_dict_json()
            logger.info("API login success")
    if not user_dict:
        user_dict = {"message": "Unauthorized"}
        return JsonResponse(user_dict, safe=False, status=401)
    return JsonResponse(user_dict, safe=False, status=201)



def logout(request):
    """
    Encerra sessão do usuário
    """
    if request.method.lower() != "post":
        raise Exception("Logout only via post")
    logger.info(f"API logout: {request.user.username}")
    auth.logout(request)
    return JsonResponse({})



def whoami(request):
    """
    Retorna dados do usuário logado
    """
    user_data = {"authenticated": False}
    if request.user.is_authenticated:
        user_data["authenticated"] = True
        user_data["user"] = request.user.to_dict_json()

    logger.info("API whoami")
    return JsonResponse(user_data)

@require_http_methods(["GET"])
@ajax_login_required
def users(request):
    """
    Retorna todos os usuários
    """
    if not request.user.is_authenticated:
        return JsonResponse({"message": "Unauthorized"}, status=401)

    # Obter todos os usuários
    users = get_user_model().objects.all()
    users_list = [user.to_dict_json() for user in users]

    return JsonResponse({"users": users_list}, safe=False)