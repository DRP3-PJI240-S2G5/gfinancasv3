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

def update_elemento(elemento_id, new_nome):
    logger.info("SERVICE update elemento")

    try:
        elemento = Elemento.objects.get(id=elemento_id)
    except Elemento.DoesNotExist:
        raise BusinessError("Elemento not found")

    elemento.nome = new_nome
    elemento.save()
    logger.info("SERVICE elemento updated.")
    return elemento.to_dict_json()

def list_elementos():
    logger.info("SERVICE list elementos")
    elementos_list = Elemento.objects.all()
    return [item.to_dict_json() for item in elementos_list]