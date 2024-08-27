from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model

class Banco(models.Model):
    cod = models.PositiveIntegerField()
    nome = models.CharField(max_length=255)

    class Meta:
        ordering = ('cod',) 
        
        verbose_name_plural = 'Bancos'

    def __str__(self):
        return self.nome

class OrganizacaoCaptadora(models.Model):
    nome = models.CharField(max_length=255)
    titular_conta = models.CharField(max_length=50, validators=[RegexValidator(regex='^[a-zA-Z ]+$', message='Nome do titular deve conter apenas letras e espaços')])
    numero_conta = models.PositiveIntegerField()
    agencia_bancaria = models.PositiveIntegerField()
    banco = models.ForeignKey(Banco, on_delete=models.CASCADE, related_name='organizacoes')
    cpf_cnpj = models.CharField(max_length=20)
    contato = models.CharField(max_length=255)
    descricao = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    criador = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True, related_name='organizacoes')

    def __str__(self):
        return self.nome