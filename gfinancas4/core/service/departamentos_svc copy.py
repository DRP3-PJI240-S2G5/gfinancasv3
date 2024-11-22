import logging
from typing import List, Dict
from ..models import Departamento
from ...accounts.models import User
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
