from django.shortcuts import render
from django.db.models import Q
from projetos.models import Projeto
from campanhas.models import Campanha, Doacao, Recompensa, Emprestimo
from usuarios.models import Usuario


def resultado_pesquisa(request):
    query = request.GET.get('query', '')
    
    if query:
        projetos = Projeto.objects.filter(
            Q(titulo__icontains=query) | Q(texto__icontains=query)
        )
        campanhas = Campanha.objects.filter(
            Q(titulo__icontains=query) | Q(descricao__icontains=query)
        )
        usuarios = Usuario.objects.filter(
            Q(email__icontains=query) | Q(nome__icontains=query)
        )

        # Obter os IDs das campanhas encontradas
        campanhas_ids = campanhas.values_list('id', flat=True)

        doacoes = []
        recompensas = []
        emprestimos = []
        
        # Buscar objetos relacionados usando os IDs das campanhas
        if campanhas_ids:
            doacoes = Doacao.objects.filter(campanha__in=campanhas_ids)
            recompensas = Recompensa.objects.filter(campanha__in=campanhas_ids)
            emprestimos = Emprestimo.objects.filter(campanha__in=campanhas_ids)
    else:
        projetos = []
        campanhas = []
        usuarios = []
        doacoes = []
        recompensas = []
        emprestimos = []
    
    return render(request, 'navegacao/2_Resultado_Busca.html', {
        'query': query,
        'projetos': projetos,
        'usuarios': usuarios,
        'doacao': doacoes,
        'recompensa': recompensas,
        'emprestimo': emprestimos,
    })