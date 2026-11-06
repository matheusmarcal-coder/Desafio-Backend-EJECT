from django.db import models

from django.core.validators import MinValueValidator

from django.contrib.auth.models import AbstractUser


    # """Classe personalizada de usuário que estende o modelo AbstractUser do Django."""
class Usuario(AbstractUser):
    #"""Define os papéis disponíveis para o usuário, representando CLIENTES e LOJISTA (papéis)."""
    class Papel(models.TextChoices):
        CLIENTE = 'cliente', 'Cliente'
        LOJISTA = 'lojista', 'Lojista'
    #"""Campo de email do usuário, definido como único e obrigatório."""
    email = models.EmailField(unique = True, blank = False, null = False)
     
    papel = models.CharField(
        max_length = 10,
        choices=Papel.choices,
        default=Papel.CLIENTE
        )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'papel']

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email



class Cliente(models.Model):

    #"""Representa um cliente e suas características."""

    usuario = models.OneToOneField(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='cliente',
    )

    nome = models.CharField(max_length = 100)
    email = models.EmailField(blank = False, max_length = 30)
    cpf = models.CharField(max_length = 11)
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length = 14)


    def __str__(self):
        
        #"""Retorna uma representação em string do cliente."""
       return f"{self.nome} | {self.email} | {self.cpf} | {self.data_nascimento} | {self.telefone}"

class Categoria(models.Model):
    #"""Representa as categorias de produtos disponíveis."""
    nome = models.CharField(max_length = 100)
    def __str__(self):
        #"""Retorna uma representação em string da categoria."""
        return f"{self.nome}"


class Produto(models.Model):
 #"""Representa um produto e suas características.(estoque não fica no produto, e sim nas variações)"""

    nome = models.CharField(max_length = 100)
    preco = models.DecimalField(max_digits = 10, decimal_places = 2, validators = [MinValueValidator(0.01)])
    categoria= models.ForeignKey(Categoria, on_delete = models.CASCADE)

    ativo = models.BooleanField(default = True)
    def __str__(self):
    #"""Retorna uma representação em string do produto."""
        return f"{self.nome} | {self.categoria} | Produto ativo? {self.ativo}"





class Variacao(models.Model):
     #"""Representa uma variação de produto e suas características."""
    Produto = models.ForeignKey(
        Produto,
        related_name='variacoes',
        on_delete=models.CASCADE,    
    )
    #"""Define os tamanhos disponíveis para a variação do produto, representando diferentes opções de tamanho. (incluindo "Único" como variação)"""
    class Tamanho (models.TextChoices):
        P = 'P', 'Pequeno'
        M = 'M', 'Médio'
        G = 'G', 'Grande'
        GG = 'GG', 'Extra Grande'
        XGG = 'XGG', 'Extra Extra Grande'
        Único = 'Único', 'Único'

    tamanho = models.CharField(
        max_length=10,
        choices=Tamanho.choices
    )
    cor = models.CharField(max_length=50)
    estoque = models.PositiveIntegerField(default=0)