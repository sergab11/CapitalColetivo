from django.db import models
from django.contrib.auth import get_user_model
from campanhas.models import Campanha, Doacao, Recompensa, Emprestimo


class ContribuicaoFinanceira(models.Model):
    usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='contribuicoes')
    campanha = models.ForeignKey(Campanha, on_delete=models.CASCADE, related_name='contribuicoes')
    
    DOACAO = 'DOACAO'
    RECOMPENSA = 'RECOMPENSA'
    EMPRESTIMO = 'EMPRESTIMO'
    TIPOS_CROWDFUNDING = [
        (DOACAO, 'Doação'),
        (RECOMPENSA, 'Recompensa'),
        (EMPRESTIMO, 'Empréstimo'),
    ]

    tipo_crowd = models.CharField(max_length=10, choices=TIPOS_CROWDFUNDING, null=True, blank=True,)
    
    STATUS_ATIVA = 'Ativa'
    STATUS_FINALIZADA = 'Finalizada'
    STATUS_CANCELADA = 'Cancelada'
    STATUS_CHOICES = [
        (STATUS_ATIVA, 'Ativa'),
        (STATUS_FINALIZADA, 'Finalizada'),
        (STATUS_CANCELADA, 'Cancelada'),
    ]
    status_contrib = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ATIVA)
    
    crowd_id = models.PositiveIntegerField(null=True, blank=True,)
    data_contribuicao = models.DateTimeField(auto_now_add=True)
    valor_contribuicao = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,)
    detalhe_contribuicao = models.ForeignKey(Recompensa, null=True, blank=True, on_delete=models.SET_NULL, related_name='contribuicoes')

    # Novos campos para forma de pagamento
    FORMA_PAGAMENTO_CHOICES = [
        ('CARTAO', 'Cartão de Crédito/Débito'),
        ('PIX', 'Pix'),
    ]
    forma_pagamento = models.CharField(max_length=10, choices=FORMA_PAGAMENTO_CHOICES, blank=True, null=True)
    
    # Campos específicos para pagamento em cartão
    nome_titular = models.CharField(max_length=100, blank=True, null=True)
    numero_cartao = models.CharField(max_length=16, blank=True, null=True)
    validade_cartao = models.DateField(blank=True, null=True)
    cvv_cartao = models.CharField(max_length=4, blank=True, null=True)
    
    # Campos específicos para pagamento via Pix
    chave_pix = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return f'{self.usuario.nome} contribuiu {self.valor_contribuicao} para {self.campanha.titulo}'
    


class MotivosCancelamento(models.Model):
    MOTIVO_CHOICES = [
        ('CIRCUNSTANCIAS', 'Mudanças de Circunstâncias Pessoais'),
        ('GESTAO', 'Descontentamento com a Gestão da Campanha'),
        ('INFORMACOES', 'Informações Enganosas ou Falsas'),
        ('ATRASOS', 'Atrasos ou Falta de Progresso'),
        ('PREFERENCIA', 'Preferência por Outra Campanha'),
    ]

    motivo = models.CharField(max_length=50, choices=MOTIVO_CHOICES)

    def __str__(self):
        return self.get_motivo_display()
