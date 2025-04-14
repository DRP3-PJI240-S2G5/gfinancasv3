import logging
from decimal import Decimal
from django.core.paginator import Paginator
from typing import List, Dict
from .models import (
    Departamento, Responsabilidade, Verba, Elemento, TipoGasto, Despesa, Subordinacao, ElementoTipoGasto
)
from ..accounts.models import User
from gfinancas4.base.exceptions import BusinessError
from django.core.exceptions import ValidationError
from decimal import Decimal

logger = logging.getLogger(__name__)


def add_departamento(new_departamento: Departamento) -> dict:
    logger.info("SERVICE add new departamento")
    
    if not isinstance(new_departamento, Departamento):
        raise BusinessError(f"Expected instance of Departamento, but got {type(new_departamento)}")
    
    new_departamento.save()
    logger.info("SERVICE departamento created.")

    return new_departamento.to_dict_json()

def update_departamento(departamento: Departamento) -> dict:
    """Atualiza um departamento com os dados do objeto fornecido."""
    logger.info("SERVICE upudate departamento")
    
    if not departamento.pk:  # Verifica se o departamento tem um ID válido (caso seja um objeto novo, ele não teria um ID ainda)
        raise BusinessError("UPDATE_VIEW: Departamento não encontrado para atualização")
    
    departamento.save()
    logger.info(f"Departamento {departamento.id} atualizado com sucesso.")
    return departamento.to_dict_json()

def list_departamentos() -> List[dict]:
    logger.info("SERVICE list departamentos")
    return [item.to_dict_json() for item in Departamento.objects.all()]

def add_subordinacao(superior: Departamento, subordinado: Departamento, observacao: str = "") -> dict:
    logger.info(f"SERVICE add subordinacao: {subordinado.id} subordinado a {superior.id}")
    
    if Subordinacao.objects.filter(superior=superior, subordinado=subordinado).exists():
        raise BusinessError("Essa relação de subordinação já existe.")
    
    subordinacao = Subordinacao(
        superior=superior, 
        subordinado=subordinado, 
        observacao=observacao)
    
    subordinacao.save()
    return subordinacao.to_dict_json()

def update_subordinacao(subordinacao: Subordinacao, observacao: str) -> dict:
    """Atualiza a observação de uma subordinação existente."""
    logger.info(f"SERVICE update subordinacao: {subordinacao.id}")
    
    if not subordinacao.pk:
        raise BusinessError("Subordinação não encontrada para atualização.")
    
    subordinacao.observacao = observacao
    subordinacao.save()
    return subordinacao.to_dict_json()

def list_subordinacoes() -> list[dict]:
    """Busca e retorna todas as relações de subordinação no formato JSON."""
    logger.info("SERVICE list subordinacoes")
    return [sub.to_dict_json() for sub in Subordinacao.objects.all()]

# SERVIÇOS PARA RESPONSABILIDADES (implementados conforme modelo e práticas)
def add_responsabilidade(usuario: User, departamento: Departamento, observacao: str = "") -> dict:
    logger.info(f"SERVICE add responsabilidade: {usuario.id} responsável pelo {departamento.id}")
    if Responsabilidade.objects.filter(usuario=usuario, departamento=departamento).exists():
        raise BusinessError("O usuário já é responsável por este departamento.")
    responsabilidade = Responsabilidade(usuario=usuario, departamento=departamento, observacao=observacao)
    responsabilidade.save()
    return responsabilidade.to_dict_json()

def update_responsabilidade(responsabilidade: Responsabilidade, observacao: str = None) -> dict:
    """Atualiza a responsabilidade, alterando a observação."""
    logger.info(f"SERVICE update responsabilidade: {responsabilidade.id}")
    
    if not responsabilidade.pk:
        raise BusinessError("Responsabilidade não encontrada para atualização.")
    
    if observacao:
        responsabilidade.observacao = observacao
    
    responsabilidade.save()
    return responsabilidade.to_dict_json()

def list_responsabilidades() -> List[dict]:
    logger.info("SERVICE list responsabilidades")
    return [resp.to_dict_json() for resp in Responsabilidade.objects.all()]

# SERVIÇOS PARA VERBAS (ajustes e implementação faltante)
def add_verba(valor, departamento: Departamento, user: User, ano: int, descricao: str) -> dict:
    logger.info(f"SERVICE add verba: {valor} para {departamento.id} no ano {ano}")
    if Verba.objects.filter(departamento=departamento, ano=ano).exists():
        raise BusinessError("Já existe uma verba estipulada para este departamento neste ano.")
    
    if valor is not None:
        valor = Decimal(valor)

    verba = Verba(valor=valor, departamento=departamento, user=user, ano=ano, descricao=descricao)
    verba.save()
    return verba.to_dict_json()

def update_verba(verba: Verba, valor: Decimal = None, descricao: str = None) -> dict:
    """Atualiza os valores ou descrição de uma verba."""
    logger.info(f"SERVICE update verba: {verba.id}")
    
    if not verba.pk:
        raise BusinessError("Verba não encontrada para atualização.")
    
    if valor is not None:
        verba.valor = Decimal(valor)
    if descricao:
        verba.descricao = descricao
    
    verba.save()
    return verba.to_dict_json()

def list_verbas() -> List[dict]:
    logger.info("SERVICE list verbas")
    return [verba.to_dict_json() for verba in Verba.objects.all()]

# SERVIÇOS PARA DESPESAS (existentes e já adequados)
def add_despesa(nova_despesa: Despesa) -> dict:
    """
    Adiciona uma nova despesa.
    Espera uma instância de Despesa.
    """
    logger.info(f"SERVICE add despesa: {nova_despesa.valor} para o departamento {nova_despesa.departamento.id}")
    
    # Verificando se o valor da despesa é válido
    if nova_despesa.valor <= 0:
        raise BusinessError("O valor da despesa deve ser maior que zero.")
    
    nova_despesa.valor = round(Decimal(nova_despesa.valor), 2)
    logger.debug(f"valor: {nova_despesa.valor}")

    # Tentando salvar a despesa
    try:
        nova_despesa.save()
    except ValidationError as e:
        raise BusinessError(f"Error de validação: {e.messages}")
    
    # Retornando o dicionário com os dados da despesa
    return nova_despesa.to_dict_json()

def update_despesa(nova_despesa: Despesa) -> dict:
    """
    Atualiza os valores, justificativa, elemento e tipoGasto de uma despesa existente.
    Espera uma instância de Despesa.
    """
    logger.info(f"SERVICE update despesa: {nova_despesa.id}")
    
    if not nova_despesa.pk:
        raise BusinessError("Despesa não encontrada para atualização.")
    
    # Verificando e atualizando o valor, se fornecido
    if nova_despesa.valor is not None:
        if nova_despesa.valor <= 0:
            raise BusinessError("O valor da despesa deve ser maior que zero.")
        nova_despesa.valor = nova_despesa.valor
    
    # Atualizando a justificativa, se fornecida
    if nova_despesa.justificativa:
        nova_despesa.justificativa = nova_despesa.justificativa
    
    # Atualizando o elemento, se fornecido
    if nova_despesa.elemento:
        nova_despesa.elemento = nova_despesa.elemento
    
    # Atualizando o tipoGasto, se fornecido
    if nova_despesa.tipoGasto:
        nova_despesa.tipoGasto = nova_despesa.tipoGasto
    
    # Tentando salvar as alterações
    try:
        nova_despesa.save()
    except ValidationError as e:
        raise BusinessError(f"Erro de validação: {e.messages}")
    
    # Retornando o dicionário com os dados atualizados da despesa
    return nova_despesa.to_dict_json()

def list_despesas(page=1, per_page=10) -> List[dict]:
    """Retorna todas as despesas paginadas, independentemente do departamento."""
    despesas = Despesa.objects.select_related(
        'user', 'elemento', 'tipoGasto', 'departamento'
    ).order_by("-created_at")

    paginator = Paginator(despesas, per_page)
    page_obj = paginator.get_page(page)

    despesas_serializadas = [d.to_dict_json() for d in page_obj.object_list]

    return {
        "despesas": despesas_serializadas,
        "paginacao": {
            "pagina_atual": page_obj.number,
            "total_paginas": paginator.num_pages,
            "total_despesas": paginator.count,
            "tem_proxima": page_obj.has_next(),
            "tem_anterior": page_obj.has_previous(),
        }
    }

def list_despesas_departamento(departamento_id, page=1, per_page=10) -> List[dict]:
    """Retorna todas as despesas de um departamento específico com paginação."""
    try:
        departamento = Departamento.objects.get(id=departamento_id)
        
        # Filtra as despesas do departamento
        despesas = Despesa.objects.filter(departamento=departamento).select_related(
            'user', 'elemento', 'tipoGasto'
        ).order_by("-created_at")

        # Pagina as despesas
        paginator = Paginator(despesas, per_page)
        page_obj = paginator.get_page(page)

        # Serializa as despesas da página atual
        despesas_serializadas = [despesa.to_dict_json() for despesa in page_obj.object_list]

        # Retorna o resultado com a paginação
        return {
            "despesas": despesas_serializadas,
            "paginacao": {
                "pagina_atual": page_obj.number,
                "total_paginas": paginator.num_pages,
                "total_despesas": paginator.count,
                "tem_proxima": page_obj.has_next(),
                "tem_anterior": page_obj.has_previous(),
            }
        }

    except Departamento.DoesNotExist:
        raise ValueError("Departamento não encontrado")
    
# SERVIÇOS PARA ELEMENTOS (implementados conforme práticas)
def add_elemento(novo_elemento: str, descricao: str) -> dict:
    logger.info(f"SERVICE add elemento: {novo_elemento}")
    elemento = Elemento(elemento=novo_elemento, descricao=descricao)
    elemento.save()
    return elemento.to_dict_json()

def update_elemento(elemento: Elemento, descricao: str = None) -> dict:
    """Atualiza a descrição de um elemento existente."""
    logger.info(f"SERVICE update elemento: {elemento.id}")
    
    if not elemento.pk:
        raise BusinessError("Elemento não encontrado para atualização.")
    
    if descricao:
        elemento.descricao = descricao
    
    elemento.save()
    return elemento.to_dict_json()

def list_elementos() -> List[dict]:
    logger.info("SERVICE list elementos")
    return [el.to_dict_json() for el in Elemento.objects.all()]

# SERVIÇOS PARA TIPOS DE GASTO (implementados conforme práticas)
def add_tipo_gasto(novo_tipo_gasto: str, descricao: str) -> dict:
    logger.info(f"SERVICE add tipo_gasto: {novo_tipo_gasto}")
    tipo_gasto = TipoGasto(tipoGasto=novo_tipo_gasto, descricao=descricao)
    tipo_gasto.save()
    return tipo_gasto.to_dict_json()

def update_tipo_gasto(tipo_gasto: TipoGasto, descricao: str = None) -> dict:
    """Atualiza a descrição de um tipo de gasto existente."""
    logger.info(f"SERVICE update tipo_gasto: {tipo_gasto.id}")
    
    if not tipo_gasto.pk:
        raise BusinessError("Tipo de gasto não encontrado para atualização.")
    
    if descricao:
        tipo_gasto.descricao = descricao
    
    tipo_gasto.save()
    return tipo_gasto.to_dict_json()

def list_tipo_gastos() -> List[dict]:
    logger.info("SERVICE list tipos_gasto")
    return [tg.to_dict_json() for tg in TipoGasto.objects.all()]

def list_tipo_gastos_por_elemento(elemento_id: int) -> List[dict]:
    logger.info(f"SERVICE list tipos_gasto por elemento {elemento_id}")
    
    relacoes = ElementoTipoGasto.objects.filter(elemento_id=elemento_id).select_related("tipo_gasto")
    return [
        {
            "id": r.tipo_gasto.id,
            "tipoGasto": r.tipo_gasto.tipoGasto,
            "descricao": r.tipo_gasto.descricao,
        }
        for r in relacoes
    ]