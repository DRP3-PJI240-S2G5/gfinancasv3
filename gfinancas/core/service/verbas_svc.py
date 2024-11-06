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
