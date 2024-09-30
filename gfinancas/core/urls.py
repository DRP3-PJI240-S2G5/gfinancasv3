
from django.urls import path

from . import views

urlpatterns = [
    path("departamentos/add", views.add_departamento),
    path("departamentos/list", views.list_departamentos),
]
