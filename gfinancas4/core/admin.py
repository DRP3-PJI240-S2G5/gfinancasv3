from django.contrib import admin

from .models import Departamento, Subordinacao, Responsabilidade

class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "description", "tipoEntidade", "responsavelId", "done")
    list_filter = ("responsavelId", "tipoEntidade")  # Adiciona filtros laterais para "done" e "TipoEntidade"
    search_fields = ("nome", "description")
    fieldsets = (
        (None, {"fields": ( "nome", "description", "tipoEntidade", "responsavelId", "done")}),
    )


@admin.action(description="Remover subordinação selecionada")
def remover_subordinacao(modeladmin, request, queryset):
    """Ação para remover as subordinações selecionadas."""
    count = queryset.count()
    queryset.delete()
    modeladmin.message_user(request, f"{count} subordinação(ões) removida(s) com sucesso.")

class SubordinacaoAdmin(admin.ModelAdmin):
    list_display = ("id", "IdDepartamentoA_nome", "IdDepartamentoB_nome", "dataSubordinacao", "observacao")
    list_filter = ("dataSubordinacao",)
    search_fields = (
        "IdDepartamentoA_nome", "IdDepartamentoA_description",
        "IdDepartamentoB_nome", "IdDepartamentoB_description"
    )
    fieldsets = (
        (None, {"fields": ("IdDepartamentoA", "IdDepartamentoB", "observacao")}),
    )
    actions = [remover_subordinacao]

    def IdDepartamentoA_nome(self, obj):
        """Exibe o nome do departamento A na lista."""
        return obj.IdDepartamentoA.nome
    IdDepartamentoA_nome.short_description = "Departamento Superior"

    def IdDepartamentoB_nome(self, obj):
        """Exibe o nome do departamento B na lista."""
        return obj.IdDepartamentoB.nome
    IdDepartamentoB_nome.short_description = "Departamento Subordinado"

class ResponsabilidadeAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario_nome", "departamento_nome", "dataCriacao", "observacao")
    search_fields = ("IdUser__username", "departamento")
    list_filter = ("dataCriacao",)
    fieldsets = (
        (None, {"fields": ("user", "departamento", "observacao")}),
    )

    def usuario_nome(self, obj):
        """Exibe o nome do usuário associado à responsabilidade."""
        return obj.IdUser.username
    usuario_nome.short_description = "Usuário"

    def departamento_nome(self, obj):
        """Exibe o nome do departamento associado à responsabilidade."""
        return obj.IdDepartamento.nome
    departamento_nome.short_description = "Departamento"

admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Subordinacao, SubordinacaoAdmin)
admin.site.register(Responsabilidade, ResponsabilidadeAdmin)