from django.db import models
from projetos.models import Projeto

class Campanha(models.Model):
    ACESSO_IMEDIATO = 'ACESSO_IMEDIATO'
    TUDO_OU_NADA = 'TUDO_OU_NADA'
    
    MODOS_CHOICES = [
        (ACESSO_IMEDIATO, 'Acesso Imediato'),
        (TUDO_OU_NADA, 'Tudo ou Nada')
    ]

    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    meta = models.DecimalField(max_digits=10, decimal_places=2)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    arrecadacao_atual = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    modo = models.CharField(max_length=20, choices=MODOS_CHOICES, null=True, blank=True)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='campanhas', null=True, blank=True)
    em_andamento = models.BooleanField(default=True)  # True para "Em Andamento", False para "Concluída"
    tipo_crowdfunding = models.ForeignKey('TipoCrowdfunding', on_delete=models.CASCADE, related_name='campanhas')

    def __str__(self):
        return self.titulo
    
    def percentual_arrecadado(self):
        if self.meta > 0:
            return (self.arrecadacao_atual / self.meta) * 100
        return 0
    

class Doacao(models.Model):
    campanha = models.ForeignKey(Campanha, on_delete=models.CASCADE, related_name='doacoes')

    valor_1 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_3 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_4 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_5 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.campanha.titulo


class TipoCrowdfunding(models.Model):
    DOACAO = 'DOACAO'
    RECOMPENSA = 'RECOMPENSA'
    EMPRESTIMO = 'EMPRESTIMO'

    TIPOS_CHOICES = [
        (DOACAO, 'Doação'),
        (RECOMPENSA, 'Recompensa'),
        (EMPRESTIMO, 'Empréstimo')
    ]

    tipo = models.CharField(max_length=10, choices=TIPOS_CHOICES)

    def __str__(self):
        return self.get_tipo_display()



class Recompensa(models.Model):
    campanha = models.ForeignKey(Campanha, on_delete=models.CASCADE, related_name='recompensa')

    nome_1 = models.CharField(max_length=255, null=True, blank=True)
    tipo_1 = models.CharField(max_length=255, null=True, blank=True)
    descricao_1 = models.TextField(null=True, blank=True)
    valor_1 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    nome_2 = models.CharField(max_length=255, null=True, blank=True)
    tipo_2 = models.CharField(max_length=255, null=True, blank=True)
    descricao_2 = models.TextField(null=True, blank=True)
    valor_2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    nome_3 = models.CharField(max_length=255, null=True, blank=True)
    tipo_3 = models.CharField(max_length=255, null=True, blank=True)
    descricao_3 = models.TextField(null=True, blank=True)
    valor_3 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    nome_4 = models.CharField(max_length=255, null=True, blank=True)
    tipo_4 = models.CharField(max_length=255, null=True, blank=True)
    descricao_4 = models.TextField(null=True, blank=True)
    valor_4 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    nome_5 = models.CharField(max_length=255, null=True, blank=True)
    tipo_5 = models.CharField(max_length=255, null=True, blank=True)
    descricao_5 = models.TextField(null=True, blank=True)
    valor_5 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.campanha.titulo


class Emprestimo(models.Model):
    campanha = models.ForeignKey(Campanha, on_delete=models.CASCADE, related_name='emprestimo')

    taxa_juros = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    porcentagem_colaborador = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    porcentagem_organizacao = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    prazo_retorno = models.DateField(null=True, blank=True)

    valor_sugerido_1 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_sugerido_2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_sugerido_3 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_sugerido_4 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.campanha.titulo