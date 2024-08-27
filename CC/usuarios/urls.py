from django.urls import path

from . import views

app_name = 'usuarios'

urlpatterns = [
    path('', views.inicial, name='inicial'),
    path('principal/', views.principal, name='principal'),
    path('criar/', views.criar_conta, name='criar_conta'),
    path('login/', views.login_conta , name='login_conta'),
    path('logout/', views.logout_conta, name='logout_conta'),
]