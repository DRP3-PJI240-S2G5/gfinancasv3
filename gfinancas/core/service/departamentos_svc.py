import logging

from ..models import Departamento
from gfinancas.base.exceptions import BusinessError

logger = logging.getLogger(__name__)


def add_departamento(new_departamento: str) -> dict:
    logger.info("SERVICE add new departamento")
    if not isinstance(new_departamento, str):
        raise BusinessError("Invalid description")

    if not new_departamento or not new_departamento.strip():
        raise BusinessError("Invalid description")

    departamento = Departamento(description=new_departamento)
    departamento.save()
    logger.info("SERVICE departamento created.")
    return departamento.to_dict_json()


def list_departamentos():
    logger.info("SERVICE list departamentos")
    departamentos_list = Departamento.objects.all()
    return [item.to_dict_json() for item in departamentos_list]
