import csv
from django.contrib import admin
from .models import Departamento, Subordinacao, Responsabilidade, Verba, Despesa, Elemento, TipoGasto, ElementoTipoGasto
from django.http import HttpResponse

@admin.action(description="Exportar dados selecionados como CSV")
def exportar_para_csv(modeladmin, request, queryset):
    # Nome do arquivo
    nome_arquivo = f"{modeladmin.model._meta.verbose_name_plural}.csv"
    
    # Configurar a resposta HTTP para download do arquivo
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f"attachment; filename={nome_arquivo}"

    # Criar o escritor CSV
    writer = csv.writer(response)

    # Obter os campos do modelo dinamicamente
    campos = [field.name for field in modeladmin.model._meta.fields]
    writer.writerow(campos)  # Cabeçalho do CSV

    # Preencher as linhas com os valores dos objetos selecionados
    for obj in queryset:
        writer.writerow([getattr(obj, campo) for campo in campos])

    return response

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
    list_display = ("id", "superior_nome", "subordinado_nome", "data_subordinacao", "observacao")
    list_filter = ("data_subordinacao",)
    search_fields = ("superior__nome", "superior__description", "subordinado__nome", "subordinado__description")
    fieldsets = (
        (None, {"fields": ("superior", "subordinado", "observacao")}),
    )
    actions = [remover_subordinacao]

    def superior_nome(self, obj):
        """Exibe o nome do departamento superior na lista."""
        return obj.superior.nome
    superior_nome.short_description = "Departamento Superior"

    def subordinado_nome(self, obj):
        """Exibe o nome do departamento subordinado na lista."""
        return obj.subordinado.nome
    subordinado_nome.short_description = "Departamento Subordinado"

class ResponsabilidadeAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario_nome", "departamento_nome", "data_criacao", "observacao")
    search_fields = ("usuario__username", "departamento__nome")
    list_filter = ("data_criacao",)
    fieldsets = (
        (None, {"fields": ("usuario", "departamento", "observacao")}),
    )

    def usuario_nome(self, obj):
        """Exibe o nome do usuário associado à responsabilidade."""
        return obj.usuario.username
    usuario_nome.short_description = "Usuário"

    def departamento_nome(self, obj):
        """Exibe o nome do departamento associado à responsabilidade."""
        return obj.departamento.nome
    departamento_nome.short_description = "Departamento"

class VerbaAdmin(admin.ModelAdmin):
    list_display = ("id", "departamento_nome", "valor", "ano", "descricao", "usuario_nome", "created_at", "updated_at")
    search_fields = ("departamento__nome", "descricao", "ano")
    list_filter = ("ano", "created_at")
    actions = [exportar_para_csv]  # Ação de exportar

    def departamento_nome(self, obj):
        return obj.departamento.nome
    departamento_nome.short_description = "Departamento"

    def usuario_nome(self, obj):
        return obj.user.username
    usuario_nome.short_description = "Usuário"


class DespesaAdmin(admin.ModelAdmin):
    list_display = ("id", "departamento_nome", "valor", "usuario_nome", "elemento_nome", "tipo_gasto_nome", "justificativa", "created_at", "updated_at")
    search_fields = ("departamento__nome", "justificativa", "elemento__descricao", "tipoGasto__descricao")
    list_filter = ("created_at", "updated_at", "tipoGasto")
    actions = [exportar_para_csv]  # Ação de exportar

    def departamento_nome(self, obj):
        return obj.departamento.nome
    departamento_nome.short_description = "Departamento"

    def usuario_nome(self, obj):
        return obj.user.username
    usuario_nome.short_description = "Usuário"

    def elemento_nome(self, obj):
        return obj.elemento.descricao
    elemento_nome.short_description = "Elemento"

    def tipo_gasto_nome(self, obj):
        return obj.tipoGasto.descricao
    tipo_gasto_nome.short_description = "Tipo de Gasto"

class ElementoAdmin(admin.ModelAdmin):
    list_display = ("id", "elemento", "descricao")
    search_fields = ("elemento", "descricao")
    list_filter = ("elemento",)
    fieldsets = (
        (None, {"fields": ("elemento", "descricao")}),
    )

class TipoGastoAdmin(admin.ModelAdmin):
    list_display = ("id", "tipoGasto", "descricao")
    search_fields = ("tipoGasto", "descricao")
    list_filter = ("tipoGasto",)
    fieldsets = (
        (None, {"fields": ("tipoGasto", "descricao")}),
    )

class ElementoTipoGastoAdmin(admin.ModelAdmin):
    list_display = ('elemento', 'tipo_gasto')  # Exibe as colunas elemento e tipo_gasto na listagem
    search_fields = ('elemento__elemento', 'tipo_gasto__tipoGasto')  # Permite pesquisar por nome do elemento e tipo de gasto
    list_filter = ('elemento', 'tipo_gasto')  # Filtros para elemento e tipo de gasto


# Registrar no admin
admin.site.register(Verba, VerbaAdmin)
admin.site.register(Despesa, DespesaAdmin)
admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Subordinacao, SubordinacaoAdmin)
admin.site.register(Responsabilidade, ResponsabilidadeAdmin)
admin.site.register(Elemento, ElementoAdmin)
admin.site.register(TipoGasto, TipoGastoAdmin)
admin.site.register(ElementoTipoGasto, ElementoTipoGastoAdmin)