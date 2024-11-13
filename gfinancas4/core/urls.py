
from django.urls import path

from . import views

urlpatterns = [
    # Endpoints para Departamento
    path("departamentos/add", views.add_departamento, name="add_departamento"),
    path("departamentos/list", views.list_departamentos, name="list_departamentos"),
    path("departamentos/update", views.update_departamento, name="update_departamento"),
    #path("subordinacoes/add", views.add_subordinacao),
    #path("subordinacoes/list", views.list_subordinacoes),
    #path("despesas/add", views.add_despesa),
    #path("despesas/list", views.list_despesas),
    #path("verbas/add", views.add_verba),
    #path("verbas/list", views.list_verbas),
]
