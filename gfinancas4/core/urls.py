
from django.urls import path

from . import views

urlpatterns = [
    # Endpoints para Departamento
    path("departamentos/add", views.add_departamento, name="add_departamento"),
    path("departamentos/list", views.list_departamentos, name="list_departamentos"),
    path("departamentos/update", views.update_departamento, name="update_departamento"),
    # subordinacao
    path("subordinacao/add", views.add_subordinacao, name="add_subordinacao"),
    path("subordinacao/list", views.list_subordinacoes, name="list_subordinacoes"),
    # Endpoints para Responsabilidade
    path("responsabilidades/add", views.add_responsabilidade, name="add_responsabilidade"),
    path("responsabilidades/list", views.list_responsabilidades, name="list_responsabilidades"),
    #path("responsabilidades/update/<int:id>", views.update_responsabilidade, name="update_responsabilidade"),
    #path("responsabilidades/delete/<int:id>", views.delete_responsabilidade, name="delete_responsabilidade"),
    # elementos
    path("elementos/list", views.list_elementos, name="list_elementos"),
    # Tipo de Gastos
    path("tipo-gastos/list", views.list_tipo_gastos, name="list_tipo_gastos"),
    path("tipo-gastos/por-elemento/<int:elemento_id>", views.list_tipo_gastos_por_elemento),
     # Endpoints para Despesa
    path("despesas/add", views.add_despesa, name="add_despesa"),
    path("despesas/update", views.update_despesa, name="update_despesa"),
    path("despesas/list", views.list_despesas, name="list_despesas"),
    path('despesas/list/<int:departamento_id>', views.list_despesas_departamento, name="list_despesas_departamento"),
]

