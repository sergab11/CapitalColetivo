from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProjetoForm, MembroProjetoForm
from organizacoes.models import OrganizacaoCaptadora
from usuarios.models import Usuario
from projetos.models import MembroProjeto, Projeto
from campanhas.models import Campanha, Doacao, Emprestimo, Recompensa


def pagina_principal(request, pk):
    projeto = get_object_or_404(Projeto, pk=pk)
    membros = MembroProjeto.objects.filter(projeto=projeto)
    
    membro_projeto = MembroProjeto.objects.filter(projeto=projeto, usuario=request.user).first()
    if membro_projeto:
        funcao_usuario = membro_projeto.funcao
    else:
        funcao_usuario = 'NONE'

    
    campanhas_em_andamento = projeto.campanhas.filter(em_andamento=True)
    campanhas_concluidas = projeto.campanhas.filter(em_andamento=False)

    crowds_em_andamento = []
    crowds_concluidas = []

    for campanha in campanhas_em_andamento:
        if campanha.tipo_crowdfunding.tipo == 'DOACAO':
            temp_crowd = Doacao.objects.filter(campanha=campanha).first()
            tipo = 1
        elif campanha.tipo_crowdfunding.tipo == 'RECOMPENSA':
            temp_crowd = Recompensa.objects.filter(campanha=campanha).first()
            tipo = 2
        elif campanha.tipo_crowdfunding.tipo == 'EMPRESTIMO':
            temp_crowd = Emprestimo.objects.filter(campanha=campanha).first()
            tipo = 3
        
        if temp_crowd:
            crowd_id = temp_crowd.id
            crowds_em_andamento.append((tipo, crowd_id))

    for campanha in campanhas_concluidas:
        if campanha.tipo_crowdfunding.tipo == 'DOACAO':
            temp_crowd = Doacao.objects.filter(campanha=campanha).first()
            tipo = 1
        elif campanha.tipo_crowdfunding.tipo == 'RECOMPENSA':
            temp_crowd = Recompensa.objects.filter(campanha=campanha).first()
            tipo = 2
        elif campanha.tipo_crowdfunding.tipo == 'EMPRESTIMO':
            temp_crowd = Emprestimo.objects.filter(campanha=campanha).first()
            tipo = 3

        if temp_crowd:
            crowd_id = temp_crowd.id
            crowds_concluidas.append((tipo, crowd_id))

    # Zip das listas
    campanhas_em_andamento_zip = zip(campanhas_em_andamento, crowds_em_andamento) if campanhas_em_andamento and crowds_em_andamento else None
    campanhas_concluidas_zip = zip(campanhas_concluidas, crowds_concluidas) if campanhas_concluidas and crowds_concluidas else None



    return render(request, 'projetos/3_Principal_Projetos.html', {
        'projeto': projeto,
        'membros': membros,
        'funcao_usuario': funcao_usuario,
        'campanhas_em_andamento_zip': campanhas_em_andamento_zip,
        'campanhas_concluidas_zip': campanhas_concluidas_zip,
    })


@login_required
def meus_projetos(request):
    usuario = request.user
    
    # Buscar todos os projetos dos quais o usuário é membro
    membro_projetos = MembroProjeto.objects.filter(usuario=usuario)
    
    
    return render(request, 'projetos/19_Meus_Projetos.html', {
        'membro_projetos': membro_projetos,
    })


@login_required
def form_criacao_projeto(request, id_org):
    org_cap = get_object_or_404(OrganizacaoCaptadora, pk=id_org)

    if request.method == 'POST':
        projeto_form = ProjetoForm(request.POST, request.FILES)

        membros_forms = []
        for i in range(1, 8):  # Defina o número máximo de membros aqui (até 7 membros)
            form_prefix = f'membro_{i}'
            membro_form = MembroProjetoForm(request.POST, prefix=form_prefix)
            if membro_form.is_valid() and membro_form.cleaned_data.get('email'):
                membros_forms.append(membro_form)
        
        if projeto_form.is_valid() and all(membro_form.is_valid() for membro_form in membros_forms):
            projeto = projeto_form.save(commit=False)
            projeto.organizacao_captadora = org_cap
            projeto.save()
            
            for membro_form in membros_forms:
                email = membro_form.cleaned_data['email']
                funcao = membro_form.cleaned_data['funcao']
                
                if email:  # Apenas processa os campos de email preenchidos
                    usuario, created = Usuario.objects.get_or_create(email=email)
                    membro_projeto = MembroProjeto(usuario=usuario, projeto=projeto, funcao=funcao)
                    membro_projeto.save()

            criador_projeto = membro_form.save(commit=False)
            criador_projeto.usuario = request.user
            criador_projeto.projeto = projeto
            criador_projeto.funcao = "ADMINISTRADOR"
            criador_projeto.save()

            return redirect('projetos:confirm_novo_projeto', projeto_id=projeto.pk)
    else:
        projeto_form = ProjetoForm()
        membros_forms = [MembroProjetoForm(prefix=f'membro_{i}') for i in range(1, 8)]

        return render(request, 'projetos/12_Formulario_Criacao_Projeto.html', {
            'titulo': 'Novo Projeto',
            'projeto': projeto_form,
            'membros': membros_forms,
        })
    

def confirma_novo_projeto(request, projeto_id):
    if request.method == 'POST':
            return redirect('projetos:principal_proj', pk=projeto_id)
    else:
        projeto = get_object_or_404(Projeto, pk=projeto_id)
        membros_projeto = MembroProjeto.objects.filter(projeto=projeto)

        return render(request, 'projetos/13_Confirmacao_Formulario_Criacao_Projeto.html', {
            'titulo': 'Resumo Novo Projeto',
            'projeto': projeto,
            'membros': membros_projeto,
        })


def gerencia_projeto(request):

    return render(request, 'projetos/15_Gerenciamento_Membros_Projeto.html', {
        'titulo': 'Titulo do Projeto',
    })


def form_adicionar_membro(request, pk):
    projeto = get_object_or_404(Projeto, pk=pk)
    membros_projeto = MembroProjeto.objects.filter(projeto=projeto)

    if request.method == 'POST':
        form = MembroProjetoForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            funcao = form.cleaned_data['funcao']

            # Verificar se o usuário já é membro do projeto
            if MembroProjeto.objects.filter(projeto=projeto, usuario__email=email).exists():
                messages.error(request, 'Este usuário já é membro deste projeto.')
                return redirect('projetos:form_adiciona_membro', pk=pk)
            else:
                if email: 
                    usuario, created = Usuario.objects.get_or_create(email=email)
                    membro_projeto = MembroProjeto(usuario=usuario, projeto=projeto, funcao=funcao)
                    membro_projeto.save()
                
                return redirect('projetos:principal_proj', pk=projeto.id)
    else:
        form = MembroProjetoForm()
        return render(request, 'projetos/16_Adicionar_Membro_Projeto.html', {
            'titulo': 'Adicionar Membro a ',
            'form': form,
            'projeto': projeto,
            'membros_projeto': membros_projeto,
        })
    

def confirma_novo_membro(request):

    return render(request, 'projetos/17_Confirmacao_Adicionar_Membro_Projeto.html', {
        'titulo': 'Resumo Novo Membro',
    })


def adicionar_membro(request):
    # adiciona membro no BD e direciona para a página de gerenciamento de membros do projeto

    return redirect('projetos:gerencia_proj')


def confirma_excluir_membro(request, membro_id):
    membro = get_object_or_404(MembroProjeto, pk=membro_id)
    projeto_id = membro.projeto.id  # Salvamos o ID do projeto antes de excluir o membro

    if request.method == 'POST':
        membro.delete()
        return redirect('projetos:principal_proj', pk=projeto_id)

    return render(request, 'projetos/18_Confirmacao_Excluir_Membro_Projeto.html', {
        'titulo': 'Excluir Membro',
        'membro': membro,
    })


def excluir_membro(request):
    # exclui membro no BD e direciona para a página principal do projeto

    return redirect('projetos:principal_proj')