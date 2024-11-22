from ..models import Verba

def add_verba(valor, departamento, user, descricao):
    verba = Verba(
        valor=valor,
        departamento=departamento,
        user=user,
        descricao=descricao
    )
    verba.save()
    return verba.to_dict_json()

def list_verbas():
    return [vb.to_dict_json() for vb in Verba.objects.all()]
