import pytest

from gfinancas4.core.models import Departamento
from gfinancas4.core.service import departamentos_svc
from gfinancas4.base.exceptions import BusinessError


@pytest.mark.django_db
def test_deve_inserir_uma_nova_tarefa():
    new_item = departamentos_svc.add_departamento("ABC")

    item = Departamento.objects.all().first()

    assert item.id == new_item.get("id")
    assert item.description == new_item.get("description")


@pytest.mark.django_db
def test_deve_retornar_um_erro_ao_cadastrar_item_sem_descricao():
    # Quando tentamos adicionar item sem valor
    with pytest.raises(BusinessError) as error:
        new_item = departamentos_svc.add_departamento(None)

    # Então
    assert str(error.value) == "Invalid description"


@pytest.mark.django_db
def test_deve_retornar_um_erro_ao_cadastrar_item_com_espacos_na_descricao():
    # Quando tentamos adicionar item sem valor
    with pytest.raises(BusinessError) as error:
        new_item = departamentos_svc.add_departamento("    ")

    # Então
    assert str(error.value) == "Invalid description"


@pytest.mark.django_db
def test_deve_aceitar_apenas_tipo_string_na_descricao():
    # Quando tentamos adicionar item sem valor
    with pytest.raises(BusinessError) as error:
        new_item = departamentos_svc.add_departamento(1000)

    # Então
    assert str(error.value) == "Invalid description"
