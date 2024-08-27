# forms.py

from django import forms
from .models import OrganizacaoCaptadora, Banco

class FormOrganizacaoCaptadora(forms.ModelForm):
    class Meta:
        model = OrganizacaoCaptadora
        fields = ['nome', 'titular_conta', 'numero_conta', 'agencia_bancaria', 'banco', 'cpf_cnpj', 'contato', 'descricao']

    def __init__(self, *args, **kwargs):
        super(FormOrganizacaoCaptadora, self).__init__(*args, **kwargs)
        # Adicione placeholders se desejar
        self.fields['nome'].widget.attrs['placeholder'] = 'Nome da Organização'
        self.fields['nome'].widget.attrs['class'] = 'w-full py-4 px-6 rounded-xl'

        self.fields['titular_conta'].widget.attrs['placeholder'] = 'Nome do Titular da Conta'
        self.fields['titular_conta'].widget.attrs['class'] = 'w-full py-4 px-6 rounded-xl'

        self.fields['numero_conta'].widget.attrs['placeholder'] = 'Número da Conta'
        self.fields['numero_conta'].widget.attrs['class'] = 'w-full py-4 px-6 rounded-xl'

        self.fields['agencia_bancaria'].widget.attrs['placeholder'] = 'Agência Bancária'
        self.fields['agencia_bancaria'].widget.attrs['class'] = 'w-full py-4 px-6 rounded-xl'

        self.fields['banco'].queryset = Banco.objects.all().order_by('cod')  # Ordene os bancos por código

        self.fields['cpf_cnpj'].widget.attrs['placeholder'] = 'CPF ou CNPJ'
        self.fields['cpf_cnpj'].widget.attrs['class'] = 'w-full py-4 px-6 rounded-xl'

        self.fields['contato'].widget.attrs['placeholder'] = 'Email ou Telefone'
        self.fields['contato'].widget.attrs['class'] = 'w-full py-4 px-6 rounded-xl'

        self.fields['descricao'].widget.attrs['placeholder'] = 'Descrição da Organização'
        self.fields['descricao'].widget.attrs['class'] = 'w-full py-4 px-6 rounded-xl'
