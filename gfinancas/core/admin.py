from django.contrib import admin

from .models import Departamento, ResponsavelDepartamento, SubordinadoA, Elemento, TipoGasto, Despesa, Verba

class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ("description", "done", "IdUserResp", "TipoEntidade", "Nome")  # Exibe mais campos na lista
    list_filter = ("done", "TipoEntidade")  # Adiciona filtros laterais para "done" e "TipoEntidade"
    fieldsets = (
        (None, {"fields": ("description", "done", "IdUserResp", "TipoEntidade", "Nome")}),
    )

class ResponsavelDepartamentoAdmin(admin.ModelAdmin):
    list_display = ("IdUser", "IdDepartamento", "dataCriacao", "Observacao")
    list_filter = ("dataCriacao",)
    search_fields = ("IdUser__username", "IdDepartamento__description")  # Permite buscar por usuário ou descrição do departamento
    fieldsets = (
        (None, {"fields": ("IdUser", "IdDepartamento", "dataCriacao", "Observacao")}),
    )

class SubordinadoAAdmin(admin.ModelAdmin):
    list_display = ("IdDepartamentoA", "IdDepartamentoB", "dataSubordinacao", "Observacao")
    list_filter = ("dataSubordinacao",)
    search_fields = ("IdDepartamentoA__description", "IdDepartamentoB__description")
    fieldsets = (
        (None, {"fields": ("IdDepartamentoA", "IdDepartamentoB", "dataSubordinacao", "Observacao")}),
    )

class ElementoAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)

class TipoGastoAdmin(admin.ModelAdmin):
    list_display = ("descricao",)
    search_fields = ("descricao",)

class DespesaAdmin(admin.ModelAdmin):
    list_display = ("IdUser", "Valor", "IdElemento", "IdTipoGasto", "IdDepartamento", "Justificativa")
    list_filter = ("IdDepartamento", "IdTipoGasto", "IdElemento")
    search_fields = ("Justificativa",)

class VerbaAdmin(admin.ModelAdmin):
    list_display = ("IdDepartamento", "IdUser", "dataAtribuicao", "descricao")
    list_filter = ("dataAtribuicao", "IdDepartamento")
    search_fields = ("descricao",)

admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(ResponsavelDepartamento, ResponsavelDepartamentoAdmin)
admin.site.register(SubordinadoA, SubordinadoAAdmin)
admin.site.register(Elemento, ElementoAdmin)
admin.site.register(TipoGasto, TipoGastoAdmin)
admin.site.register(Despesa, DespesaAdmin)
admin.site.register(Verba, VerbaAdmin)