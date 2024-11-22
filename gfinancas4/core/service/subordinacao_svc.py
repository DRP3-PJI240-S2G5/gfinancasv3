import logging
from ..models import Subordinacao, Departamento

logger = logging.getLogger(__name__)

def add_subordinacao(departamento_a: Departamento, departamento_b: Departamento, observacao: str = "") -> dict:
    """Cria uma relação de subordinação entre dois departamentos."""
    logger.info(f"SERVICE add subordinacao: {departamento_b.id} subordinado a {departamento_a.id}")
    
    # Verifica se a relação já existe
    if Subordinacao.objects.filter(IdDepartamentoA=departamento_a, IdDepartamentoB=departamento_b).exists():
        raise ValueError("Essa relação de subordinação já existe.")
    
    subordinacao = Subordinacao(
        IdDepartamentoA=departamento_a,
        IdDepartamentoB=departamento_b,
        Observacao=observacao
    )
    subordinacao.save()
    
    logger.info(f"Relação de subordinação criada: {subordinacao}")
    return subordinacao.to_dict_json()

def list_subordinacoes() -> list[dict]:
    """Busca e retorna todas as relações de subordinação no formato JSON."""
    logger.info("SERVICE list subordinacoes")
    subordinacoes = Subordinacao.objects.all()
    return [sub.to_dict_json() for sub in subordinacoes]