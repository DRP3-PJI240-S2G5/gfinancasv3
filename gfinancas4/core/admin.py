from django.contrib import admin

from .models import Departamento


class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "description", "tipoEntidade", "responsavelId", "done")
    list_filter = ("responsavelId", "tipoEntidade")  # Adiciona filtros laterais para "done" e "TipoEntidade"
    fieldsets = (
        (None, {"fields": ( "nome", "description", "tipoEntidade", "responsavelId", "done")}),
    )

admin.site.register(Departamento, DepartamentoAdmin)
