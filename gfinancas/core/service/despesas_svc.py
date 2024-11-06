import logging
from ..models import Despesa, Elemento, Departamento, TipoGasto
from ...accounts.models import User
from gfinancas.base.exceptions import BusinessError

logger = logging.getLogger(__name__)

# Função para adicionar uma Despesa
def add_despesa(user_id, valor, elemento_id, tipo_gasto_id, departamento_id, justificativa):
    logger.info("SERVICE add new despesa")
    
    # Verificar se os parâmetros são válidos
    try:
        departamento = Departamento.objects.get(id=departamento_id)
        user = User.objects.get(id=user_id)
        elemento = Elemento.objects.get(id=elemento_id)
        tipo_gasto = TipoGasto.objects.get(id=tipo_gasto_id)
    except (Departamento.DoesNotExist, User.DoesNotExist, Elemento.DoesNotExist, TipoGasto.DoesNotExist):
        raise BusinessError("Invalid references to Departamento, User, Elemento or TipoGasto")
    
    despesa = Despesa(
        IdUser=user,
        Valor=valor,
        IdElemento=elemento,
        IdTipoGasto=tipo_gasto,
        IdDepartamento=departamento,
        Justificativa=justificativa,
    )
    despesa.save()
    logger.info("SERVICE despesa created.")
    return despesa.to_dict_json()