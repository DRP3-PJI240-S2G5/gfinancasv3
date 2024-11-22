import logging
from typing import List, Dict
from .models import Departamento, Responsabilidade, Verba, Elemento, TipoGasto, Despesa, Subordinacao
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
    
    # Verifica se o responsável (User) existe com o ID fornecido
    responsavel = User.objects.filter(id=departamento.responsavelId.id).first()
    
    try:
        departamento.save()
        logger.info(f"Departamento {departamento.id} atualizado com sucesso.")
    except Exception as e:
        raise ValueError(f"UPDATE_VIEW_Erro ao atualizar o departamento: {str(e)}")
    
    return departamento.to_dict_json()

def list_departamentos() -> List[dict]:
    logger.info("SERVICE list departamentos")
    
    departamentos_list = Departamento.objects.all()
    return [item.to_dict_json() for item in departamentos_list]

def add_despesa(user, departamento, valor, elemento, tipo_gasto, justificativa) -> dict:
    # Verificar campos obrigatórios
    if not all([user.id, valor, elemento.id, tipo_gasto.id, departamento.id, justificativa]):
        raise BusinessError("Todos os campos obrigatórios devem ser preenchidos.")

    # Verificar se o valor é válido
    if valor <= 0:
        raise BusinessError("O valor da despesa deve ser maior que zero.")
    
    despesa = Despesa(
        user=user,
        departamento=departamento,
        valor=valor,
        elemento=elemento,
        tipo_gasto=tipo_gasto,
        justificativa=justificativa
    )
    despesa.save()
    return despesa.to_dict_json()

def list_despesas() -> list[dict]:
    return [desp.to_dict_json() for desp in Despesa.objects.all()]

def add_subordinacao(departamento_a: Departamento, departamento_b: Departamento, observacao: str = "") -> dict:
    """Cria uma relação de subordinação entre dois departamentos."""
    logger.info(f"SERVICE add subordinacao: {departamento_b.id} subordinado a {departamento_a.id}")
    
    # Verifica se a relação já existe
    if Subordinacao.objects.filter(IdDepartamentoA=departamento_a, IdDepartamentoB=departamento_b).exists():
        raise ValueError("Essa relação de subordinação já existe.")
    
    subordinacao = Subordinacao(
        IdDepartamentoA=departamento_a,
        IdDepartamentoB=departamento_b,
        Observacao=observacao
    )
    subordinacao.save()
    
    logger.info(f"Relação de subordinação criada: {subordinacao}")
    return subordinacao.to_dict_json()

def list_subordinacoes() -> list[dict]:
    """Busca e retorna todas as relações de subordinação no formato JSON."""
    logger.info("SERVICE list subordinacoes")
    subordinacoes = Subordinacao.objects.all()
    return [sub.to_dict_json() for sub in subordinacoes]


def add_verba(valor, departamento, user, descricao) -> dict:
    verba = Verba(
        valor=valor,
        departamento=departamento,
        user=user,
        descricao=descricao
    )
    verba.save()
    return verba.to_dict_json()

def list_verbas() -> list[dict]:
    logger.info("SERVICE list verbas")
    return [vb.to_dict_json() for vb in Verba.objects.all()]
