from ..models import User, Despesa, Elemento, Departamento, TipoGasto
from gfinancas4.base.exceptions import BusinessError

def add_despesa(user, departamento, valor, elemento, tipo_gasto, justificativa) -> dict:
    # Verificar campos obrigatórios
    if not all([user.id, valor, elemento.id, tipo_gasto.id, departamento.id, justificativa]):
        raise BusinessError("Todos os campos obrigatórios devem ser preenchidos.")

    # Verificar se o valor é válido
    if valor <= 0:
        raise BusinessError("O valor da despesa deve ser maior que zero.")
    
    despesa = Despesa(
        user=user,
        departamento=departamento,
        valor=valor,
        elemento=elemento,
        tipo_gasto=tipo_gasto,
        justificativa=justificativa
    )
    despesa.save()
    return despesa.to_dict_json()

def list_despesas() -> list[dict]:
    return [desp.to_dict_json() for desp in Despesa.objects.all()]
