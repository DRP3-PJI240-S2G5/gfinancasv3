# coding: utf-8
import logging
import json
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.contrib import auth
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from ..commons.django_views_utils import ajax_login_required
from ..accounts.models import User
from .service import user_svc
from gfinancas4.base.exceptions import BusinessError
    
logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["POST"])
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Somente usuários autenticados podem acessar
def add_user(request):
    try:
        # Chama o serviço para criar o usuário com os dados recebidos
        user = user_svc.add_user(request.data)
        
        # Retorna a resposta com os dados do usuário criado
        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
            status=status.HTTP_201_CREATED
        )
    except ValidationError as e:
        # Tratamento de erro de validação
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@csrf_exempt
def login(request):
    """
    Login do usuário e criação de uma nova sessão
    """
    logger.info("API login")
    body = json.loads(request.body)
    username = body["username"]
    password = body["password"]
    user_authenticated = auth.authenticate(username=username, password=password)
    user_dict = None
    if user_authenticated is not None:
        if user_authenticated.is_active:
            auth.login(request, user_authenticated)
            user_dict = user_authenticated.to_dict_json()
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
        return JsonResponse({"logout_error": "Logout method must be 'POST'"}, status=405)
    
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


@csrf_exempt
@ajax_login_required
def list_users(request):
    users = User.objects.all()
    users_json = [user.to_dict_json() for user in users]
    return JsonResponse({"users": users_json})