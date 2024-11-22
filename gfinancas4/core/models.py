from django.db import models
from ..accounts.models import User

class Departamento(models.Model):
    nome = models.CharField(max_length=256)
    description = models.CharField(max_length=512)
    tipoEntidade = models.CharField(max_length=256)
    done = models.BooleanField(default=False)
    responsavelId = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name="departamentos",
        verbose_name="responsavel"
    )

    def __str__(self):
        return self.nome
    
    def to_dict_json(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "description": self.description,
            "tipoEntidade": self.tipoEntidade,
            "responsavelId": self.responsavelId.id if self.responsavelId else None,
            "done": self.done,
        }

class Subordinacao(models.Model):
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
            "IdDepartamentoA": {
                "id": self.IdDepartamentoA.id,
                "nome": self.IdDepartamentoA.nome,
            },
            "IdDepartamentoB": {
                "id": self.IdDepartamentoB.id,
                "nome": self.IdDepartamentoB.nome,
            },
            "dataSubordinacao": self.dataSubordinacao,
            "Observacao": self.Observacao,
        }
    
class Responsabilidade(models.Model):
    IdUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="responsabilidades")
    IdDepartamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name="responsaveis")
    dataCriacao = models.DateTimeField(auto_now_add=True)
    Observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.IdUser} é responsável por {self.IdDepartamento} desde {self.dataCriacao}"

    def to_dict_json(self):
        return {
            "id": self.id,
            "usuario": {
                "id": self.IdUser.id,
                "username": self.IdUser.username,
            },
            "departamento": {
                "id": self.IdDepartamento.id,
                "nome": self.IdDepartamento.nome,
            },
            "data_criacao": self.dataCriacao.isoformat(),
            "observacao": self.Observacao,
        }