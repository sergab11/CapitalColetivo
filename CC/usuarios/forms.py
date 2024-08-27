# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario, Interesse

class FormCriaUsuario(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ( 'email', 'nome', 'data_nasc', 'password1', 'password2', 'imagem_perfil', 'interesses')

    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'Seu email',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

    nome = forms.CharField(max_length=255, required=True,widget=forms.TextInput(attrs={
        'placeholder': 'Digite um nome',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

    data_nasc = forms.DateField(required=True, widget=forms.SelectDateWidget(
        years=range(1924, 2024),
        months={
                1: ('Janeiro'), 2: ('Fevereiro'), 3: ('Março'), 4: ('Abril'),
                5: ('Maio'), 6: ('Junho'), 7: ('Julho'), 8: ('Agosto'),
                9: ('Setembro'), 10: ('Outubro'), 11: ('Novembro'), 12: ('Dezembro')
            }
        )
    )
    
    imagem_perfil = forms.ImageField(required=True)
    
    interesses = forms.ModelMultipleChoiceField(
        queryset=Interesse.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Interesses'
    )

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Sua senha',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirme sua senha',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))


    def __init__(self, *args, **kwargs):
        super(FormCriaUsuario, self).__init__(*args, **kwargs)


class FormLogin(forms.Form):
    email = forms.EmailField(label='Email', required=True)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput, required=True)

    def __init__(self, *args, **kwargs):
        super(FormLogin, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['email'].widget.attrs['class'] = 'w-full py-4 px-6 rounded-xl'

        self.fields['password'].widget.attrs['placeholder'] = 'Senha'
        self.fields['password'].widget.attrs['class'] = 'w-full py-4 px-6 rounded-xl'   