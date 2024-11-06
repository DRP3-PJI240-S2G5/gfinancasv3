import logging
from ..models import Elemento
from gfinancas.base.exceptions import BusinessError

logger = logging.getLogger(__name__)

# Função para adicionar um Elemento
def add_elemento(nome):
    logger.info("SERVICE add new elemento")
    if not nome or not isinstance(nome, str):
        raise BusinessError("Invalid name for Elemento")
    
    elemento = Elemento(nome=nome)
    elemento.save()
    logger.info("SERVICE elemento created.")
    return elemento.to_dict_json()
