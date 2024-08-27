from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'contribuicoes'

urlpatterns = [
    path('minhas_contribs/', views.minhas_contribs, name='minhas_contribs'),

    path('escolhe_contrib/<int:tipo>/<int:crowd_id>/', views.escolhe_contribuicao, name='escolhe_contrib'),
    path('confirma_escolha/<int:tipo>/<int:crowd_id>/', views.confirma_escolha_contrib, name='confirm_escolha_contrib'),
    path('forma_pagamento/<int:contrib_id>/', views.escolhe_forma_pagamento, name='forma_pag_contrib'),
    path('dados_pagamento/<int:contrib_id>/<int:forma>', views.dados_pagamento, name='dados_pag_contrib'),
    
    path('contrib_realizada/<int:contrib_id>', views.contrib_realizada, name='contrib_realizada'),

    path('motivo_cancelamento/<int:contrib_id>', views.motivo_cancel_contrib, name='motivo_cancel_contrib'),
    path('confirma_cancel_contrib/<int:contrib>', views.confirma_cancel_contrib, name='confirm_cancel_contrib'),
]