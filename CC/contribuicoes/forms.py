from django import forms
from campanhas.models import Doacao, Recompensa, Emprestimo

class DoacaoForm(forms.ModelForm):
    class Meta:
        model = Doacao
        fields = ['valor_1', 'valor_2', 'valor_3', 'valor_4', 'valor_5']

class RecompensaForm(forms.ModelForm):
    class Meta:
        model = Recompensa
        fields = [
            'nome_1', 'tipo_1', 'descricao_1', 'valor_1',
            'nome_2', 'tipo_2', 'descricao_2', 'valor_2',
            'nome_3', 'tipo_3', 'descricao_3', 'valor_3',
            'nome_4', 'tipo_4', 'descricao_4', 'valor_4',
            'nome_5', 'tipo_5', 'descricao_5', 'valor_5'
        ]

class EmprestimoForm(forms.ModelForm):
    valor_emprestimo = forms.DecimalField(max_digits=10, decimal_places=2, required=False)

    class Meta:
        model = Emprestimo
        fields = ['taxa_juros',
                  'porcentagem_colaborador',
                  'porcentagem_organizacao',
                  'prazo_retorno',
                  'valor_sugerido_1',
                  'valor_sugerido_2',
                  'valor_sugerido_3',
                  'valor_sugerido_4']

    def clean(self):
        cleaned_data = super().clean()
        valor_emprestimo = cleaned_data.get('valor_emprestimo')
        valor_emprestimo_especifico = self.data.get('valor_emprestimo_especifico')

        if not valor_emprestimo and not valor_emprestimo_especifico:
            raise forms.ValidationError('Por favor, escolha um valor sugerido ou insira um valor específico.')

        if valor_emprestimo_especifico:
            try:
                valor_emprestimo_especifico = float(valor_emprestimo_especifico)
                cleaned_data['valor_contribuicao'] = valor_emprestimo_especifico
            except ValueError:
                raise forms.ValidationError('Valor específico inválido.')
        else:
            cleaned_data['valor_contribuicao'] = valor_emprestimo

        return cleaned_data


class DadosCartaoForm(forms.Form):
    nome_titular = forms.CharField(label='Nome do Titular', max_length=100)
    numero_cartao = forms.CharField(label='Número do Cartão', max_length=16)
    validade_cartao = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
        label='Validade do Cartão'
    )
    cvv_cartao = forms.CharField(label='CVV', max_length=4)