from django.contrib import admin

from .models import Campanha, TipoCrowdfunding, Doacao, Recompensa, Emprestimo

admin.site.register(Campanha)
admin.site.register(TipoCrowdfunding)
admin.site.register(Doacao)
admin.site.register(Recompensa)
admin.site.register(Emprestimo)