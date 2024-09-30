import pytest
from unittest.mock import ANY

from gfinancas.core.models import Departamento


def test_nao_deve_permitir_listar_departamento_sem_login(client):
    # Dado um usuário anônimo

    # Quando tentamos listar itens
    resp = client.get("/api/core/departamentos/list")

    # Entao recebemos um sem autorizacao
    assert resp.status_code == 401


@pytest.mark.django_db
def test_deve_retornar_lista_vazia(client, logged_jon):
    # Quando tentamos listar itens
    resp = client.get("/api/core/departamentos/list")
    data = resp.json()

    # Entao recebemos um sem autorizacao
    assert resp.status_code == 200
    assert data.get("departamentos") == []


@pytest.mark.django_db
def test_deve_listar_departamento_com_login(client, logged_jon):
    # Dado um item criado
    Departamento.objects.create(description="walk the dog")

    # Quando listamos
    resp = client.get("/api/core/departamentos/list")
    data = resp.json()

    # Entao
    assert resp.status_code == 200
    assert data == {
        "departamentos": [{"description": "walk the dog", "done": False, "id": ANY}]
    }
