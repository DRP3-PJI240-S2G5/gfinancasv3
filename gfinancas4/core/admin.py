from django.contrib import admin

from .models import Departamento, Subordinacao


class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "description", "tipoEntidade", "responsavelId", "done")
    list_filter = ("responsavelId", "tipoEntidade")  # Adiciona filtros laterais para "done" e "TipoEntidade"
    fieldsets = (
        (None, {"fields": ( "nome", "description", "tipoEntidade", "responsavelId", "done")}),
    )

class SubordinacaoAdmin(admin.ModelAdmin):
    list_display = ("IdDepartamentoA", "IdDepartamentoB", "dataSubordinacao", "Observacao")
    list_filter = ("dataSubordinacao",)
    search_fields = ("IdDepartamentoA__description", "IdDepartamentoB__description")
    fieldsets = (
        (None, {"fields": ("IdDepartamentoA", "IdDepartamentoB", "dataSubordinacao", "Observacao")}),
    )

admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Subordinacao, SubordinacaoAdmin)