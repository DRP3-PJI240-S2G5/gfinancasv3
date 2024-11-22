# coding: utf-8
import logging
import json
from gfinancas4.base.exceptions import BusinessError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from ..commons.django_views_utils import ajax_login_required
from . import service
from .models import Departamento, Responsabilidade
from ..accounts.models import User

logger = logging.getLogger(__name__)

@csrf_exempt
@ajax_login_required
@require_http_methods(["POST"])
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

    new_departamento = service.add_departamento(departamento)

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
        updated_departamento = service.update_departamento(departamento)
        return JsonResponse(updated_departamento, status=200)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=500)

@require_http_methods(["GET"])
@ajax_login_required
def list_departamentos(request):
    """Lista Departamentos"""
    logger.info("API list departamentos")
    departamentos = service.list_departamentos()
    return JsonResponse({"departamentos": departamentos})


@csrf_exempt
@ajax_login_required
@require_http_methods(["POST"])
def add_subordinacao(request):
    """Adiciona uma relação de subordinação entre departamentos."""
    logger.info("API add subordinacao.")
    body = json.loads(request.body)
    
    id_departamento_a = body.get("IdDepartamentoA")
    id_departamento_b = body.get("IdDepartamentoB")
    observacao = body.get("Observacao", "")
    
    # Valida os departamentos
    departamento_a = get_object_or_404(Departamento, id=id_departamento_a)
    departamento_b = get_object_or_404(Departamento, id=id_departamento_b)
    
    # Previne laços de subordinação direta
    if id_departamento_a == id_departamento_b:
        return JsonResponse(
            {"error": "Um departamento não pode ser subordinado a si mesmo."}, 
            status=400
        )
    
    try:
        subordinacao = service.add_subordinacao(departamento_a, departamento_b, observacao)
        return JsonResponse(subordinacao, status=201)
    except ValueError as e:
        return JsonResponse({"error in add_subordinacao": str(e)}, status=500)

@require_http_methods(["GET"])
@ajax_login_required
def list_subordinacoes(request):
    """Lista as relações de subordinação entre departamentos."""
    subordinacoes = service.list_subordinacoes()
    return JsonResponse({"subordinacoes": subordinacoes}, status=200)

@csrf_exempt
@ajax_login_required
@require_http_methods(["POST"])
def add_responsabilidade(request):
    data = json.loads(request.body)
    try:
        usuario = User.objects.get(id=data.get("usuario_id"))
        departamento = Departamento.objects.get(id=data.get("departamento_id"))
        observacao = data.get("observacao", "")
        responsabilidade = Responsabilidade.objects.create(
            IdUser=usuario,
            IdDepartamento=departamento,
            observacao=observacao
        )
        return JsonResponse(responsabilidade.to_dict_json(), status=201)
    except User.DoesNotExist:
        return JsonResponse({"error": "Usuário não encontrado."}, status=404)
    except Departamento.DoesNotExist:
        return JsonResponse({"error": "Departamento não encontrado."}, status=404)

@ajax_login_required
@require_http_methods(["GET"])
def list_responsabilidades(request):
    responsabilidades = Responsabilidade.objects.all()
    data = [resp.to_dict_json() for resp in responsabilidades]
    return JsonResponse(data, safe=False, status=200)
