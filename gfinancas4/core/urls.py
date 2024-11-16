
from django.urls import path

from . import views

urlpatterns = [
    # Endpoints para Departamento
    path("departamentos/add", views.add_departamento, name="add_departamento"),
    path("departamentos/list", views.list_departamentos, name="list_departamentos"),
    path("departamentos/update", views.update_departamento, name="update_departamento"),
    path("subordinacao/add", views.add_subordinacao, name="add_subordinacao"),
    path("subordinacao/list", views.list_subordinacoes, name="list_subordinacoes"),
]
