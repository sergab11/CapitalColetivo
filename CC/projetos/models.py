from django.db import models
from usuarios.models import Usuario  # Importe a classe Usuário do app usuarios
from organizacoes.models import OrganizacaoCaptadora  # Importe a classe Organizacao do app organizacoes
from usuarios.models import Interesse

class Projeto(models.Model):
    titulo = models.CharField(max_length=255, default='')
    imagem_perfil = models.ImageField(upload_to='projeto_imagens/', default='default_projeto.jpg')
    texto = models.TextField(max_length=5000, default='')
    categoria = models.ForeignKey(Interesse, related_name='projetos', blank=True, null=True, on_delete=models.CASCADE)
    imagem1 = models.ImageField(upload_to='imagens_pitch_deck/', blank=True, null=True)
    imagem2 = models.ImageField(upload_to='imagens_pitch_deck/', blank=True, null=True)
    imagem3 = models.ImageField(upload_to='imagens_pitch_deck/', blank=True, null=True)
    data_criacao = models.DateField(auto_now_add=True, blank=True, null=True)
    tem_campanha = models.BooleanField(default=False)
    
    # Relacionamento Many-to-Many com Usuário (da classe Usuario no app usuarios)
    membros = models.ManyToManyField(Usuario, through='MembroProjeto')
    
    # Relacionamento One-to-One com Organizacao (da classe Organizacao no app organizacoes)
    organizacao_captadora = models.ForeignKey(OrganizacaoCaptadora, on_delete=models.CASCADE, related_name='projetos', null=True, blank=True)

    def __str__(self):
        return self.titulo

class MembroProjeto(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    FUNCAO_CHOICES = (
        ('MEMBRO', 'Membro'),
        ('ADMINISTRADOR', 'Administrador'),
    )
    funcao = models.CharField(max_length=15, choices=FUNCAO_CHOICES, default='MEMBRO')
    data_inclusao = models.DateField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f'{self.usuario} - {self.projeto} ({self.funcao})'
