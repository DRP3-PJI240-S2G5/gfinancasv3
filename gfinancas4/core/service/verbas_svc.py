import logging
from ..models import Verba

logger = logging.getLogger(__name__)

def add_verba(valor, departamento, user, descricao) -> dict:
    verba = Verba(
        valor=valor,
        departamento=departamento,
        user=user,
        descricao=descricao
    )
    verba.save()
    return verba.to_dict_json()

def list_verbas() -> list[dict]:
    logger.info("SERVICE list verbas")
    return [vb.to_dict_json() for vb in Verba.objects.all()]
