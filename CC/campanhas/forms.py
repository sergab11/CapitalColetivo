from django import forms
from .models import Campanha, Doacao, Recompensa, Emprestimo

class CampanhaForm(forms.ModelForm):
    class Meta:
        model = Campanha
        fields = ['titulo', 'tipo_crowdfunding', 'data_inicio', 'data_fim', 'meta', 'descricao', 'modo']
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'data_fim': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(CampanhaForm, self).__init__(*args, **kwargs)
        self.fields['titulo'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Título'})
        self.fields['descricao'].widget.attrs.update({'class': 'form-textarea', 'placeholder': 'Descrição'})
        self.fields['meta'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Meta'})
        self.fields['modo'].widget.attrs.update({'class': 'form-select'})
        self.fields['tipo_crowdfunding'].widget.attrs.update({'class': 'form-select'})

class DoacaoForm(forms.ModelForm):
    class Meta:
        model = Doacao
        fields = ['valor_1', 'valor_2', 'valor_3', 'valor_4', 'valor_5']

    def __init__(self, *args, **kwargs):
        super(DoacaoForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-input', 'placeholder': 'Valor de Doação'})

class RecompensaForm(forms.ModelForm):
    class Meta:
        model = Recompensa
        fields = ['nome_1', 'tipo_1', 'descricao_1', 'valor_1', 
                  'nome_2', 'tipo_2', 'descricao_2', 'valor_2',
                  'nome_3', 'tipo_3', 'descricao_3', 'valor_3',
                  'nome_4', 'tipo_4', 'descricao_4', 'valor_4',
                  'nome_5', 'tipo_5', 'descricao_5', 'valor_5']

    def __init__(self, *args, **kwargs):
        super(RecompensaForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-input', 'placeholder': 'Recompensa'})

class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ['taxa_juros',
                  'porcentagem_colaborador',
                  'porcentagem_organizacao',
                  'prazo_retorno',
                  'valor_sugerido_1',
                  'valor_sugerido_2',
                  'valor_sugerido_3',
                  'valor_sugerido_4'
                  ]
        
        widgets = {
            'prazo_retorno': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(EmprestimoForm, self).__init__(*args, **kwargs)
        self.fields['taxa_juros'].label = 'Taxa de Juros (%)'
        self.fields['porcentagem_colaborador'].label = 'Aquisição Juros - Colaborador (%)'
        self.fields['porcentagem_organizacao'].label = 'Aquisição Juros - Organização (%)'
        self.fields['prazo_retorno'].label = 'Prazo de Retorno'
        self.fields['valor_sugerido_1'].label = 'Valor Sugerido 1 (R$)'
        self.fields['valor_sugerido_2'].label = 'Valor Sugerido 2 (R$)'
        self.fields['valor_sugerido_3'].label = 'Valor Sugerido 3 (R$)'
        self.fields['valor_sugerido_4'].label = 'Valor Sugerido 4 (R$)'

        self.fields['taxa_juros'].widget.attrs.update({'label': 'Taxa de Juros (%)', 'class': 'form-input', 'placeholder': 'Juros (%)'})
        self.fields['porcentagem_colaborador'].widget.attrs.update({'label': 'Porcentagem Juros Colaborador (%)', 'class': 'form-input', 'placeholder': 'Colaborador (%)'})
        self.fields['porcentagem_organizacao'].widget.attrs.update({'label': 'Porcentagem Juros Organização (%)', 'class': 'form-input', 'placeholder': 'Organização (%)'})
