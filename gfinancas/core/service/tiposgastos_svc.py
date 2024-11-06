import logging
from ..models import TipoGasto
from gfinancas.base.exceptions import BusinessError

logger = logging.getLogger(__name__)

# Função para adicionar um TipoGasto
def add_tipo_gasto(descricao):
    logger.info("SERVICE add new tipo de gasto")
    if not descricao or not isinstance(descricao, str):
        raise BusinessError("Invalid description for TipoGasto")
    
    tipo_gasto = TipoGasto(descricao=descricao)
    tipo_gasto.save()
    logger.info("SERVICE tipo de gasto created.")
    return tipo_gasto.to_dict_json()
