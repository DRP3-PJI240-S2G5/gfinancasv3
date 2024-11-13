from ..models import Subordinacao

def add_subordinacao(depto_a, depto_b, data_subordinacao, observacao=None):
    subordinacao = Subordinacao(
        id_departamento_a=depto_a,
        id_departamento_b=depto_b,
        data_subordinacao=data_subordinacao,
        observacao=observacao
    )
    subordinacao.save()
    return subordinacao.to_dict_json()

def list_subordinacoes():
    return [sub.to_dict_json() for sub in Subordinacao.objects.all()]