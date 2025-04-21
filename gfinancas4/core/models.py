from django.db import models
from ..accounts.models import User
from django.core.exceptions import ValidationError

def verificar_ciclo_subordinacao(superior, subordinado, visitados=None):
    """
    Verifica se existe um ciclo de subordinação entre dois departamentos.
    
    Args:
        superior: Departamento superior
        subordinado: Departamento subordinado
        visitados: Conjunto de IDs de departamentos já visitados na busca
        
    Returns:
        bool: True se existe um ciclo, False caso contrário
    """
    if visitados is None:
        visitados = set()
        
    # Se o departamento atual já foi visitado, temos um ciclo
    if subordinado.id in visitados:
        return True
        
    # Adiciona o departamento atual aos visitados
    visitados.add(subordinado.id)
    
    # Verifica subordinações diretas
    subordinacoes = Subordinacao.objects.filter(superior=subordinado)
    for sub in subordinacoes:
        # Se encontramos o superior em alguma subordinação, temos um ciclo
        if sub.subordinado.id == superior.id:
            return True
        # Verifica recursivamente as subordinações indiretas
        if verificar_ciclo_subordinacao(superior, sub.subordinado, visitados):
            return True
            
    return False 

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
        return f"{self.nome}"
    
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
    superior = models.ForeignKey(  
        Departamento,
        on_delete=models.CASCADE,
        related_name="departamentos_superiores"
    )
    subordinado = models.ForeignKey( 
        Departamento,
        on_delete=models.CASCADE,
        related_name="departamentos_subordinados"
    )
    data_subordinacao = models.DateTimeField(auto_now_add=True) 
    observacao = models.TextField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['superior', 'subordinado'],
                name='unique_subordinacao'
            )
        ]

    def clean(self):
        if self.superior_id == self.subordinado_id:
            raise ValidationError("Um departamento não pode ser subordinado a si mesmo.")
            
        if verificar_ciclo_subordinacao(self.superior, self.subordinado):
            raise ValidationError("Não é possível criar esta subordinação pois ela criaria um ciclo na hierarquia.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.subordinado} subordinado a {self.superior} desde {self.data_subordinacao}"

    def to_dict_json(self):
        return {
            "id": self.id,
            "superior": {
                "id": self.superior.id,
                "nome": self.superior.nome,
            },
            "subordinado": {
                "id": self.subordinado.id,
                "nome": self.subordinado.nome,
            },
            "data_subordinacao": self.data_subordinacao.isoformat(),
            "observacao": self.observacao,
        }
    
class Responsabilidade(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="responsabilidades")
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name="responsaveis")
    data_criacao = models.DateTimeField(auto_now_add=True)  # Alterado para snake_case
    observacao = models.TextField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["usuario", "departamento"], name="unique_user_dep_resp")
        ]

    def __str__(self):
        return f"{self.usuario} é responsável por {self.departamento} desde {self.data_criacao}"

    def to_dict_json(self):
        return {
            "id": self.id,
            "usuario": {
                "id": self.usuario.id,
                "username": self.usuario.username,
            },
            "departamento": {
                "id": self.departamento.id,
                "nome": self.departamento.nome,
            },
            "data_criacao": self.data_criacao.isoformat(),
            "observacao": self.observacao,
        }

class Verba(models.Model):
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="verbas_estipuladas", verbose_name="usuário que atribuiu")
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name="verbas", verbose_name="verbas atribuidas")
    ano = models.IntegerField(verbose_name="Ano")
    descricao = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['departamento', 'ano'], name='unique_departamento_ano_verba')
        ]

    def __str__(self):
        return f"Verba para {self.departamento} atribuída em {self.created_at}"

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
            "ano": self.ano,
            "descricao": self.descricao,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
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

class ElementoTipoGasto(models.Model):
    elemento = models.ForeignKey(Elemento, on_delete=models.CASCADE, related_name="tipos_gasto")
    tipo_gasto = models.ForeignKey(TipoGasto, on_delete=models.CASCADE, related_name="elementos")

    class Meta:
        unique_together = ('elemento', 'tipo_gasto')  # Garantir que cada par (Elemento, TipoGasto) seja único

    def __str__(self):
        return f"{self.elemento.elemento} - {self.tipo_gasto.tipoGasto}"

    def to_dict_json(self):
        return {
            "id": self.id,
            "elemento": {
                "id": self.elemento.id,
                "elemento": self.elemento.elemento,
            },
            "tipoGasto": {
                "id": self.tipo_gasto.id,
                "tipoGasto": self.tipo_gasto.tipoGasto,
            }
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
    
    def clean(self):
        if not ElementoTipoGasto.objects.filter(elemento=self.elemento, tipo_gasto=self.tipoGasto).exists():
            raise ValidationError("O tipo de gasto selecionado não está vinculado ao elemento informado.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Garante que a validação seja executada antes de salvar
        super().save(*args, **kwargs)
    
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
            "elemento": {
                "id": self.elemento.id,
                "elemento": self.elemento.elemento,
            },
            "tipoGasto": {
                "id": self.tipoGasto.id,
                "tipoGasto": self.tipoGasto.tipoGasto,
            },
            "justificativa": self.justificativa,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
    
