import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError
from ..models import Departamento
from ..service import (
    add_departamento, update_departamento, delete_departamento, list_departamentos
)
from gfinancas4.base.exceptions import BusinessError
from gfinancas4.accounts.models import User

@pytest.mark.django_db
class TestDepartamentoServices:
    def test_add_departamento_success(self):
        # Criar um usuário responsável primeiro
        responsavel = User.objects.create_user(username="testuser", password="testpass")
        
        # Teste de adição bem sucedida
        departamento = add_departamento("Teste", "Descrição teste", "Entidade", responsavel.id)
        assert departamento["nome"] == "Teste"
        assert departamento["description"] == "Descrição teste"
        assert departamento["tipoEntidade"] == "Entidade"
        assert departamento["responsavelId"] == responsavel.id
        assert departamento["done"] == False
        assert Departamento.objects.count() == 1

    def test_add_departamento_responsavel_not_found(self):
        # Teste de adição com responsável inexistente
        with pytest.raises(BusinessError) as exc:
            add_departamento("Teste", "Descrição teste", "Entidade", 999)
        assert "Responsável com ID 999 não encontrado" in str(exc.value)

    def test_update_departamento_success(self):
        # Criar um usuário responsável primeiro
        responsavel = User.objects.create_user(username="testuser", password="testpass")
        
        # Criar departamento inicial
        departamento = add_departamento("Teste", "Descrição teste", "Entidade", responsavel.id)
        
        # Teste de atualização bem sucedida
        updated = update_departamento(
            departamento["id"], 
            nome="Teste Atualizado", 
            description="Nova descrição",
            tipoEntidade="Nova Entidade"
        )
        assert updated["nome"] == "Teste Atualizado"
        assert updated["description"] == "Nova descrição"
        assert updated["tipoEntidade"] == "Nova Entidade"
        assert updated["responsavelId"] == responsavel.id

    def test_update_departamento_not_found(self):
        # Teste de atualização de departamento inexistente
        with pytest.raises(BusinessError) as exc:
            update_departamento(999, nome="Teste")
        assert "Departamento com ID 999 não encontrado" in str(exc.value)

    def test_update_departamento_responsavel_not_found(self):
        # Criar um usuário responsável primeiro
        responsavel = User.objects.create_user(username="testuser", password="testpass")
        
        # Criar departamento inicial
        departamento = add_departamento("Teste", "Descrição teste", "Entidade", responsavel.id)
        
        # Teste de atualização com responsável inexistente
        with pytest.raises(BusinessError) as exc:
            update_departamento(departamento["id"], responsavelId=999)
        assert "Responsável com ID 999 não encontrado" in str(exc.value)

    def test_delete_departamento_success(self):
        # Criar um usuário responsável primeiro
        responsavel = User.objects.create_user(username="testuser", password="testpass")
        
        # Criar departamento
        departamento = add_departamento("Teste", "Descrição teste", "Entidade", responsavel.id)
        
        # Teste de exclusão bem sucedida
        delete_departamento(departamento["id"])
        assert Departamento.objects.count() == 0

    def test_delete_departamento_not_found(self):
        # Teste de exclusão de departamento inexistente
        with pytest.raises(BusinessError) as exc:
            delete_departamento(999)
        assert "Departamento com ID 999 não encontrado" in str(exc.value)

    def test_list_departamentos(self):
        # Criar um usuário responsável primeiro
        responsavel = User.objects.create_user(username="testuser", password="testpass")
        
        # Criar departamentos
        add_departamento("Teste1", "Descrição 1", "Entidade1", responsavel.id)
        add_departamento("Teste2", "Descrição 2", "Entidade2", responsavel.id)
        
        # Teste de listagem
        departamentos = list_departamentos()
        assert len(departamentos) == 2
        assert departamentos[0]["nome"] == "Teste1"
        assert departamentos[1]["nome"] == "Teste2" 