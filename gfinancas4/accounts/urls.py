
from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login),
    path('logout', views.logout),
    path('whoami', views.whoami),
    path("list-users", views.list_users, name="list_users"),
    path("add-user", views.add_user, name="add_user"),
]