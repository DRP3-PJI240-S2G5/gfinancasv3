import logging
from ..models import Departamento
from ...accounts.models import User
from gfinancas.base.exceptions import BusinessError

logger = logging.getLogger(__name__)


def add_departamento(nome: str, description: str, tipo_entidade: str, responsavel_id: int, done: bool = False) -> dict:
    logger.info("SERVICE add new departamento")
    
    # Validação básica para os campos
    if not isinstance(nome, str) or not nome.strip():
        raise BusinessError("Invalid nome")
    
    if len(nome.strip()) <= 2:  # Exemplo de limite mínimo de 3 caracteres para nome
        raise BusinessError("Nome must be at least 3 characters long")
    
    if not isinstance(description, str) or not description.strip():
        raise BusinessError("Invalid description")
    
    if not isinstance(tipo_entidade, str) or not tipo_entidade.strip():
        raise BusinessError("Invalid tipo_entidade")
    
    if not isinstance(responsavel_id, int) or responsavel_id <= 0:
        raise BusinessError("Invalid responsavel_id")

    # Verifica se o responsável existe
    try:
        responsavel = User.objects.get(id=responsavel_id)
    except User.DoesNotExist:
        raise BusinessError("Responsável not found")

    # Criação do novo departamento
    departamento = Departamento(
        Nome=nome,
        description=description,
        TipoEntidade=tipo_entidade,
        IdUserResp=responsavel,
        done=done
    )
    departamento.save()
    logger.info("SERVICE departamento created.")
    
    return departamento.to_dict_json()


def update_departamento(departamento_id, new_nome=None, new_description=None, new_tipo_entidade=None, new_responsavel_id=None, new_done=None):
    logger.info("SERVICE update departamento")
    
    # Verifica se o departamento existe
    try:
        departamento = Departamento.objects.get(id=departamento_id)
    except Departamento.DoesNotExist:
        raise BusinessError("Departamento not found")

    # Atualiza os campos fornecidos
    if new_nome is not None:
        if not isinstance(new_nome, str) or not new_nome.strip():
            raise BusinessError("Invalid nome")
        if len(new_nome.strip()) <= 2:  # Limite mínimo de 3 caracteres
            raise BusinessError("Nome must be at least 3 characters long")
        departamento.Nome = new_nome

    if new_description is not None:
        if not isinstance(new_description, str) or not new_description.strip():
            raise BusinessError("Invalid description")
        if len(new_description.strip()) <= 2:  # Exemplo de validação mínima
            raise BusinessError("Description must be at least 3 characters long")
        departamento.description = new_description

    if new_tipo_entidade is not None:
        if not isinstance(new_tipo_entidade, str) or not new_tipo_entidade.strip():
            raise BusinessError("Invalid tipo_entidade")
        departamento.TipoEntidade = new_tipo_entidade

    if new_responsavel_id is not None:
        if not isinstance(new_responsavel_id, int) or new_responsavel_id <= 0:
            raise BusinessError("Invalid IdUserResp")
        
        # Verifica se o responsável existe
        try:
            IdUserResp = User.objects.get(id=new_responsavel_id)
        except User.DoesNotExist:
            raise BusinessError("Responsável not found")
        
        departamento.IdUserResp = IdUserResp

    if new_done is not None:
        if not isinstance(new_done, bool):
            raise BusinessError("Invalid done value")
        departamento.done = new_done
    
    departamento.save()
    logger.info("SERVICE departamento updated.")
    return departamento.to_dict_json()

def list_departamentos():
    logger.info("SERVICE list departamentos")
    departamentos_list = Departamento.objects.all()
    return [item.to_dict_json() for item in departamentos_list]