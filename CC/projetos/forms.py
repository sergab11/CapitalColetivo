from django import forms
from .models import Projeto, MembroProjeto
from usuarios.models import Interesse, Usuario


class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = ['titulo', 'categoria', 'imagem_perfil', 'texto', 'imagem1', 'imagem2', 'imagem3']
    
    def __init__(self, *args, **kwargs):
        super(ProjetoForm, self).__init__(*args, **kwargs)
        
        # Campo título
        self.fields['titulo'] = forms.CharField(
            max_length=255,
            required=True,
            widget=forms.TextInput(attrs={'placeholder': 'Título do Projeto'})
        )
        
        # Campo imagem_perfil
        self.fields['imagem_perfil'] = forms.ImageField(
            required=True,
            widget=forms.ClearableFileInput()
        )
        
        # Campo texto
        self.fields['texto'] = forms.CharField(
            max_length=5000,
            required=True,
            widget=forms.Textarea(attrs={'placeholder': 'Descrição do Projeto', 'rows': 10, 'cols':10})
        )
        
        # Campo imagem1
        self.fields['imagem1'] = forms.ImageField(
            required=False,
            widget=forms.ClearableFileInput()
        )

        self.fields['categoria'].queryset = Interesse.objects.all()
        
        # Campo imagem2
        self.fields['imagem2'] = forms.ImageField(
            required=False,
            widget=forms.ClearableFileInput()
        )
        
        # Campo imagem3
        self.fields['imagem3'] = forms.ImageField(
            required=False,
            widget=forms.ClearableFileInput()
        )
        

class MembroProjetoForm(forms.ModelForm):
    '''email = forms.EmailField(label='Email do Membro', required=False)
    
    class Meta:
        model = MembroProjeto
        fields = ['email', 'funcao']
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        
        if email:
            # Busca ou cria o usuário com base no email fornecido
            usuario, created = Usuario.objects.get_or_create(email=email)
            self.instance.usuario = usuario  # Define o usuário associado ao objeto MembroProjeto
        
        return cleaned_data'''
    
    class Meta:
        model = MembroProjeto
        fields = ['email', 'funcao']
    
    email = forms.EmailField(label='Email do Membro', required=False)
    funcao = forms.ChoiceField(
        choices=MembroProjeto.FUNCAO_CHOICES,
        required=False,
        widget=forms.Select
    )
