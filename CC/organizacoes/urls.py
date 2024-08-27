from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'organizacoes'

urlpatterns = [
    path('form_criar/', views.solicita_nova, name='form_solicita'),
    path('confirma_nova/', views.confirma_criacao, name='confirma_criacao'),
    path('<int:pk>/', views.gerencia_organizacao, name='gerencia_org'),
]