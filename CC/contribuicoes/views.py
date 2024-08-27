from django.shortcuts import render, redirect, get_object_or_404
from campanhas.models import Doacao, Recompensa, Emprestimo, Campanha, TipoCrowdfunding
from contribuicoes.models import ContribuicaoFinanceira, MotivosCancelamento
from django.contrib.auth.decorators import login_required
from .forms import DoacaoForm, RecompensaForm, EmprestimoForm, DadosCartaoForm
from django.http import HttpResponseBadRequest

@login_required
def minhas_contribs(request):
    contribuicoes = ContribuicaoFinanceira.objects.filter(usuario=request.user)

    return render(request, 'contribuicoes/35_Minhas_Contribuicoes.html', {
        'contribuicoes': contribuicoes,
    })


def escolhe_contribuicao(request, tipo, crowd_id):
    if tipo == 1:
        crowdfunding = get_object_or_404(Doacao, pk=crowd_id)
        form = DoacaoForm()
    elif tipo == 2:
        crowdfunding = get_object_or_404(Recompensa, pk=crowd_id)
        form = RecompensaForm()
    elif tipo == 3:
        crowdfunding = get_object_or_404(Emprestimo, pk=crowd_id)
        form = EmprestimoForm()

    if request.method == 'GET': 
        return render(request, 'contribuicoes/29_Escolhe_Contrib.html', {
            'tipo': tipo,
            'crowdfunding': crowdfunding,
            'form': form,
            'crowd_id': crowd_id,
        })
    

def confirma_escolha_contrib(request, tipo, crowd_id):
    valor_selecionado = 0
    if request.method == 'POST':
        if tipo == 1:
            crowdfunding = get_object_or_404(Doacao, pk=crowd_id)
            form = DoacaoForm(request.POST)
            tipo_crowd = TipoCrowdfunding.DOACAO
            valor_selecionado = request.POST.get('valor_doacao')
        elif tipo == 2:
            crowdfunding = get_object_or_404(Recompensa, pk=crowd_id)
            form = RecompensaForm(request.POST)
            tipo_crowd = TipoCrowdfunding.RECOMPENSA
        elif tipo == 3:
            crowdfunding = get_object_or_404(Emprestimo, pk=crowd_id)
            form = EmprestimoForm(request.POST)
            tipo_crowd = TipoCrowdfunding.EMPRESTIMO

            if form.is_valid():
                valor_selecionado = form.cleaned_data.get('valor_emprestimo')
                if not valor_selecionado:
                    valor_selecionado= request.POST.get('valor_emprestimo_especifico')
                    try:
                        valor_selecionado = float(valor_selecionado)
                    except ValueError:
                        return HttpResponseBadRequest('Valor de empréstimo inválido.')


        if form.is_valid():
            # Salvar o formulário e processar a contribuição
            contribuicao = ContribuicaoFinanceira.objects.create(
            usuario=request.user,  # ou use seu método para obter o usuário
            campanha=crowdfunding.campanha,
            tipo_crowd=tipo_crowd,
            crowd_id=crowd_id,
            valor_contribuicao = valor_selecionado
        )
            # registrar na arrecadação da campanha
            campanha = get_object_or_404(Campanha, pk=crowdfunding.campanha.pk)
            campanha.arrecadacao_atual += int(float(valor_selecionado))
            campanha.save()

            return redirect('contribuicoes:forma_pag_contrib', contribuicao.id)
    else:
        return render(request, 'contribuicoes/30_Resumo_Contrib.html', {
            'titulo': 'Resumo Contribuição',
        })


def escolhe_forma_pagamento(request, contrib_id):

    if request.method == 'POST':
        forma_pagamento = request.POST.get('forma_pagamento')
        print(f"FORMA PAG: {forma_pagamento}")
        if forma_pagamento == 'cartao':
            forma_pagamento = 1
        else:
            forma_pagamento = 2
        return redirect('contribuicoes:dados_pag_contrib', contrib_id=contrib_id, forma=forma_pagamento)
    else:
        return render(request, 'contribuicoes/31_Forma_Pagamento.html', {
            'titulo': 'Escolha a Forma de Pagamento',
        })
    

def dados_pagamento(request, contrib_id, forma):
    contribuicao = get_object_or_404(ContribuicaoFinanceira, pk=contrib_id)
    
    if forma == 1:  # Cartão de Crédito/Débito
        form_class = DadosCartaoForm
    elif forma == 2:  # Pix
        # Implementar formulário para Pix, se necessário
        pass

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            contribuicao.nome_titular = form.cleaned_data['nome_titular']
            contribuicao.forma_pagamento = 'Cartão de Crédito/Débito'
            contribuicao.numero_cartao = form.cleaned_data['numero_cartao']
            contribuicao.validade_cartao = form.cleaned_data['validade_cartao']
            contribuicao.cvv_cartao = form.cleaned_data['cvv_cartao']
            contribuicao.status_contrib = ContribuicaoFinanceira.STATUS_ATIVA
            contribuicao.save()

        return redirect('contribuicoes:contrib_realizada', contrib_id=contrib_id)
    else:
        form = form_class()
        return render(request, 'contribuicoes/33_Dados_Pagamento_Contrib.html', {
            'titulo': 'Entre com os dados do Pagamento',
            'form': form,
        })
    

def contrib_realizada(request, contrib_id):
    contribuicao = get_object_or_404(ContribuicaoFinanceira, pk=contrib_id)
    
    return render(request, 'contribuicoes/34_Contribuicao_Realizada.html', {
            'contribuicao': contribuicao,
        })


def motivo_cancel_contrib(request, contrib_id):
    contribuicao = get_object_or_404(ContribuicaoFinanceira, pk=contrib_id)

    if request.method == 'POST':
        motivo_id = request.POST.get('motivo_cancelamento')
        if motivo_id:
            motivo = get_object_or_404(MotivosCancelamento, id=motivo_id)
            # Aqui você pode adicionar a lógica para registrar o motivo de cancelamento, se necessário
            campanha = get_object_or_404(Campanha, pk=contribuicao.campanha.id)
            campanha.arrecadacao_atual -= contribuicao.valor_contribuicao
            campanha.save()
            
            # Deletar a contribuição do banco de dados
            contribuicao.status_contrib = ContribuicaoFinanceira.STATUS_CANCELADA
            contribuicao.save()
            return redirect('contribuicoes:minhas_contribs')
    
    motivos_cancelamento = MotivosCancelamento.objects.all()
    nome_campanha = contribuicao.campanha.titulo
    return render(request, 'contribuicoes/36_Motivo_Cancelamento.html', {
        'motivos_cancelamento': motivos_cancelamento,
        'titulo_camp': nome_campanha,
    })
    

def confirma_cancel_contrib(request, contrib_id):

    return render(request, 'contribuicoes/37_Cancelamento_Contribuicao.html', {
            'pk_contrib': 'PK da Contribuição',
            'data_cancel': 'Data do Cancelamento',
        })
