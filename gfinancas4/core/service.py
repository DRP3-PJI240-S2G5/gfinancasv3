import logging
from decimal import Decimal
from typing import List, Dict
from .models import (
    Departamento, Responsabilidade, Verba, Elemento, TipoGasto, Despesa, Subordinacao
)
from ..accounts.models import User
from gfinancas4.base.exceptions import BusinessError

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
def add_despesa(user: User, departamento: Departamento, valor: Decimal, elemento: Elemento, tipo_gasto: TipoGasto, justificativa: str) -> dict:
    logger.info(f"SERVICE add despesa: {valor} para o departamento {departamento.id}")
    if valor <= 0:
        raise BusinessError("O valor da despesa deve ser maior que zero.")
    despesa = Despesa(
        user=user,
        departamento=departamento,
        valor=valor,
        elemento=elemento,
        tipoGasto=tipo_gasto,
        justificativa=justificativa
    )
    despesa.save()
    return despesa.to_dict_json()

def update_despesa(despesa: Despesa, valor: float = None, justificativa: str = None) -> dict:
    """Atualiza os valores ou justificativa de uma despesa."""
    logger.info(f"SERVICE update despesa: {despesa.id}")
    
    if not despesa.pk:
        raise BusinessError("Despesa não encontrada para atualização.")
    
    if valor is not None:
        if valor <= 0:
            raise BusinessError("O valor da despesa deve ser maior que zero.")
        despesa.valor = valor
    if justificativa:
        despesa.justificativa = justificativa
    
    despesa.save()
    return despesa.to_dict_json()

def list_despesas() -> List[dict]:
    logger.info("SERVICE list despesas")
    return [desp.to_dict_json() for desp in Despesa.objects.all()]

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

def list_tipos_gasto() -> List[dict]:
    logger.info("SERVICE list tipos_gasto")
    return [tg.to_dict_json() for tg in TipoGasto.objects.all()]