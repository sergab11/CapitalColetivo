from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'navegacao'

urlpatterns = [
    path('', views.resultado_pesquisa, name='resultado_pesquisa'),
]