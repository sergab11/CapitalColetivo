from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'projetos'

urlpatterns = [
    path('<int:pk>/', views.pagina_principal, name='principal_proj'),
    path('meus_projetos', views.meus_projetos, name='meus_projetos'),

    path('form_criar_projeto/<int:id_org>/', views.form_criacao_projeto, name='form_criacao_proj'),
    path('confirma_novo_projeto/<int:projeto_id>/', views.confirma_novo_projeto, name='confirm_novo_projeto'),

    path('gerencia/', views.gerencia_projeto, name='gerencia_proj'),

    path('form_adicionar_membro/<int:pk>', views.form_adicionar_membro, name='form_adiciona_membro'),
    path('confirma_novo_membro/', views.confirma_novo_membro, name='confirm_novo_membro'),
    path('adiciona_membro/', views.adicionar_membro, name='adicionar_membro'),
    
    path('confirma_excluir_membro/<int:membro_id>/', views.confirma_excluir_membro, name='confirma_excluir_membro'),
    path('exclui_membro/', views.excluir_membro, name='excluir_membro'),
]