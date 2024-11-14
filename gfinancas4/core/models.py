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
