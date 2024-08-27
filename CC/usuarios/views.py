from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login, authenticate
from django.db.models import Sum, F

from .forms import FormCriaUsuario, FormLogin
from .models import Usuario
from organizacoes.models import OrganizacaoCaptadora
from projetos.models import Projeto
from contribuicoes.models import ContribuicaoFinanceira
from campanhas.models import Campanha, TipoCrowdfunding, Doacao, Recompensa, Emprestimo


def tem_organizacao(request):
    organizacao_criada = None
    if request.user.is_authenticated:
        # Buscar todas as organizações captadoras criadas pelo usuário logado
        organizacao_criada = OrganizacaoCaptadora.objects.filter(criador=request.user).first()
    return organizacao_criada


def inicial(request):
    organizacao_criada = tem_organizacao(request)

     # Número total de Projetos
    total_projetos = Projeto.objects.count()

    # Total financiado na plataforma
    total_financiado = Campanha.objects.aggregate(Sum('arrecadacao_atual'))['arrecadacao_atual__sum'] or 0

    # Número total de Contribuições
    total_contribuicoes = ContribuicaoFinanceira.objects.count()

    campanhas = Campanha.objects.filter(em_andamento=True)
    campanhas = sorted(campanhas, key=lambda c: c.percentual_arrecadado(), reverse=True)
    top_campanhas = campanhas[:5]

    top_crowds_links = []
    tipo = 0
    crowd_id = 0
    for campanha in top_campanhas:
        if campanha.tipo_crowdfunding.tipo == 'DOACAO':
            temp_campanha = get_object_or_404(Campanha, pk=campanha.id)
            temp_crowd = Doacao.objects.filter(campanha=temp_campanha).first()
            crowd_id = temp_crowd.id
            tipo = 1
        elif campanha.tipo_crowdfunding.tipo == 'RECOMPENSA':
            temp_campanha = get_object_or_404(Campanha, pk=campanha.id)
            temp_crowd = Recompensa.objects.filter(campanha=temp_campanha).first()
            crowd_id = temp_crowd.id
            tipo = 2
        elif campanha.tipo_crowdfunding.tipo == 'EMPRESTIMO':
            temp_campanha = get_object_or_404(Campanha, pk=campanha.id)
            temp_crowd = Emprestimo.objects.filter(campanha=temp_campanha).first()
            crowd_id = temp_crowd.id
            tipo = 3

        lista_crowd = [tipo, crowd_id]
        top_crowds_links.append(lista_crowd)

    listas_zip = zip(top_campanhas, top_crowds_links)


    return render(request, 'usuarios/1_Inicial_CC.html', {
        'titulo': 'Inicial',
        'organizacao_criada_pk': organizacao_criada.pk if organizacao_criada else None,
        'total_projetos': total_projetos,
        'total_financiado': total_financiado,
        'total_contribuicoes': total_contribuicoes,
        'listas_zip': listas_zip,
    })


def principal(request):
    organizacao_criada = tem_organizacao()

    return render(request, 'usuarios/5_Principal_Usuario.html', {
        'titulo': 'Nome do Usuario',
        'organizacao_criada_pk': organizacao_criada,
    })


def criar_conta(request):
    if request.method == 'POST':
        form = FormCriaUsuario(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = FormCriaUsuario()

    return render(request, 'usuarios/6_Criacao_Conta.html',{
        'titulo': 'Inscrever-se',
        'form': form,
        })


def login_conta(request):
    if request.method == 'POST':
        form = FormLogin(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = Usuario.objects.get(email=email)
            except Usuario.DoesNotExist:
                user = None

            if user is not None:
                user = authenticate(request, email=user.email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('usuarios:inicial')  # Redirecione para a página inicial ou onde desejar
                else:
                    form.add_error('password', 'Senha incorreta')
            else:
                form.add_error('email', 'Email não encontrado')
    else:
        form = FormLogin()
    
    return render(request, 'usuarios/7_Login_Conta.html', {
        'titulo': 'Entrar',
        'form': form,
        })


def logout_conta(request):
    logout(request)
    
    return redirect('usuarios:inicial')