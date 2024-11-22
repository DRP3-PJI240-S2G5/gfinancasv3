
from django.urls import path

from . import views

urlpatterns = [
    # Endpoints para Departamento
    path("departamentos/add", views.add_departamento, name="add_departamento"),
    path("departamentos/list", views.list_departamentos, name="list_departamentos"),
    #path("departamentos/update", views.update_departamento, name="update_departamento"),
    # subordinacao
    path("subordinacao/add", views.add_subordinacao, name="add_subordinacao"),
    path("subordinacao/list", views.list_subordinacoes, name="list_subordinacoes"),
    # Endpoints para Responsabilidade
    path("responsabilidades/add", views.add_responsabilidade, name="add_responsabilidade"),
    path("responsabilidades/list", views.list_responsabilidades, name="list_responsabilidades"),
    #path("responsabilidades/update/<int:id>", views.update_responsabilidade, name="update_responsabilidade"),
    #path("responsabilidades/delete/<int:id>", views.delete_responsabilidade, name="delete_responsabilidade"),
]
