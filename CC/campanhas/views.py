from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Campanha, Projeto, TipoCrowdfunding, Doacao, Emprestimo, Recompensa
from .forms import CampanhaForm, DoacaoForm, RecompensaForm, EmprestimoForm
from projetos.models import MembroProjeto

def pagina_principal(request, tipo, crowd_id):
    if tipo == 1:
        crowdfunding = get_object_or_404(Doacao, pk=crowd_id)
    elif tipo == 2:
        crowdfunding = get_object_or_404(Recompensa, pk=crowd_id)
    elif tipo == 3:
        crowdfunding = get_object_or_404(Emprestimo, pk=crowd_id)


    campanha = get_object_or_404(Campanha, id=crowdfunding.campanha.id)
    projeto = campanha.projeto
    membro_projeto = MembroProjeto.objects.filter(projeto=projeto, usuario=request.user).first()

    if membro_projeto:
        funcao_usuario = membro_projeto.funcao
    else:
        funcao_usuario = 'NONE'


    return render(request, 'campanhas/4_Principal_Campanha.html', {
        'crowd_id': crowdfunding.id,
        'campanha': crowdfunding.campanha,
        'tipo': tipo,
        'funcao_usuario': funcao_usuario,
    })


def form_criacao_campanha(request, projeto_id):
    projeto = get_object_or_404(Projeto, id=projeto_id)

    if request.method == 'POST':
        form = CampanhaForm(request.POST)
        if form.is_valid():
            campanha = form.save(commit=False)
            campanha.projeto = projeto
            campanha.save()
            projeto.tem_campanha = True
            projeto.save()
            request.session['campanha_id'] = campanha.id
            return redirect('campanhas:confirma_parcial_nova_campanha')
        else:
            print("Erro")
    else:
        form = CampanhaForm()
    
    return render(request, 'campanhas/20_Formulario_Criacao_Campanha.html', {
        'form': form,
        'projeto': projeto,
    })
    

def confirma_parcial_nova_campanha(request):
    campanha_id = request.session.get('campanha_id')
    campanha = get_object_or_404(Campanha, id=campanha_id)

    if request.method == 'POST':
        return redirect('campanhas:tipo_crowd_nova_camp', tipo_crowdfunding=campanha.tipo_crowdfunding.tipo)

    return render(request, 'campanhas/21_Confirmacao_Formulario_Criacao_Campanha.html', {
        'campanha': campanha
    })

    

def especificacoes_tipo_crowd(request, tipo_crowdfunding):
    campanha_id = request.session.get('campanha_id')
    campanha = get_object_or_404(Campanha, id=campanha_id)

    if tipo_crowdfunding == TipoCrowdfunding.DOACAO:
        form_class = DoacaoForm
    elif tipo_crowdfunding == TipoCrowdfunding.RECOMPENSA:
        form_class = RecompensaForm
    elif tipo_crowdfunding == TipoCrowdfunding.EMPRESTIMO:
        form_class = EmprestimoForm


    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            crowdfunding = form.save(commit=False)
            crowdfunding.campanha = campanha
            crowdfunding.save()
            return redirect('campanhas:confirm_nova_campanha', tipo_crowdfunding=crowdfunding.campanha.tipo_crowdfunding, crowd_id=crowdfunding.id)
    else:
        form = form_class()

    if tipo_crowdfunding == 'DOACAO':
        return render(request, 'campanhas/22_Espec_Crowd_Campanha.html',{
            'form': form,
            'tipo': 'Doação',
        })
    elif tipo_crowdfunding == 'RECOMPENSA':
        return render(request, 'campanhas/22_Espec_Crowd_Campanha.html',{
            'form': form,
            'tipo': 'Recompensa',
        })
    elif tipo_crowdfunding == 'EMPRESTIMO':
        return render(request, 'campanhas/22_Espec_Crowd_Campanha.html',{
            'form': form,
            'tipo': 'Empréstimo',
        })
    

def confirma_nova_campanha(request, tipo_crowdfunding, crowd_id):
    crowdfunding = None
    tipo = 0
    if tipo_crowdfunding == 'Doação':
        crowdfunding = get_object_or_404(Doacao, pk=crowd_id)
        tipo = 1
    elif tipo_crowdfunding == 'Recompensa':
        crowdfunding = get_object_or_404(Recompensa, pk=crowd_id)
        tipo = 2
    elif tipo_crowdfunding == 'Empréstimo':
        crowdfunding = get_object_or_404(Emprestimo, pk=crowd_id)
        tipo = 3
    print(f"VAR CROWD.ID: {crowdfunding.id}    CROWD_ID: {crowd_id}    TIPO_CROWD: {tipo_crowdfunding}")


    if request.method == 'POST':
        return redirect('campanhas:principal_camp', tipo=tipo, crowd_id=crowd_id)
    else:
        return render(request, 'campanhas/25_Resumo_Total_Campanha.html', {
                'campanha': crowdfunding.campanha,
                'crowd_id': crowd_id,
                'crowd': crowdfunding,
                'tipo': tipo,
                'tipo_crowdfunding': tipo_crowdfunding,
            })


def criar_campanha(request):
    # cria campanha no BD e direciona para a página principal da campanha recém-criad

    return redirect('campanhas:principal_camp')