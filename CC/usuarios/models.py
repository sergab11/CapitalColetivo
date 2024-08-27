from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone


class Interesse(models.Model):
    nome = models.CharField(max_length=255)

    class Meta:
        ordering = ('nome',) 
        
        verbose_name_plural = 'Interesses'

    def __str__(self):
        return self.nome
    

class GerenciadorUsuario(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Voce não escreveu um email valido')
        
        email = self.normalize_email(email)
        usuario = self.model(email=email, **extra_fields)
        usuario.set_password(password)
        usuario.save(using=self._db)

        return usuario
    
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(email, password, **extra_fields)
    

class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=True, default='', unique=True)
    nome = models.CharField(max_length=255, blank=True, default='')
    data_nasc = models.DateField(null=True, blank=True)
    imagem_perfil = models.ImageField(upload_to='imagens_perfil/', null=True, blank=True)
    interesses = models.ManyToManyField(Interesse, related_name='usuarios')

    tem_organizacao = models.BooleanField(default=False)
    organizacao_id = models.PositiveIntegerField(null=True, blank=True, default=None)
    
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    data_entrou = models.DateTimeField(default=timezone.now)
    ultimo_login = models.DateField(blank=True, null=True)

    objects = GerenciadorUsuario()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def get_nome(self):
        return self.nome
    