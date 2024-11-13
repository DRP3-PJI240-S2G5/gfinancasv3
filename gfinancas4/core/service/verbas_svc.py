from ..models import Verba

def add_verba(departamento, user, descricao):
    verba = Verba(
        departamento=departamento,
        user=user,
        descricao=descricao
    )
    verba.save()
    return verba.to_dict_json()

def list_verbas():
    return [vb.to_dict_json() for vb in Verba.objects.all()]
