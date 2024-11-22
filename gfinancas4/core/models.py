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
    departamentoA = models.ForeignKey(
        Departamento, 
        on_delete=models.CASCADE, 
        related_name="departamentos_superiores"
    )
    departamentoB = models.ForeignKey(
        Departamento, 
        on_delete=models.CASCADE, 
        related_name="departamentos_subordinados"
    )
    dataSubordinacao = models.DateTimeField(auto_now_add=True)
    Observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.departamentoB} subordinado a {self.departamentoA} desde {self.dataSubordinacao}"

    def to_dict_json(self):
        return {
            "departamentoA": {
                "id": self.departamentoA.id,
                "nome": self.departamentoA.nome,
            },
            "departamentoB": {
                "id": self.departamentoB.id,
                "nome": self.departamentoB.nome,
            },
            "dataSubordinacao": self.dataSubordinacao,
            "Observacao": self.Observacao,
        }
    
class Responsabilidade(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="responsabilidades")
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name="responsaveis")
    dataCriacao = models.DateTimeField(auto_now_add=True)
    observacao = models.TextField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'departamento'], name='unique_user_departamento_responsabilidade')
        ]

    def __str__(self):
        return f"{self.user} é responsável por {self.departamento} desde {self.dataCriacao}"

    def to_dict_json(self):
        return {
            "id": self.id,
            "usuario": {
                "id": self.user.id,
                "username": self.user.username,
            },
            "departamento": {
                "id": self.departamento.id,
                "nome": self.departamento.nome,
            },
            "data_criacao": self.dataCriacao.isoformat(),
            "observacao": self.observacao,
        }

class Verba(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="verbas_estipuladas", verbose_name="usuário que atribuiu")
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name="verbas", verbose_name="verbas atribuidas")
    dataAtribuicao = models.DateTimeField(auto_now_add=True)
    ano = models.IntegerField(verbose_name="Ano")
    descricao = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['departamento', 'ano'], name='unique_departamento_ano_verba')
        ]

    def __str__(self):
        return f"Verba para {self.departamento} atribuída em {self.dataAtribuicao}"

    def to_dict_json(self):
        return {
            "id": self.id,
            "departamento": {
                "id": self.departamento.id,
                "nome": self.departamento.nome,
            },
            "usuario":{
                "id": self.user.id,
                "username": self.user.username,
            },
            "dataAtribuicao": self.dataAtribuicao,
            "ano": self.ano,
            "descricao": self.descricao,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

class Elemento(models.Model):
    elemento = models.CharField(max_length=256)
    descricao = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.elemento}"
    
    def to_dict_json(self):
        return {
            "id": self.id,
            "elemento": self.elemento,
            "descricao": self.descricao,
        }

class TipoGasto(models.Model):
    tipoGasto = models.CharField(max_length=256)
    descricao = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.tipoGasto}"
    
    def to_dict_json(self):
        return {
            "id": self.id,
            "tipoGasto": self.tipoGasto,
            "descricao": self.descricao,
        }

class Despesa(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="despesas")
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    elemento = models.ForeignKey(Elemento, on_delete=models.CASCADE, related_name="despesas_elemento")
    tipoGasto = models.ForeignKey(TipoGasto, on_delete=models.CASCADE, related_name="despesas_tipoGasto")
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name="despesas_departamento")
    justificativa = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Despesa de {self.valor} - {self.departamento.nome}"

    def to_dict_json(self):
        return {
            "id": self.id,
            "departamento": {
                "id": self.departamento.id,
                "nome": self.departamento.nome,
            },
            "usuario":{
                "id": self.user.id,
                "username": self.user.username,
            },
            "valor": self.valor,
            "elemento": self.elemento.id,
            "tipoGasto": self.tipoGasto.id,
            "justificativa": self.justificativa,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }