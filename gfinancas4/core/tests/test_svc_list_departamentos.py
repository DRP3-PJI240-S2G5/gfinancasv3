import pytest

from gfinancas4.core.models import Departamento
import gfinancas4.core.service


@pytest.mark.django_db
def test_deve_retornar_lista_vazia():
    itens_list = departamentos_svc.list_departamentos()
    assert itens_list == []


@pytest.mark.django_db
def test_deve_listar_com_10_iten():
    # Dado 10 itens criados
    itens = [Departamento(description=f"Departamentos nro ${number}") for number in range(1, 11)]
    Departamento.objects.bulk_create(itens)

    itens_list = departamentos_svc.list_departamentos()

    assert len(itens_list) == 10
