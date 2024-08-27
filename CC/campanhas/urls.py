from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'campanhas'

urlpatterns = [
    path('<int:tipo>/<int:crowd_id>/', views.pagina_principal, name='principal_camp'),

    path('form_criar_campanha/<int:projeto_id>', views.form_criacao_campanha, name='form_criacao_camp'),
    path('confirma_parcial_nova_campanha/', views.confirma_parcial_nova_campanha, name='confirma_parcial_nova_campanha'),
    path('tipo_crowd_nova_campanha/<str:tipo_crowdfunding>/', views.especificacoes_tipo_crowd, name='tipo_crowd_nova_camp'),
    path('confirma_nova_campanha/<str:tipo_crowdfunding>/<int:crowd_id>', views.confirma_nova_campanha, name='confirm_nova_campanha'),
    path('criacao_campanha/', views.criar_campanha, name='criacao_campanha'),
]