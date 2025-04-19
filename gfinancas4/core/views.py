# coding: utf-8
import logging
import json
from django.contrib.auth import get_user_model
from gfinancas4.base.exceptions import BusinessError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from ..commons.django_views_utils import ajax_login_required
from . import service
from .models import Departamento, Responsabilidade, Elemento, TipoGasto, Despesa
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
        new_departamento = service.add_departamento(
            nome=nome,
            description=description,
            tipoEntidade=tipoEntidade,
            responsavelId=responsavelId,
            done=done
        )
        return JsonResponse(new_departamento, status=201)
    except BusinessError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        logger.error(f"Erro ao adicionar departamento: {str(e)}")
        return JsonResponse({"error": "Erro interno do servidor"}, status=500)


@csrf_exempt
@ajax_login_required
@require_http_methods(["PUT"])
def update_departamento(request):
    """Update Departamento"""
    logger.info("API update departamento.")
    
    body = json.loads(request.body)
    departamento_id = body.get("id")
    
    if not departamento_id:
        return JsonResponse({"error": "ID do departamento não fornecido."}, status=400)
    
    nome = body.get("nome")
    description = body.get("description")
    tipoEntidade = body.get("tipoEntidade")
    responsavelId = body.get("responsavelId")
    done = body.get("done")
    
    try:
        updated_departamento = service.update_departamento(
            departamento_id=departamento_id,
            nome=nome,
            description=description,
            tipoEntidade=tipoEntidade,
            responsavelId=responsavelId,
            done=done
        )
        return JsonResponse(updated_departamento, status=200)
    except BusinessError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        logger.error(f"Erro ao atualizar departamento: {str(e)}")
        return JsonResponse({"error": "Erro interno do servidor"}, status=500)

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
    
    # Previne laços de subordinação direta
    if id_departamento_a == id_departamento_b:
        return JsonResponse(
            {"error": "Um departamento não pode ser subordinado a si mesmo."}, 
            status=400
        )
    
    try:
        subordinacao = service.add_subordinacao(
            superior_id=id_departamento_a,
            subordinado_id=id_departamento_b,
            observacao=observacao
        )
        return JsonResponse(subordinacao, status=201)
    except BusinessError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        logger.error(f"Erro ao adicionar subordinação: {str(e)}")
        return JsonResponse({"error": "Erro interno do servidor"}, status=500)

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
    """Adiciona uma responsabilidade a um usuário em um departamento."""
    logger.info("API add responsabilidade.")
    
    body = json.loads(request.body)
    
    usuario_id = body.get("usuario_id")
    departamento_id = body.get("departamento_id")
    observacao = body.get("observacao", "")
    
    try:
        # Chama o serviço para adicionar a responsabilidade
        response_data = service.add_responsabilidade(
            usuario_id=usuario_id,
            departamento_id=departamento_id,
            observacao=observacao
        )
        return JsonResponse(response_data, status=201)
    
    except BusinessError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        logger.error(f"Erro ao adicionar responsabilidade: {str(e)}")
        return JsonResponse({"error": "Erro interno do servidor"}, status=500)

@csrf_exempt
@ajax_login_required
@require_http_methods(["PUT"])
def update_responsabilidade_view(request, id):
    """Atualiza uma responsabilidade existente."""
    logger.info("API update responsabilidade.")
    
    body = json.loads(request.body)
    observacao = body.get("observacao", "")
    
    try:
        # Chama o serviço para atualizar a responsabilidade
        response_data = service.update_responsabilidade(
            responsabilidade_id=id,
            observacao=observacao
        )
        return JsonResponse(response_data, status=200)
    
    except BusinessError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        logger.error(f"Erro ao atualizar responsabilidade: {str(e)}")
        return JsonResponse({"error": "Erro interno do servidor"}, status=500)

@ajax_login_required
@require_http_methods(["GET"])
def list_responsabilidades(request):
    """Lista todas as responsabilidades associadas a departamentos."""
    logger.info("API list responsabilidades.")
    
    try:
        # Chama o serviço para listar as responsabilidades
        response_data = service.list_responsabilidades()
        return JsonResponse(response_data, safe=False, status=200)
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@ajax_login_required
@require_http_methods(["GET"])
def list_elementos(request):
    """Lista todos os elementos."""
    logger.info("API list elementos.")
    
    try:
        # Chama o serviço para listar as responsabilidades
        response_data = service.list_elementos()
        return JsonResponse({"elementos": response_data}, safe=False, status=200)
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@ajax_login_required
@require_http_methods(["GET"])
def list_tipo_gastos(request):
    """Lista todos os Tipos de Gastos."""
    logger.info("API list tipo gastos.")
    
    try:
        # Chama o serviço para listar o tipo de gastos
        response_data = service.list_tipo_gastos()
        return JsonResponse({"tipoGastos": response_data}, safe=False, status=200)
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
def list_tipo_gastos_por_elemento(request, elemento_id):
    try:
        response_data = service.list_tipo_gastos_por_elemento(elemento_id)
        return JsonResponse({"tipo_gastos": response_data}, safe=False, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

@csrf_exempt
@ajax_login_required
@require_http_methods(["POST"])
def add_despesa(request):
    """Adiciona uma nova despesa."""
    logger.info("API add despesa.")
    body = json.loads(request.body)
        
    # Obtendo os dados do corpo da requisição
    user_id = body.get("user_id")
    departamento_id = body.get("departamento_id")
    valor = body.get("valor")
    elemento_id = body.get("elemento_id")
    tipo_gasto_id = body.get("tipo_gasto_id")
    justificativa = body.get("justificativa", "")

    try:
        # Verificando se o usuário e o departamento existem
        user = User.objects.get(id=user_id)
        departamento = Departamento.objects.get(id=departamento_id)
        elemento = Elemento.objects.get(id=elemento_id)
        tipo_gasto = TipoGasto.objects.get(id=tipo_gasto_id)

    except User.DoesNotExist:
        return JsonResponse({"error": "Usuário não encontrado."}, status=404)
    except Departamento.DoesNotExist:
        return JsonResponse({"error": "Departamento não encontrado."}, status=404)
    except Elemento.DoesNotExist:
        return JsonResponse({"error": "Elemento não encontrado."}, status=404)
    except TipoGasto.DoesNotExist:
        return JsonResponse({"error": "Tipo de Gasto não encontrado."}, status=404)

    # Criando uma nova instância de Despesa
    nova_despesa = Despesa(
        user=user,
        departamento=departamento,
        valor=valor,
        elemento=elemento,
        tipoGasto=tipo_gasto,
        justificativa=justificativa
    )

    try:
        # Chama o serviço para adicionar a despesa
        response_data = service.add_despesa(nova_despesa)
        return JsonResponse(response_data, status=201)
    except BusinessError as e:
        return JsonResponse({"errorr": str(e)}, status=400)
    except Exception as e:
        return JsonResponse({"errorr": str(e)}, status=500)
    
@csrf_exempt
@ajax_login_required
@require_http_methods(["PUT"])
def update_despesa(request):
    """Atualiza uma despesa existente."""
    logger.info("API update despesa.")
    body = json.loads(request.body)

    # Obtendo o ID da despesa a ser atualizada
    despesa_id = body.get("id")
    
    # Buscando a despesa pelo ID
    despesa = get_object_or_404(Despesa, id=despesa_id)

    # Obtendo os dados que podem ser atualizados
    user_id = body.get("user_id", despesa.user.id)
    departamento_id = body.get("departamento_id", despesa.departamento.id)
    valor = body.get("valor")
    elemento_id = body.get("elemento_id", despesa.elemento.id)
    tipo_gasto_id = body.get("tipo_gasto_id", despesa.tipoGasto.id)
    justificativa = body.get("justificativa", despesa.justificativa)

    try:
        # Verificando se os objetos relacionados existem
        user = User.objects.get(id=user_id)
        departamento = Departamento.objects.get(id=departamento_id)
        elemento = Elemento.objects.get(id=elemento_id)
        tipo_gasto = TipoGasto.objects.get(id=tipo_gasto_id)
        
        # Atualizando os campos da despesa
        despesa.user = user
        despesa.departamento = departamento
        if valor is not None:
            despesa.valor = valor
        despesa.elemento = elemento
        despesa.tipoGasto = tipo_gasto
        despesa.justificativa = justificativa

        # Chama o serviço para atualizar a despesa
        response_data = service.update_despesa(despesa)
        return JsonResponse(response_data, status=200)

    except User.DoesNotExist:
        return JsonResponse({"error": "Usuário não encontrado."}, status=404)
    except Departamento.DoesNotExist:
        return JsonResponse({"error": "Departamento não encontrado."}, status=404)
    except Elemento.DoesNotExist:
        return JsonResponse({"error": "Elemento não encontrado."}, status=404)
    except TipoGasto.DoesNotExist:
        return JsonResponse({"error": "Tipo de Gasto não encontrado."}, status=404)
    except BusinessError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        logger.error(f"Erro ao atualizar despesa: {str(e)}")
        return JsonResponse({"error": "Erro interno do servidor"}, status=500)
    
@csrf_exempt
@ajax_login_required
@require_http_methods(["GET"])
def list_despesas(request):
    """View que retorna despesas paginadas."""
    try:
        page = int(request.GET.get("page", 1))
        per_page = int(request.GET.get("per_page", 10))

        resultado = service.list_despesas(page, per_page)
        return JsonResponse(resultado, status=200)

    except Exception as e:
        logger.error(f"Erro ao paginar despesas: {e}")
        return JsonResponse({"error": "Erro ao listar despesas."}, status=500)

@csrf_exempt
@ajax_login_required
@require_http_methods(["GET"])
def list_despesas_departamento(request, departamento_id):
    """Lista as despesas de um departamento específico com paginação."""
    try:
        # Obtendo os parâmetros de paginação da requisição (padrão: página 1, 10 itens por página)
        page = int(request.GET.get("page", 1))
        per_page = int(request.GET.get("per_page", 10))

        # Chamando o serviço para obter as despesas paginadas
        despesas = service.list_despesas_departamento(departamento_id, page, per_page)

        # Retornando o resultado com as despesas e informações de paginação
        return JsonResponse(despesas, status=200)
    
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=404)
    except Exception as e:
        logger.error(f"Erro ao listar despesas do departamento {departamento_id}: {e}")
        return JsonResponse({"error": "Erro ao listar despesas do departamento."}, status=500)

@ajax_login_required
@require_http_methods(["GET"])
def total_despesas_departamento(request, departamento_id):
    """
    Retorna o total de despesas de um departamento específico.
    """
    logger.info(f"API get total despesas departamento: {departamento_id}")
    
    try:
        resultado = service.get_total_despesas_departamento(departamento_id)
        return JsonResponse(resultado, status=200)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=404)
    except BusinessError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        logger.error(f"Erro ao obter total de despesas: {str(e)}")
        return JsonResponse({"error": "Erro interno do servidor"}, status=500)

@ajax_login_required
@require_http_methods(["POST"])
def add_despesa_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = request.user.id
            departamento_id = data.get('departamento_id')
            valor = data.get('valor')
            elemento_id = data.get('elemento_id')
            tipo_gasto_id = data.get('tipo_gasto_id')
            justificativa = data.get('justificativa', '')

            if not all([departamento_id, valor, elemento_id, tipo_gasto_id]):
                return JsonResponse({'error': 'Dados incompletos'}, status=400)

            despesa = service.add_despesa(
                user_id=user_id,
                departamento_id=departamento_id,
                valor=valor,
                elemento_id=elemento_id,
                tipo_gasto_id=tipo_gasto_id,
                justificativa=justificativa
            )
            return JsonResponse(despesa)
        except service.BusinessError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            logger.error(f"Erro ao adicionar despesa: {str(e)}")
            return JsonResponse({'error': 'Erro interno do servidor'}, status=500)
    return JsonResponse({'error': 'Método não permitido'}, status=405)