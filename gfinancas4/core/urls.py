from django.urls import path

from . import views

urlpatterns = [
    # Endpoints para Departamento
    path("departamentos/add", views.add_departamento, name="add_departamento"),
    path("departamentos/list", views.list_departamentos, name="list_departamentos"),
    path("departamentos/update", views.update_departamento, name="update_departamento"),
    path("departamentos/total-despesas/<int:departamento_id>", views.total_despesas_departamento, name="total_despesas_departamento"),
    path("departamentos/total-despesas-apartir-data/<int:departamento_id>/data/<str:data_inicio>", views.total_despesas_departamento_apartir_data, name="total_despesas_departamento_apartir_data"),
    path("departamentos/total-despesas-periodo/<int:departamento_id>/data/<str:data_inicio>/<str:data_termino>", views.total_despesas_departamento_periodo, name="total_despesas_departamento_periodo"),
    # Endpoints para Subordinação
    path("subordinacoes/add", views.add_subordinacao, name="add_subordinacao"),
    path("subordinacoes/list", views.list_subordinacoes, name="list_subordinacoes"),
    path("subordinacoes/update/<int:id>", views.update_subordinacao, name="update_subordinacao"),
    path("subordinacoes/delete/<int:id>", views.delete_subordinacao, name="delete_subordinacao"),
    
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
    path("despesas/add", views.add_despesa_view, name="add_despesa"),
    path("despesas/update", views.update_despesa, name="update_despesa"),
    path("despesas/delete/<int:id>", views.delete_despesa, name="delete_despesa"),
    path("despesas/list", views.list_despesas, name="list_despesas"),
    path('despesas/list/<int:departamento_id>', views.list_despesas_departamento, name="list_despesas_departamento"),
    path('despesas/list/departamento/<int:departamento_id>/apartir-data/<str:data_inicio>',views.list_despesas_departamento_apartir_data,name="list_despesas_departamento_apartir_data"),
    path('despesas/list/departamento/<int:departamento_id>/periodo/<str:data_inicio>/<str:data_termino>', views.list_despesas_departamento_periodo, name="list_despesas_departamento_periodo"),
    # Endpoints de verbas
    path("verbas/add", views.add_verba, name="add_verba"),
    path("verbas/update/<int:id>", views.update_verba, name="update_verba"),
    path("verbas/delete/<int:id>", views.delete_verba, name="delete_verba"),
    path("verbas/get/<int:id>", views.get_verba, name="get_verba"),
    path("verbas/list", views.list_verbas, name="list_verbas"),
    path("verbas/departamento/<int:departamento_id>", views.list_verbas_departamento, name="list_verbas_departamento"),
    path("verbas/departamento/<int:departamento_id>/ano/<int:ano>", views.get_verba_departamento_ano, name="get_verba_departamento_ano"),
    path("verbas/ultima-do-departamento/<int:departamento_id>", views.get_ultima_verba_departamento, name="get_ultima_verba_departamento"),
]

