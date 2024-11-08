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

def update_tipo_gasto(tipo_gasto_id, new_descricao):
    logger.info("SERVICE update tipo gasto")

    try:
        tipo_gasto = TipoGasto.objects.get(id=tipo_gasto_id)
    except TipoGasto.DoesNotExist:
        raise BusinessError("TipoGasto not found")

    tipo_gasto.descricao = new_descricao
    tipo_gasto.save()
    logger.info("SERVICE tipo gasto updated.")
    return tipo_gasto.to_dict_json()

def list_tipos_gastos():
    logger.info("SERVICE list tipos de gasto")
    tipos_gastos_list = TipoGasto.objects.all()
    return [item.to_dict_json() for item in tipos_gastos_list]