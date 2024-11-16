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
            "IdDepartamentoA": self.IdDepartamentoA.id if self.IdDepartamentoA else None,
            "IdDepartamentoB": self.IdDepartamentoB.id if self.IdDepartamentoB else None,
            "dataSubordinacao": self.dataSubordinacao,
            "Observacao": self.Observacao,
        }