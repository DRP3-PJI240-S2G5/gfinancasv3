from django.db import models
from gfinancas.accounts.models import User

# Classe auxiliar para representar um tipo de elemento de gasto
class Elemento(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

    def to_dict_json(self):
        return {
            "id": self.id,
            "nome": self.nome,
        }

# Classe auxiliar para representar o tipo de gasto
class TipoGasto(models.Model):
    descricao = models.CharField(max_length=255)

    def __str__(self):
        return self.descricao

    def to_dict_json(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
        }

class Departamento(models.Model):
    description = models.CharField(max_length=512)
    done = models.BooleanField(default=False)
    TipoEntidade = models.CharField(max_length=256)
    Nome = models.CharField(max_length=256)
    IdUserResp = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name="departamentos",
        verbose_name="Responsável"
    )

    def to_dict_json(self):
        return {
            "id": self.id,
            "description": self.description,
            "done": self.done,
            "IdUserResp": self.IdUserResp.id if self.IdUserResp else None,
            "TipoEntidade": self.TipoEntidade,
            "Nome": self.Nome,
        }

# Classe Despesa que armazena despesas realizadas por cada departamento
class Despesa(models.Model):
    IdUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="despesas")
    Valor = models.DecimalField(max_digits=10, decimal_places=2)
    IdElemento = models.ForeignKey(Elemento, on_delete=models.CASCADE, related_name="despesas")
    IdTipoGasto = models.ForeignKey(TipoGasto, on_delete=models.CASCADE, related_name="despesas")
    IdDepartamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name="despesas")
    Justificativa = models.TextField()

    def __str__(self):
        return f"Despesa de {self.Valor} - {self.IdDepartamento}"

    def to_dict_json(self):
        return {
            "id": self.id,
            "IdUser": self.IdUser.id,
            "Valor": self.Valor,
            "IdElemento": self.IdElemento.id,
            "IdTipoGasto": self.IdTipoGasto.id,
            "IdDepartamento": self.IdDepartamento.id,
            "Justificativa": self.Justificativa,
        }

# Classe Verba que representa a verba máxima atribuída a cada departamento
class Verba(models.Model):
    IdDepartamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name="verbas")
    IdUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="verbas_atribuidas")
    dataAtribuicao = models.DateTimeField(auto_now_add=True)
    descricao = models.TextField()

    def __str__(self):
        return f"Verba para {self.IdDepartamento} atribuída em {self.dataAtribuicao}"

    def to_dict_json(self):
        return {
            "id": self.id,
            "IdDepartamento": self.IdDepartamento.id,
            "IdUser": self.IdUser.id,
            "dataAtribuicao": self.dataAtribuicao,
            "descricao": self.descricao,
        }

class ResponsavelDepartamento(models.Model):
    IdUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="responsabilidades")
    IdDepartamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name="responsaveis")
    dataCriacao = models.DateTimeField(auto_now_add=True)
    Observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.IdUser} é responsável por {self.IdDepartamento} desde {self.dataCriacao}"

    def to_dict_json(self):
        return {
            "id": self.id,
            "IdUser": self.IdUser.id if self.IdUser else None,
            "IdDepartamento": self.IdDepartamento.id if self.IdDepartamento else None,
            "dataCriacao": self.dataCriacao,
            "Observacao": self.Observacao,
        }

class SubordinadoA(models.Model):
    IdDepartamentoA = models.ForeignKey(
        Departamento, 
        on_delete=models.CASCADE, 
        related_name="departamentos_superiores"
    )
    IdDepartamentoB = models.ForeignKey(
        Departamento, 
        on_delete=models.CASCADE, 
        related_name="departamentos_subordinados"
    )
    dataSubordinacao = models.DateTimeField(auto_now_add=True)
    Observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.IdDepartamentoB} subordinado a {self.IdDepartamentoA} desde {self.dataSubordinacao}"

    def to_dict_json(self):
        return {
            "id": self.id,
            "IdDepartamentoA": self.IdDepartamentoA.id if self.IdDepartamentoA else None,
            "IdDepartamentoB": self.IdDepartamentoB.id if self.IdDepartamentoB else None,
            "dataSubordinacao": self.dataSubordinacao,
            "Observacao": self.Observacao,
        }