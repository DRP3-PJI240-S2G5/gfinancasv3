import json
import pytest
from django.urls import reverse
from gfinancas4.core.models import Departamento
from gfinancas4.accounts.models import User
from decimal import Decimal

@pytest.mark.django_db
class TestDepartamentoViews:
    def setup_method(self, method):
        """Configuração inicial para cada teste"""
        # Criar um usuário para autenticação
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )

    def test_add_departamento_success(self, client):
        """Testa a adição bem-sucedida de um departamento"""
        client.login(username='testuser', password='testpass123')
        url = reverse('add_departamento')
        data = {
            "nome": "Departamento Teste",
            "description": "Descrição do departamento teste",
            "tipoEntidade": "Entidade Teste",
            "responsavelId": self.user.id,
            "done": False
        }
        
        response = client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        response_data = json.loads(response.content)
        assert response_data["nome"] == data["nome"]
        assert response_data["description"] == data["description"]
        assert response_data["tipoEntidade"] == data["tipoEntidade"]
        assert response_data["responsavelId"] == self.user.id
        assert response_data["done"] == data["done"]

    def test_add_departamento_missing_fields(self, client):
        """Testa a adição de departamento com campos obrigatórios faltando"""
        client.login(username='testuser', password='testpass123')
        url = reverse('add_departamento')
        
        # Teste sem o campo nome
        data_sem_nome = {
            "description": "Descrição do departamento teste",
            "tipoEntidade": "Entidade Teste",
            "responsavelId": self.user.id
        }
        
        response = client.post(
            url,
            data=json.dumps(data_sem_nome),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        response_data = json.loads(response.content)
        assert "error" in response_data
        assert "O campo 'nome' é obrigatório" in response_data["error"]
        
        # Teste sem o campo description
        data_sem_description = {
            "nome": "Departamento Teste",
            "tipoEntidade": "Entidade Teste",
            "responsavelId": self.user.id
        }
        
        response = client.post(
            url,
            data=json.dumps(data_sem_description),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        response_data = json.loads(response.content)
        assert "error" in response_data
        assert "O campo 'description' é obrigatório" in response_data["error"]

    def test_update_departamento_success(self, client):
        """Testa a atualização bem-sucedida de um departamento"""
        client.login(username='testuser', password='testpass123')
        # Primeiro cria um departamento
        departamento = Departamento.objects.create(
            nome="Departamento Original",
            description="Descrição Original",
            tipoEntidade="Entidade Original",
            responsavelId=self.user,
            done=False
        )
        
        url = reverse('update_departamento')
        data = {
            "id": departamento.id,
            "nome": "Departamento Atualizado",
            "description": "Nova Descrição",
            "tipoEntidade": "Nova Entidade",
            "responsavelId": self.user.id,
            "done": True
        }
        
        response = client.put(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert response_data["nome"] == data["nome"]
        assert response_data["description"] == data["description"]
        assert response_data["tipoEntidade"] == data["tipoEntidade"]
        assert response_data["done"] == data["done"]

    def test_update_departamento_not_found(self, client):
        """Testa a atualização de um departamento inexistente"""
        client.login(username='testuser', password='testpass123')
        url = reverse('update_departamento')
        data = {
            "id": 999,  # ID inexistente
            "nome": "Departamento Atualizado",
            "description": "Nova Descrição",
            "tipoEntidade": "Nova Entidade",
            "responsavelId": self.user.id
        }
        
        response = client.put(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        response_data = json.loads(response.content)
        assert "error" in response_data

    def test_list_departamentos(self, client):
        """Testa a listagem de departamentos"""
        client.login(username='testuser', password='testpass123')
        # Criar alguns departamentos
        Departamento.objects.create(
            nome="Departamento 1",
            description="Descrição 1",
            tipoEntidade="Entidade 1",
            responsavelId=self.user,
            done=False
        )
        Departamento.objects.create(
            nome="Departamento 2",
            description="Descrição 2",
            tipoEntidade="Entidade 2",
            responsavelId=self.user,
            done=True
        )
        
        url = reverse('list_departamentos')
        response = client.get(url)
        
        assert response.status_code == 200
        response_data = json.loads(response.content)
        assert "departamentos" in response_data
        assert len(response_data["departamentos"]) == 2
        assert response_data["departamentos"][0]["nome"] == "Departamento 1"
        assert response_data["departamentos"][1]["nome"] == "Departamento 2"

    def test_add_departamento_unauthorized(self, client):
        """Testa a adição de departamento sem autenticação"""
        url = reverse('add_departamento')
        data = {
            "nome": "Departamento Teste",
            "description": "Descrição do departamento teste",
            "tipoEntidade": "Entidade Teste",
            "responsavelId": self.user.id,
            "done": False
        }
        
        response = client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 403  # Forbidden 