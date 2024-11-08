
from django.urls import path

from . import views

urlpatterns = [
    # Endpoints para Departamento
    path("departamentos/add", views.add_departamento, name="add_departamento"),
    path("departamentos/list", views.list_departamentos, name="list_departamentos"),
    path("departamentos/update/<int:departamento_id>", views.update_departamento, name="update_departamento"),

    # Endpoints para Despesa
    path("despesas/add", views.add_despesa, name="add_despesa"),
    path("despesas/list", views.list_despesas, name="list_despesas"),
    path("despesas/update/<int:despesa_id>", views.update_despesa, name="update_despesa"),

    # Endpoints para Verba
    path("verbas/add", views.add_verba, name="add_verba"),
    path("verbas/list", views.list_verbas, name="list_verbas"),
    path("verbas/update/<int:verba_id>", views.update_verba, name="update_verba"),

    # Endpoints para Elemento
    path("elementos/add", views.add_elemento, name="add_elemento"),
    path("elementos/list", views.list_elementos, name="list_elementos"),
    path("elementos/update/<int:elemento_id>", views.update_elemento, name="update_elemento"),

    # Endpoints para TipoGasto
    path("tiposgastos/add", views.add_tipo_gasto, name="add_tipo_gasto"),
    path("tiposgastos/list", views.list_tipos_gastos, name="list_tipos_gasto"),
    path("tiposgastos/update/<int:tipo_gasto_id>", views.update_tipo_gasto, name="update_tipo_gasto"),
]
