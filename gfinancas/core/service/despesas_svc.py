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

def update_despesa(despesa_id, new_user_id=None, new_valor=None, new_elemento_id=None, new_tipo_gasto_id=None, new_justificativa=None):
    logger.info("SERVICE update despesa")

    try:
        despesa = Despesa.objects.get(id=despesa_id)
    except Despesa.DoesNotExist:
        raise BusinessError("Despesa not found")

    # Atualiza os campos fornecidos
    if new_user_id:
        despesa.IdUser_id = new_user_id
    if new_valor is not None:
        despesa.Valor = new_valor
    if new_elemento_id:
        despesa.IdElemento_id = new_elemento_id
    if new_tipo_gasto_id:
        despesa.IdTipoGasto_id = new_tipo_gasto_id
    if new_justificativa:
        despesa.Justificativa = new_justificativa
    
    despesa.save()
    logger.info("SERVICE despesa updated.")
    return despesa.to_dict_json()

def list_despesas():
    logger.info("SERVICE list despesas")
    despesas_list = Despesa.objects.all()
    return [item.to_dict_json() for item in despesas_list]