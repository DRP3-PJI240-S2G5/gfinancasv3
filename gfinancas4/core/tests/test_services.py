import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError
from ..models import Elemento, TipoGasto, ElementoTipoGasto
from ..service import (
    add_elemento, update_elemento, delete_elemento, list_elementos,
    add_tipo_gasto, update_tipo_gasto, delete_tipo_gasto, list_tipo_gastos,
    add_elemento_tipo_gasto, delete_elemento_tipo_gasto, list_tipo_gastos_por_elemento
)
from gfinancas4.base.exceptions import BusinessError

@pytest.mark.django_db
class TestElementoServices:
    def test_add_elemento_success(self):
        # Teste de adição bem sucedida
        elemento = add_elemento("Teste", "Descrição teste")
        assert elemento["elemento"] == "Teste"
        assert elemento["descricao"] == "Descrição teste"
        assert Elemento.objects.count() == 1

    def test_add_elemento_duplicate(self):
        # Teste de adição com nome duplicado
        add_elemento("Teste", "Descrição teste")
        with pytest.raises(BusinessError) as exc:
            add_elemento("Teste", "Outra descrição")
        assert "Já existe um elemento com o nome" in str(exc.value)

    def test_add_elemento_empty_fields(self):
        # Teste de adição com campos vazios
        with pytest.raises(BusinessError) as exc:
            add_elemento("", "Descrição teste")
        assert "O campo 'elemento' é obrigatório" in str(exc.value)

        with pytest.raises(BusinessError) as exc:
            add_elemento("Teste", "")
        assert "O campo 'descricao' é obrigatório" in str(exc.value)

    def test_update_elemento_success(self):
        # Teste de atualização bem sucedida
        elemento = add_elemento("Teste", "Descrição teste")
        updated = update_elemento(elemento["id"], "Teste Atualizado", "Nova descrição")
        assert updated["elemento"] == "Teste Atualizado"
        assert updated["descricao"] == "Nova descrição"

    def test_update_elemento_not_found(self):
        # Teste de atualização de elemento inexistente
        with pytest.raises(BusinessError) as exc:
            update_elemento(999, "Teste", "Descrição")
        assert "Elemento com ID 999 não encontrado" in str(exc.value)

    def test_update_elemento_duplicate(self):
        # Teste de atualização com nome duplicado
        add_elemento("Teste1", "Descrição 1")
        elemento2 = add_elemento("Teste2", "Descrição 2")
        with pytest.raises(BusinessError) as exc:
            update_elemento(elemento2["id"], "Teste1", "Nova descrição")
        assert "Já existe um elemento com o nome" in str(exc.value)

    def test_delete_elemento_success(self):
        # Teste de exclusão bem sucedida
        elemento = add_elemento("Teste", "Descrição teste")
        delete_elemento(elemento["id"])
        assert Elemento.objects.count() == 0

    def test_delete_elemento_not_found(self):
        # Teste de exclusão de elemento inexistente
        with pytest.raises(BusinessError) as exc:
            delete_elemento(999)
        assert "Elemento com ID 999 não encontrado" in str(exc.value)

    def test_list_elementos(self):
        # Teste de listagem
        add_elemento("Teste1", "Descrição 1")
        add_elemento("Teste2", "Descrição 2")
        elementos = list_elementos()
        assert len(elementos) == 2
        assert elementos[0]["elemento"] == "Teste1"
        assert elementos[1]["elemento"] == "Teste2"

@pytest.mark.django_db
class TestTipoGastoServices:
    def test_add_tipo_gasto_success(self):
        # Teste de adição bem sucedida
        tipo_gasto = add_tipo_gasto("Teste", "Descrição teste")
        assert tipo_gasto["tipoGasto"] == "Teste"
        assert tipo_gasto["descricao"] == "Descrição teste"
        assert TipoGasto.objects.count() == 1

    def test_add_tipo_gasto_duplicate(self):
        # Teste de adição com nome duplicado
        add_tipo_gasto("Teste", "Descrição teste")
        with pytest.raises(BusinessError) as exc:
            add_tipo_gasto("Teste", "Outra descrição")
        assert "Já existe um tipo de gasto com o nome" in str(exc.value)

    def test_add_tipo_gasto_empty_fields(self):
        # Teste de adição com campos vazios
        with pytest.raises(BusinessError) as exc:
            add_tipo_gasto("", "Descrição teste")
        assert "O campo 'tipoGasto' é obrigatório" in str(exc.value)

        with pytest.raises(BusinessError) as exc:
            add_tipo_gasto("Teste", "")
        assert "O campo 'descricao' é obrigatório" in str(exc.value)

    def test_update_tipo_gasto_success(self):
        # Teste de atualização bem sucedida
        tipo_gasto = add_tipo_gasto("Teste", "Descrição teste")
        updated = update_tipo_gasto(tipo_gasto["id"], "Teste Atualizado", "Nova descrição")
        assert updated["tipoGasto"] == "Teste Atualizado"
        assert updated["descricao"] == "Nova descrição"

    def test_update_tipo_gasto_not_found(self):
        # Teste de atualização de tipo de gasto inexistente
        with pytest.raises(BusinessError) as exc:
            update_tipo_gasto(999, "Teste", "Descrição")
        assert "Tipo de Gasto com ID 999 não encontrado" in str(exc.value)

    def test_update_tipo_gasto_duplicate(self):
        # Teste de atualização com nome duplicado
        add_tipo_gasto("Teste1", "Descrição 1")
        tipo_gasto2 = add_tipo_gasto("Teste2", "Descrição 2")
        with pytest.raises(BusinessError) as exc:
            update_tipo_gasto(tipo_gasto2["id"], "Teste1", "Nova descrição")
        assert "Já existe um tipo de gasto com o nome" in str(exc.value)

    def test_delete_tipo_gasto_success(self):
        # Teste de exclusão bem sucedida
        tipo_gasto = add_tipo_gasto("Teste", "Descrição teste")
        delete_tipo_gasto(tipo_gasto["id"])
        assert TipoGasto.objects.count() == 0

    def test_delete_tipo_gasto_not_found(self):
        # Teste de exclusão de tipo de gasto inexistente
        with pytest.raises(BusinessError) as exc:
            delete_tipo_gasto(999)
        assert "Tipo de Gasto com ID 999 não encontrado" in str(exc.value)

    def test_list_tipo_gastos(self):
        # Teste de listagem
        add_tipo_gasto("Teste1", "Descrição 1")
        add_tipo_gasto("Teste2", "Descrição 2")
        tipo_gastos = list_tipo_gastos()
        assert len(tipo_gastos) == 2
        assert tipo_gastos[0]["tipoGasto"] == "Teste1"
        assert tipo_gastos[1]["tipoGasto"] == "Teste2"

@pytest.mark.django_db
class TestElementoTipoGastoServices:
    def test_add_elemento_tipo_gasto_success(self):
        # Teste de adição bem sucedida
        elemento = add_elemento("Teste", "Descrição teste")
        tipo_gasto = add_tipo_gasto("Teste", "Descrição teste")
        relacao = add_elemento_tipo_gasto(elemento["id"], tipo_gasto["id"])
        assert relacao["elemento"]["id"] == elemento["id"]
        assert relacao["tipoGasto"]["id"] == tipo_gasto["id"]
        assert ElementoTipoGasto.objects.count() == 1

    def test_add_elemento_tipo_gasto_duplicate(self):
        # Teste de adição de relacionamento duplicado
        elemento = add_elemento("Teste", "Descrição teste")
        tipo_gasto = add_tipo_gasto("Teste", "Descrição teste")
        add_elemento_tipo_gasto(elemento["id"], tipo_gasto["id"])
        with pytest.raises(BusinessError) as exc:
            add_elemento_tipo_gasto(elemento["id"], tipo_gasto["id"])
        assert "Este relacionamento já existe" in str(exc.value)

    def test_add_elemento_tipo_gasto_not_found(self):
        # Teste de adição com elemento ou tipo de gasto inexistentes
        elemento = add_elemento("Teste", "Descrição teste")
        with pytest.raises(BusinessError) as exc:
            add_elemento_tipo_gasto(999, 1)
        assert "Elemento com ID 999 não encontrado" in str(exc.value)

        tipo_gasto = add_tipo_gasto("Teste", "Descrição teste")
        with pytest.raises(BusinessError) as exc:
            add_elemento_tipo_gasto(elemento["id"], 999)
        assert "Tipo de Gasto com ID 999 não encontrado" in str(exc.value)

    def test_delete_elemento_tipo_gasto_success(self):
        # Teste de exclusão bem sucedida
        elemento = add_elemento("Teste", "Descrição teste")
        tipo_gasto = add_tipo_gasto("Teste", "Descrição teste")
        relacao = add_elemento_tipo_gasto(elemento["id"], tipo_gasto["id"])
        delete_elemento_tipo_gasto(relacao["id"])
        assert ElementoTipoGasto.objects.count() == 0

    def test_delete_elemento_tipo_gasto_not_found(self):
        # Teste de exclusão de relacionamento inexistente
        with pytest.raises(BusinessError) as exc:
            delete_elemento_tipo_gasto(999)
        assert "Relacionamento com ID 999 não encontrado" in str(exc.value)

    def test_list_tipo_gastos_por_elemento(self):
        # Teste de listagem de tipos de gasto por elemento
        elemento = add_elemento("Teste", "Descrição teste")
        tipo_gasto1 = add_tipo_gasto("Teste1", "Descrição 1")
        tipo_gasto2 = add_tipo_gasto("Teste2", "Descrição 2")
        add_elemento_tipo_gasto(elemento["id"], tipo_gasto1["id"])
        add_elemento_tipo_gasto(elemento["id"], tipo_gasto2["id"])
        
        tipo_gastos = list_tipo_gastos_por_elemento(elemento["id"])
        assert len(tipo_gastos) == 2
        assert tipo_gastos[0]["tipoGasto"] == "Teste1"
        assert tipo_gastos[1]["tipoGasto"] == "Teste2"

    def test_list_tipo_gastos_por_elemento_not_found(self):
        # Teste de listagem para elemento inexistente
        with pytest.raises(BusinessError) as exc:
            list_tipo_gastos_por_elemento(999)
        assert "Elemento com ID 999 não encontrado" in str(exc.value) 