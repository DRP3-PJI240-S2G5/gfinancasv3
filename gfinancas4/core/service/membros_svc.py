import logging

from ..models import MembroDepartamento
from gfinancas4.base.exceptions import BusinessError

logger = logging.getLogger(__name__)

def add_membro(new_membro: MembroDepartamento) -> MembroDepartamento:
    """Adiciona um novo membro a um departamento."""
    logger.info("SERVICE add new membro")
    
    if not isinstance(new_membro, MembroDepartamento):
        raise BusinessError(f"Expected instance of MembroDepartamento, but got {type(new_membro)}")
    
    try:
        new_membro.save()
        logger.info(f"Membro {new_membro.usuario.id} adicionado ao departamento {new_membro.departamento.id}.")
        return new_membro
    except Exception as e:
        logger.error(f"Erro ao adicionar membro: {str(e)}")
        raise BusinessError("Erro ao adicionar o membro ao departamento.")

def remove_membro(membro: MembroDepartamento) -> None:
    """Remove um membro de um departamento."""
    logger.info("SERVICE remove membro")
    
    if not isinstance(membro, MembroDepartamento):
        raise BusinessError(f"Expected instance of MembroDepartamento, but got {type(membro)}")
    
    try:
        membro.delete()
        logger.info(f"Membro {membro.id} removido com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao remover membro: {str(e)}")
        raise BusinessError("Erro ao remover o membro do departamento.")

def list_membros(departamento) -> list:
    """Lista todos os membros de um departamento."""
    logger.info("SERVICE list membros")
    
    if not departamento:
        raise BusinessError("Departamento inválido ou não fornecido.")
    
    membros = MembroDepartamento.objects.filter(departamento=departamento)
    logger.info(f"{membros.count()} membros encontrados para o departamento {departamento.id}.")
    return list(membros)

def get_membro_by_id(membro_id: int) -> MembroDepartamento:
    """Obtém um membro pelo ID."""
    logger.info(f"SERVICE get membro by ID: {membro_id}")
    
    try:
        membro = MembroDepartamento.objects.get(id=membro_id)
        return membro
    except MembroDepartamento.DoesNotExist:
        logger.error(f"Membro com ID {membro_id} não encontrado.")
        raise BusinessError(f"Membro com ID {membro_id} não encontrado.")
