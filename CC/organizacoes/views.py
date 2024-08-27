from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import FormOrganizacaoCaptadora
from .models import OrganizacaoCaptadora, Banco

@login_required
def solicita_nova(request):
    if request.method == 'POST':
        form = FormOrganizacaoCaptadora(request.POST)
        if form.is_valid():
            # Armazena os dados do formulário na sessão para a página de confirmação
            organizacao_data = form.cleaned_data
            organizacao_data['banco_id'] = organizacao_data['banco'].id
            del organizacao_data['banco']  # Remove o objeto Banco
            request.session['organizacao_data'] = organizacao_data
            return redirect('organizacoes:confirma_criacao')
    else:
        form = FormOrganizacaoCaptadora()
    
    return render(request, 'organizacoes/9_Formulario_Criacao_Organizacao.html', {
        'titulo': 'Nova Organização',
        'form': form,
        })
    

@login_required    
def confirma_criacao(request):
    # Recupera os dados do formulário da sessão
    organizacao_data = request.session.get('organizacao_data')
    if not organizacao_data:
        return redirect('criar_organizacao')

    banco = get_object_or_404(Banco, id=organizacao_data['banco_id'])
    organizacao_data['banco'] = banco

    if request.method == 'POST':
        form = FormOrganizacaoCaptadora(organizacao_data)
        if form.is_valid():
            organizacao = form.save(commit=False)
            organizacao.criador = request.user
            organizacao.save()

            request.user.tem_organizacao = True
            request.user.organizacao_id = organizacao.id
            request.user.save()
            # Redirecione para a página de gerenciamento da Organização Captadora
            return redirect('organizacoes:gerencia_org', pk=organizacao.id)
    else:
        return render(request, 'organizacoes/10_Confirmacao_Formulario_Criacao_Organizacao.html', {
            'titulo': 'Resumo Nova Organização',
            'organizacao': organizacao_data,
            })
    

@login_required    
def gerencia_organizacao(request, pk):
    organizacao = get_object_or_404(OrganizacaoCaptadora, pk=pk)

    return render(request, 'organizacoes/11_Inicial_Organizacao.html', {
        'titulo': organizacao.nome,
        'organizacao': organizacao,
        'organizacao_criada_pk': pk,
     })