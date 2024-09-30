# coding: utf-8
import logging

import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from django.views.decorators.http import require_http_methods

from ..commons.django_views_utils import ajax_login_required


from .service import departamentos_svc


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
