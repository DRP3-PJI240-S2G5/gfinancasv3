# coding: utf-8
import logging
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from ..commons.django_views_utils import ajax_login_required
from .service import departamentos_svc, despesas_svc, verbas_svc, elementos_svc, tiposgastos_svc

logger = logging.getLogger(__name__)

@csrf_exempt
@ajax_login_required
def add_departamento(request):
    """Adiciona Departamento"""
    logger.info("API add new departamento.")
    body = json.loads(request.body)
    description = body.get("description")

    if not description:
        raise ValueError("body.departamento.description: Field required (missing)")
    if type(description) not in [str]:
        raise ValueError("body.departamento.description: Input should be a valid string (string_type)")

    description = str(description)
    if len(description) <= 2:
        raise ValueError(
            "body.departamento.description: Value error, It must be at least 3 characteres long. (value_error)"
        )

    new_departamento = departamentos_svc.add_departamento(description)

    return JsonResponse(new_departamento, status=201)



@require_http_methods(["GET"])
@ajax_login_required

def list_departamentos(request):
    """Lista Departamentos"""
    logger.info("API list departamentos")
    departamentos = departamentos_svc.list_departamentos()
    return JsonResponse({"departamentos": departamentos})

@require_http_methods(["GET"])
@ajax_login_required
def list_departamentos(request):
    """Lista Departamentos"""
    logger.info("API list departamentos")
    departamentos = departamentos_svc.list_departamentos()
    return JsonResponse({"departamentos": departamentos})

# 2. Views para Despesa
@csrf_exempt
@ajax_login_required
def add_despesa(request):
    """Adiciona Despesa"""
    logger.info("API add new despesa.")
    body = json.loads(request.body)
    
    user_id = body.get("IdUser")
    valor = body.get("Valor")
    elemento_id = body.get("IdElemento")
    tipo_gasto_id = body.get("IdTipoGasto")
    departamento_id = body.get("IdDepartamento")
    justificativa = body.get("Justificativa")

    if not all([user_id, valor, elemento_id, tipo_gasto_id, departamento_id, justificativa]):
        return JsonResponse({"error": "All fields are required"}, status=400)
    
    new_despesa = despesas_svc.add_despesa(
        user_id, valor, elemento_id, tipo_gasto_id, departamento_id, justificativa
    )
    return JsonResponse(new_despesa, status=201)


@require_http_methods(["GET"])
@ajax_login_required
def list_despesas(request):
    """Lista Despesas"""
    logger.info("API list despesas")
    despesas = despesas_svc.list_despesas()
    return JsonResponse({"despesas": despesas})

# 3. Views para Verba
@csrf_exempt
@ajax_login_required
def add_verba(request):
    """Adiciona Verba"""
    logger.info("API add new verba.")
    body = json.loads(request.body)

    departamento_id = body.get("IdDepartamento")
    user_id = body.get("IdUser")
    descricao = body.get("descricao")

    if not all([departamento_id, user_id, descricao]):
        return JsonResponse({"error": "All fields are required"}, status=400)

    new_verba = verbas_svc.add_verba(departamento_id, user_id, descricao)
    return JsonResponse(new_verba, status=201)


@require_http_methods(["GET"])
@ajax_login_required
def list_verbas(request):
    """Lista Verbas"""
    logger.info("API list verbas")
    verbas = verbas_svc.list_verbas()
    return JsonResponse({"verbas": verbas})

# 4. Views para Elemento
@csrf_exempt
@ajax_login_required
def add_elemento(request):
    """Adiciona Elemento"""
    logger.info("API add new elemento.")
    body = json.loads(request.body)
    nome = body.get("nome")

    if not nome:
        return JsonResponse({"error": "Field 'nome' is required"}, status=400)

    new_elemento = elementos_svc.add_elemento(nome)
    return JsonResponse(new_elemento, status=201)


@require_http_methods(["GET"])
@ajax_login_required
def list_elementos(request):
    """Lista Elementos"""
    logger.info("API list elementos")
    elementos = elementos_svc.list_elementos()
    return JsonResponse({"elementos": elementos})

# 5. Views para TipoGasto
@csrf_exempt
@ajax_login_required
def add_tipo_gasto(request):
    """Adiciona Tipo de Gasto"""
    logger.info("API add new tipo de gasto.")
    body = json.loads(request.body)
    descricao = body.get("descricao")

    if not descricao:
        return JsonResponse({"error": "Field 'descricao' is required"}, status=400)

    new_tipo_gasto = tiposgastos_svc.add_tipo_gasto(descricao)
    return JsonResponse(new_tipo_gasto, status=201)


@require_http_methods(["GET"])
@ajax_login_required
def list_tipos_gastos(request):
    """Lista Tipos de Gasto"""
    logger.info("API list tipos de gasto")
    tipos_gastos = tiposgastos_svc.list_tipos_gastos()
    return JsonResponse({"tipos_gastos": tipos_gastos})