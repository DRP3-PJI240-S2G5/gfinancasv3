# coding: utf-8
import logging
import json
from gfinancas4.base.exceptions import BusinessError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from ..commons.django_views_utils import ajax_login_required
from .service import departamentos_svc
from .models import Departamento
from ..accounts.models import User

logger = logging.getLogger(__name__)

@csrf_exempt
@ajax_login_required
def add_departamento(request):
    """Adiciona Departamento"""
    
    logger.info("API add new departamento.")
    body = json.loads(request.body)
    vazio = "Vazio"
    nome = body.get("nome", vazio)
    description = body.get("description", vazio)
    tipoEntidade = body.get("tipoEntidade", vazio)
    responsavelId = body.get("responsavelId", 1)
    done = body.get("done", False)

    try:
        responsavel = User.objects.filter(id=responsavelId).first()
        if not responsavel:
            return JsonResponse({"update_error": f"Responsável com ID {responsavelId} não encontrado."}, status=404)
    except ValueError as e:
        return JsonResponse({"get_responsavel_error", str(e)}, status=500)
    
    
    departamento = Departamento(
        nome=nome, 
        description=description, 
        tipoEntidade=tipoEntidade, 
        responsavelId=responsavel, 
        done=done
    )

    new_departamento = departamentos_svc.add_departamento(departamento)

    return JsonResponse(new_departamento, status=201)

@csrf_exempt
@ajax_login_required
@require_http_methods(["PUT"])   #  VERIFIQUE iSSO DEPOIS QUE FUNCIONAR
def update_departamento(request):
    """Update Departamento"""
    logger.info("API update new departamento.")
    
    body = json.loads(request.body)
    departamentoId = body.get("id")

    departamento = get_object_or_404(Departamento, id=departamentoId)
    
    try:
        responsavel = User.objects.filter(id=body.get("responsavelId", departamento.responsavelId)).first()
        if not responsavel:
            return JsonResponse({"update_error": f"Responsável com ID {departamento.responsavelId} não encontrado."}, status=404)
    except ValueError as e:
        return JsonResponse({"get_responsavel_error", str(e)}, status=500)
    
    departamento.nome = body.get("nome", departamento.nome)
    departamento.description = body.get("description", departamento.description)
    departamento.tipoEntidade = body.get("tipoEntidade", departamento.tipoEntidade)
    departamento.responsavelId = responsavel if responsavel else departamento.responsavelId
    departamento.done = body.get("done", departamento.done)

    try:
        updated_departamento = departamentos_svc.update_departamento(departamento)
        return JsonResponse(updated_departamento, status=200)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@require_http_methods(["GET"])
@ajax_login_required
def list_departamentos(request):
    """Lista Departamentos"""
    logger.info("API list departamentos")
    departamentos = departamentos_svc.list_departamentos()
    return JsonResponse({"departamentos": departamentos})


