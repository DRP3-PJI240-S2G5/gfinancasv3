import logging
from ..models import Verba, Departamento
from ...accounts.models import User
from gfinancas.base.exceptions import BusinessError

logger = logging.getLogger(__name__)

# Função para adicionar uma Verba
def add_verba(departamento_id, user_id, descricao):
    logger.info("SERVICE add new verba")
    
    try:
        departamento = Departamento.objects.get(id=departamento_id)
        user = User.objects.get(id=user_id)
    except (Departamento.DoesNotExist, User.DoesNotExist):
        raise BusinessError("Invalid references to Departamento or User")
    
    verba = Verba(IdDepartamento=departamento, IdUser=user, descricao=descricao)
    verba.save()
    logger.info("SERVICE verba created.")
    return verba.to_dict_json()

def update_verba(verba_id, new_departamento_id=None, new_user_id=None, new_descricao=None):
    logger.info("SERVICE update verba")

    try:
        verba = Verba.objects.get(id=verba_id)
    except Verba.DoesNotExist:
        raise BusinessError("Verba not found")

    # Atualiza os campos fornecidos
    if new_departamento_id:
        verba.IdDepartamento_id = new_departamento_id
    if new_user_id:
        verba.IdUser_id = new_user_id
    if new_descricao:
        verba.descricao = new_descricao

    verba.save()
    logger.info("SERVICE verba updated.")
    return verba.to_dict_json()

def list_verbas():
    logger.info("SERVICE list verbas")
    verbas_list = Verba.objects.all()
    return [item.to_dict_json() for item in verbas_list]
