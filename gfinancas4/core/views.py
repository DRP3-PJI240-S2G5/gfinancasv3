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
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from decimal import Decimal, InvalidOperation
from datetime import datetime

logger = logging.getLogger(__name__)

@csrf_exempt
@ajax_login_required
@require_http_methods(["POST"])
def add_departamento(request):
    """Adiciona Departamento"""
    
    logger.info("API add new departamento.")
    body = json.loads(request.body)
    nome = body.get("nome")
    description = body.get("description")
    tipoEntidade = body.get("tipoEntidade")
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

@csrf_exempt
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

@csrf_exempt
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

@csrf_exempt    
@ajax_login_required
@require_http_methods(["GET"])
def list_elementos(request):
    """Lista todos os elementos."""
    logger.info("API list elementos.")
    
    try:
        response_data = service.list_elementos()
        return JsonResponse({"elementos": response_data}, safe=False, status=200)
    except BusinessError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        logger.error(f"Erro ao listar elementos: {str(e)}")
        return JsonResponse({"error": "Erro interno do servidor"}, status=500)

@csrf_exempt    
@ajax_login_required
@require_http_methods(["GET"])
def list_tipo_gastos(request):
    """Lista todos os Tipos de Gastos."""
    logger.info("API list tipo gastos.")
    
    try:
        response_data = service.list_tipo_gastos()
        return JsonResponse({"tipoGastos": response_data}, safe=False, status=200)
    except BusinessError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        logger.error(f"Erro ao listar tipos de gasto: {str(e)}")
        return JsonResponse({"error": "Erro interno do servidor"}, status=500)

@csrf_exempt
@ajax_login_required
@require_http_methods(["GET"])    
def list_tipo_gastos_por_elemento(request, elemento_id):
    """Lista todos os tipos de gasto associados a um elemento."""
    logger.info(f"API list tipo gastos por elemento {elemento_id}")
    
    try:
        response_data = service.list_tipo_gastos_por_elemento(elemento_id)
        return JsonResponse({"tipo_gastos": response_data}, safe=False, status=200)
    except BusinessError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        logger.error(f"Erro ao listar tipos de gasto do elemento: {str(e)}")
        return JsonResponse({"error": "Erro interno do servidor"}, status=500)

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

@csrf_exempt
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

@csrf_exempt
@ajax_login_required
@require_http_methods(["GET"])
def total_despesas_departamento_apartir_data(request, departamento_id, data_inicio):
    """
    Retorna o total das despesas de um departamento a partir de uma data específica.
    """
    logger.info(f"API total despesas departamento {departamento_id} a partir de {data_inicio}")
    try:
        data_inicio_date = datetime.strptime(data_inicio, "%Y-%m-%d").date()
        
        resultado = service.get_total_despesas_departamento_apartir_data(departamento_id, data_inicio_date)
        return JsonResponse(resultado, status=200)
    
    except ValueError as e:
        logger.error(f"Erro de valor: {e}")
        return JsonResponse({"error": "Data em formato inválido. Use AAAA-MM-DD."}, status=400)
    except Exception as e:
        logger.error(f"Erro ao calcular total de despesas do departamento {departamento_id} a partir da data {data_inicio}: {e}")
        return JsonResponse({"error": "Erro interno do servidor."}, status=500)

@csrf_exempt
@ajax_login_required
@require_http_methods(["GET"])
def list_despesas_departamento_apartir_data(request, departamento_id, data_inicio):
    """
    Lista paginada das despesas de um departamento a partir de uma data específica.
    """
    logger.info(f"API list despesas departamento {departamento_id} a partir de {data_inicio}")
    try:
        # Validação da data
        data_inicio_date = datetime.strptime(data_inicio, "%Y-%m-%d").date()
        
        # Paginação
        page = int(request.GET.get("page", 1))
        per_page = int(request.GET.get("per_page", 10))
        
        # Chamada ao serviço
        resultado = service.list_despesas_departamento_apartir_data(departamento_id, data_inicio_date, page, per_page)
        return JsonResponse(resultado, status=200)
    
    except ValueError as e:
        logger.error(f"Erro de valor: {e}")
        return JsonResponse({"error": "Parâmetros inválidos. Verifique a data e paginação."}, status=400)
    except Exception as e:
        logger.error(f"Erro ao listar despesas do departamento {departamento_id} a partir da data {data_inicio}: {e}")
        return JsonResponse({"error": "Erro interno do servidor."}, status=500)

@csrf_exempt
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

@csrf_exempt
@ajax_login_required
@require_http_methods(["PUT"])
def update_subordinacao(request, id):
    """Atualiza uma relação de subordinação existente."""
    logger.info("API update subordinacao.")
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
        subordinacao = service.update_subordinacao(
            subordinacao_id=id,
            superior_id=id_departamento_a,
            subordinado_id=id_departamento_b,
            observacao=observacao
        )
        return JsonResponse(subordinacao, status=200)
    except BusinessError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        logger.error(f"Erro ao atualizar subordinação: {str(e)}")
        return JsonResponse({"error": "Erro interno do servidor"}, status=500)

@csrf_exempt
@ajax_login_required
@require_http_methods(["DELETE"])
def delete_subordinacao(request, id):
    """Remove uma relação de subordinação existente."""
    logger.info(f"API delete subordinacao: {id}")
    
    try:
        service.delete_subordinacao(id)
        return JsonResponse({"message": "Subordinação removida com sucesso."}, status=200)
    except BusinessError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        logger.error(f"Erro ao remover subordinação: {str(e)}")
        return JsonResponse({"error": "Erro interno do servidor"}, status=500)

@csrf_exempt
@ajax_login_required
@require_http_methods(["POST"])
def add_verba(request):
    """
    Adiciona uma nova verba.
    
    Args:
        request: Requisição HTTP contendo os dados da verba
        
    Returns:
        JsonResponse: Resposta HTTP com os dados da verba criada
        
    Raises:
        HTTP_400_BAD_REQUEST: Se os dados forem inválidos
        HTTP_500_INTERNAL_SERVER_ERROR: Se ocorrer um erro interno
    """
    logger.info("API add verba")
    
    try:
        # Obtém os dados do corpo da requisição
        data = json.loads(request.body)
        
        # Validação dos campos obrigatórios
        required_fields = ['valor', 'departamento_id', 'ano']
        for field in required_fields:
            if field not in data:
                return JsonResponse(
                    {"error": f"Campo obrigatório não fornecido: {field}"},
                    status=400
                )
        
        # Converte o valor para Decimal
        try:
            valor = Decimal(str(data['valor']))
        except (ValueError, InvalidOperation):
            return JsonResponse(
                {"error": "Valor inválido. Forneça um número válido."},
                status=400
            )
        
        # Converte o ano para inteiro
        try:
            ano = int(data['ano'])
        except (ValueError, TypeError):
            return JsonResponse(
                {"error": "Ano inválido. Forneça um número inteiro."},
                status=400
            )
        
        # Adiciona a verba
        verba = service.add_verba(
            valor=valor,
            departamento_id=data['departamento_id'],
            user_id=request.user.id,
            ano=ano,
            descricao=data.get('descricao', '')
        )
        
        return JsonResponse(verba, status=201)
        
    except BusinessError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        logger.error(f"Erro ao adicionar verba: {str(e)}", exc_info=True)
        return JsonResponse(
            {"error": "Erro interno do servidor"},
            status=500
        )

@csrf_exempt
@ajax_login_required
@require_http_methods(["PUT"])
def update_verba(request, id):
    """
    Atualiza uma verba existente.
    
    Args:
        request: Requisição HTTP contendo os dados da verba
        id: ID da verba a ser atualizada
        
    Returns:
        JsonResponse: Resposta HTTP com os dados da verba atualizada
        
    Raises:
        HTTP_400_BAD_REQUEST: Se os dados forem inválidos
        HTTP_404_NOT_FOUND: Se a verba não for encontrada
        HTTP_500_INTERNAL_SERVER_ERROR: Se ocorrer um erro interno
    """
    logger.info(f"API update verba: id={id}")
    
    try:
        # Obtém os dados do corpo da requisição
        data = json.loads(request.body)
        
        # Validação dos campos obrigatórios
        required_fields = ['valor', 'departamento_id', 'ano']
        for field in required_fields:
            if field not in data:
                return JsonResponse(
                    {"error": f"Campo obrigatório não fornecido: {field}"},
                    status=400
                )
        
        # Converte o valor para Decimal
        try:
            valor = Decimal(str(data['valor']))
        except (ValueError, InvalidOperation):
            return JsonResponse(
                {"error": "Valor inválido. Forneça um número válido."},
                status=400
            )
        
        # Converte o ano para inteiro
        try:
            ano = int(data['ano'])
        except (ValueError, TypeError):
            return JsonResponse(
                {"error": "Ano inválido. Forneça um número inteiro."},
                status=400
            )
        
        # Atualiza a verba
        verba = service.update_verba(
            verba_id=id,
            valor=valor,
            departamento_id=data['departamento_id'],
            ano=ano,
            descricao=data.get('descricao', '')
        )
        
        return JsonResponse(verba, status=200)
        
    except BusinessError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        logger.error(f"Erro ao atualizar verba: {str(e)}", exc_info=True)
        return JsonResponse(
            {"error": "Erro interno do servidor"},
            status=500
        )

@csrf_exempt
@ajax_login_required
@require_http_methods(["DELETE"])
def delete_verba(request, id):
    """
    Remove uma verba.
    
    Args:
        request: Requisição HTTP
        id: ID da verba a ser removida
        
    Returns:
        JsonResponse: Resposta HTTP indicando sucesso
        
    Raises:
        HTTP_404_NOT_FOUND: Se a verba não for encontrada
        HTTP_500_INTERNAL_SERVER_ERROR: Se ocorrer um erro interno
    """
    logger.info(f"API delete verba: id={id}")
    
    try:
        service.delete_verba(id)
        return JsonResponse({"message": "Verba excluída com sucesso"}, status=200)
        
    except BusinessError as e:
        return JsonResponse({"error": str(e)}, status=404)
    except Exception as e:
        logger.error(f"Erro ao remover verba: {str(e)}", exc_info=True)
        return JsonResponse(
            {"error": "Erro interno do servidor"},
            status=500
        )

@csrf_exempt
@ajax_login_required
@require_http_methods(["GET"])
def get_verba(request, id):
    """
    Retorna os dados de uma verba específica.
    
    Args:
        request: Requisição HTTP
        id: ID da verba
        
    Returns:
        JsonResponse: Resposta HTTP com os dados da verba
        
    Raises:
        HTTP_404_NOT_FOUND: Se a verba não for encontrada
        HTTP_500_INTERNAL_SERVER_ERROR: Se ocorrer um erro interno
    """
    logger.info(f"API get verba: id={id}")
    
    try:
        verba = service.get_verba(id)
        return JsonResponse(verba, status=200)
        
    except BusinessError as e:
        return JsonResponse({"error": str(e)}, status=404)
    except Exception as e:
        logger.error(f"Erro ao buscar verba: {str(e)}", exc_info=True)
        return JsonResponse(
            {"error": "Erro interno do servidor"},
            status=500
        )

@csrf_exempt
@ajax_login_required
@require_http_methods(["GET"])
def list_verbas(request):
    """
    Lista todas as verbas com paginação.
    
    Args:
        request: Requisição HTTP com parâmetros de paginação opcionais
        
    Returns:
        JsonResponse: Lista de verbas serializadas com informações de paginação
    """
    try:
        logger.info(f"Iniciando listagem de verbas. Usuário: {request.user.username}")
        
        # Verifica se o usuário está autenticado
        if not request.user.is_authenticated:
            logger.error(f"Usuário não autenticado tentou acessar listagem de verbas")
            return JsonResponse({'error': 'Usuário não autenticado'}, status=401)
        
        # Obter parâmetros de paginação
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 10))
        
        # Lista as verbas com paginação
        result = service.list_verbas(page=page, per_page=per_page)
        
        # Verifica se há verbas
        if not result['verbas']:
            logger.info("Nenhuma verba encontrada")
            return JsonResponse({
                'verbas': [], 
                'paginacao': result['paginacao'],
                'message': 'Nenhuma verba encontrada'
            })
            
        logger.info(f"Listagem de verbas concluída com sucesso. Página {page} de {result['paginacao']['total_paginas']}")
        return JsonResponse(result)
        
    except BusinessError as e:
        logger.error(f"Erro de negócio ao listar verbas: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        logger.error(f"Erro ao listar verbas: {str(e)}", exc_info=True)
        return JsonResponse({'error': 'Erro interno ao listar verbas'}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
@ajax_login_required
def list_verbas_departamento(request, departamento_id):
    """
    Lista todas as verbas de um departamento específico.
    
    Args:
        request: Request HTTP
        departamento_id: ID do departamento
        
    Returns:
        JsonResponse: Lista de verbas do departamento serializadas
    """
    try:
        logger.info(f"Iniciando listagem de verbas do departamento {departamento_id}. Usuário: {request.user.username}")
        
        # Verifica se o usuário está autenticado
        if not request.user.is_authenticated:
            logger.error(f"Usuário não autenticado tentou acessar listagem de verbas do departamento {departamento_id}")
            return JsonResponse({'error': 'Usuário não autenticado'}, status=401)
            
        # Lista as verbas do departamento
        verbas = service.list_verbas_departamento(departamento_id)
        
        # Verifica se há verbas
        if not verbas:
            logger.info(f"Nenhuma verba encontrada para o departamento {departamento_id}")
            return JsonResponse({'verbas': [], 'message': f'Nenhuma verba encontrada para o departamento {departamento_id}'})
            
        logger.info(f"Listagem de verbas do departamento {departamento_id} concluída com sucesso. Total: {len(verbas)}")
        return JsonResponse({'verbas': verbas})
        
    except BusinessError as e:
        logger.error(f"Erro de negócio ao listar verbas do departamento {departamento_id}: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        logger.error(f"Erro ao listar verbas do departamento {departamento_id}: {str(e)}", exc_info=True)
        return JsonResponse({'error': 'Erro interno ao listar verbas do departamento'}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
@ajax_login_required
def get_verba_departamento_ano(request, departamento_id, ano):
    """
    Retorna a verba de um departamento para um ano específico.
    
    Args:
        request: Requisição HTTP
        departamento_id: ID do departamento
        ano: Ano da verba
        
    Returns:
        JsonResponse: Resposta HTTP com os dados da verba
        
    Raises:
        HTTP_400_BAD_REQUEST: Se o ano for inválido
        HTTP_404_NOT_FOUND: Se o departamento não for encontrado ou não houver verba
        HTTP_500_INTERNAL_SERVER_ERROR: Se ocorrer um erro interno
    """
    logger.info(f"API get verba departamento ano: departamento_id={departamento_id}, ano={ano}")
    
    try:
        # Converte o ano para inteiro
        try:
            ano = int(ano)
        except (ValueError, TypeError):
            return JsonResponse(
                {"error": "Ano inválido. Forneça um número inteiro."},
                status=400
            )
        
        verba = service.get_verba_departamento_ano(departamento_id, ano)
        return JsonResponse(verba, status=200)
        
    except BusinessError as e:
        return JsonResponse({"error": str(e)}, status=404)
    except Exception as e:
        logger.error(f"Erro ao buscar verba do departamento: {str(e)}", exc_info=True)
        return JsonResponse(
            {"error": "Erro interno do servidor"},
            status=500
        )
    
@csrf_exempt
@ajax_login_required
@require_http_methods(["GET"])
def get_ultima_verba_departamento(request, departamento_id):
    """
    Retorna a última verba definida para um departamento específico.
    
    Args:
        request: Requisição HTTP
        departamento_id: ID do departamento
        
    Returns:
        JsonResponse: Dados da última verba definida para o departamento
        
    Raises:
        HTTP_404_NOT_FOUND: Se o departamento não for encontrado ou não houver verba
        HTTP_500_INTERNAL_SERVER_ERROR: Se ocorrer um erro interno
    """
    logger.info(f"API get última verba departamento: departamento_id={departamento_id}")
    
    try:
        # Obtém a última verba para o departamento
        ultima_verba = service.get_ultima_verba_departamento(departamento_id)
        
        if not ultima_verba:
            logger.info(f"Nenhuma verba encontrada para o departamento {departamento_id}")
            return JsonResponse({'error': f'Nenhuma verba encontrada para o departamento {departamento_id}'}, status=404)
        
        logger.info(f"Última verba do departamento {departamento_id} recuperada com sucesso")
        return JsonResponse(ultima_verba, status=200)
        
    except BusinessError as e:
        logger.error(f"Erro de negócio ao buscar última verba do departamento {departamento_id}: {str(e)}")
        return JsonResponse({'error': str(e)}, status=404)
    except Exception as e:
        logger.error(f"Erro ao buscar última verba do departamento {departamento_id}: {str(e)}", exc_info=True)
        return JsonResponse({'error': 'Erro interno ao buscar última verba'}, status=500)

@csrf_exempt
@ajax_login_required
@require_http_methods(["GET"])
def list_despesas_departamento_periodo(request, departamento_id, data_inicio, data_termino):
    """Lista despesas de um departamento em um período específico"""
    try:
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 10))

        despesas = service.list_despesas_departamento_periodo(
            departamento_id=departamento_id,
            data_inicio=data_inicio,
            data_termino=data_termino,
            page=page,
            per_page=per_page
        )
        return JsonResponse(despesas, safe=False)
    except BusinessError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        logger.error(f"Erro ao listar despesas do departamento: {str(e)}")
        return JsonResponse({"error": "Erro interno do servidor"}, status=500)

@csrf_exempt
@ajax_login_required
@require_http_methods(["GET"])
def total_despesas_departamento_periodo(request, departamento_id, data_inicio, data_termino):
    """Retorna o valor total das despesas de um departamento em um período específico"""
    try:
        total = service.total_despesas_departamento_periodo(
            departamento_id=departamento_id,
            data_inicio=data_inicio,
            data_termino=data_termino
        )
        return JsonResponse({"total": str(total)}, safe=False)
    except BusinessError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        logger.error(f"Erro ao calcular total de despesas do departamento: {str(e)}")
        return JsonResponse({"error": "Erro interno do servidor"}, status=500)

@csrf_exempt
@ajax_login_required
@require_http_methods(["DELETE"])
def delete_despesa(request, id):
    """Remove uma despesa existente."""
    logger.info(f"API delete despesa: {id}")
    
    try:
        service.delete_despesa(id)
        return JsonResponse({"success": True}, status=200)
    except BusinessError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        logger.error(f"Erro ao remover despesa: {str(e)}")
        return JsonResponse({"error": "Erro interno do servidor"}, status=500)

@csrf_exempt
@ajax_login_required
@require_http_methods(["POST"])
def add_elemento(request):
    """Adiciona um novo elemento."""
    logger.info("API add new elemento.")
    body = json.loads(request.body)
    
    elemento = body.get("elemento", "")
    descricao = body.get("descricao", "")

    try:
        new_elemento = service.add_elemento(
            elemento=elemento,
            descricao=descricao
        )
        return JsonResponse(new_elemento, status=201)
    except BusinessError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        logger.error(f"Erro ao adicionar elemento: {str(e)}")
        return JsonResponse({"error": "Erro interno do servidor"}, status=500)

@csrf_exempt
@ajax_login_required
@require_http_methods(["PUT"])
def update_elemento(request):
    """Atualiza um elemento existente."""
    logger.info("API update elemento.")
    body = json.loads(request.body)
    
    elemento_id = body.get("id")
    elemento = body.get("elemento", "")
    descricao = body.get("descricao", "")

    try:
        updated_elemento = service.update_elemento(
            elemento_id=elemento_id,
            elemento=elemento,
            descricao=descricao
        )
        return JsonResponse(updated_elemento, status=200)
    except BusinessError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        logger.error(f"Erro ao atualizar elemento: {str(e)}")
        return JsonResponse({"error": "Erro interno do servidor"}, status=500)

@csrf_exempt
@ajax_login_required
@require_http_methods(["DELETE"])
def delete_elemento(request, id):
    """Deleta um elemento."""
    logger.info(f"API delete elemento {id}.")
    
    try:
        service.delete_elemento(id)
        return JsonResponse({}, status=204)
    except BusinessError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        logger.error(f"Erro ao deletar elemento: {str(e)}")
        return JsonResponse({"error": "Erro interno do servidor"}, status=500)

@csrf_exempt
@ajax_login_required
@require_http_methods(["POST"])
def add_tipo_gasto(request):
    """Adiciona um novo tipo de gasto."""
    logger.info("API add new tipo_gasto.")
    body = json.loads(request.body)
    
    tipo_gasto = body.get("tipoGasto", "")
    descricao = body.get("descricao", "")

    try:
        new_tipo_gasto = service.add_tipo_gasto(
            tipo_gasto=tipo_gasto,
            descricao=descricao
        )
        return JsonResponse(new_tipo_gasto, status=201)
    except BusinessError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        logger.error(f"Erro ao adicionar tipo de gasto: {str(e)}")
        return JsonResponse({"error": "Erro interno do servidor"}, status=500)

@csrf_exempt
@ajax_login_required
@require_http_methods(["PUT"])
def update_tipo_gasto(request):
    """Atualiza um tipo de gasto existente."""
    logger.info("API update tipo_gasto.")
    body = json.loads(request.body)
    
    tipo_gasto_id = body.get("id")
    tipo_gasto = body.get("tipoGasto", "")
    descricao = body.get("descricao", "")

    try:
        updated_tipo_gasto = service.update_tipo_gasto(
            tipo_gasto_id=tipo_gasto_id,
            tipo_gasto=tipo_gasto,
            descricao=descricao
        )
        return JsonResponse(updated_tipo_gasto, status=200)
    except BusinessError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        logger.error(f"Erro ao atualizar tipo de gasto: {str(e)}")
        return JsonResponse({"error": "Erro interno do servidor"}, status=500)

@csrf_exempt
@ajax_login_required
@require_http_methods(["DELETE"])
def delete_tipo_gasto(request, id):
    """Deleta um tipo de gasto."""
    logger.info(f"API delete tipo_gasto {id}.")
    
    try:
        service.delete_tipo_gasto(id)
        return JsonResponse({}, status=204)
    except BusinessError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        logger.error(f"Erro ao deletar tipo de gasto: {str(e)}")
        return JsonResponse({"error": "Erro interno do servidor"}, status=500)

@csrf_exempt
@ajax_login_required
@require_http_methods(["POST"])
def add_elemento_tipo_gasto(request):
    """Adiciona um relacionamento entre elemento e tipo de gasto."""
    logger.info("API add elemento_tipo_gasto.")
    body = json.loads(request.body)
    
    elemento_id = body.get("elemento_id")
    tipo_gasto_id = body.get("tipo_gasto_id")

    try:
        new_relacao = service.add_elemento_tipo_gasto(
            elemento_id=elemento_id,
            tipo_gasto_id=tipo_gasto_id
        )
        return JsonResponse(new_relacao, status=201)
    except BusinessError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        logger.error(f"Erro ao adicionar relacionamento: {str(e)}")
        return JsonResponse({"error": "Erro interno do servidor"}, status=500)

@csrf_exempt
@ajax_login_required
@require_http_methods(["DELETE"])
def delete_elemento_tipo_gasto(request, id):
    """Deleta um relacionamento entre elemento e tipo de gasto."""
    logger.info(f"API delete elemento_tipo_gasto {id}.")
    
    try:
        service.delete_elemento_tipo_gasto(id)
        return JsonResponse({}, status=204)
    except BusinessError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        logger.error(f"Erro ao deletar relacionamento: {str(e)}")
        return JsonResponse({"error": "Erro interno do servidor"}, status=500)

@csrf_exempt
@ajax_login_required
@require_http_methods(["GET"])
def total_despesas_departamento_elemento(request, departamento_id, elemento_id):
    """Retorna o total de despesas de um departamento para um elemento específico."""
    logger.info(f"API total despesas departamento {departamento_id} elemento {elemento_id}")
    
    try:
        total = service.total_despesas_departamento_elemento(departamento_id, elemento_id)
        return JsonResponse({"total_despesas": float(total)}, status=200)
    except BusinessError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        logger.error(f"Erro ao buscar total de despesas do departamento por elemento: {str(e)}")
        return JsonResponse({"error": "Erro interno do servidor"}, status=500)