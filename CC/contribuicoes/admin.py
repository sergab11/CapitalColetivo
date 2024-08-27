from django.contrib import admin

from .models import ContribuicaoFinanceira, MotivosCancelamento

admin.site.register(ContribuicaoFinanceira)
admin.site.register(MotivosCancelamento)