from django.db import models

from django.core.validators import MinValueValidator

from django.contrib.auth.models import AbstractUser


    # """Classe personalizada de usuário que estende o modelo AbstractUser do Django."""
class Usuario(AbstractUser):
    #"""Define os papéis disponíveis para o usuário, representando CLIENTES e LOJISTA (papéis)."""
    class Papel(models.TextChoices):
        CLIENTE = 'cliente', 'Cliente'
        LOJISTA = 'lojista', 'Lojista'
    #"""Campo de email do usuário, definido como único e obrigatório, além das atribuições para registro de usuário."""
    email = models.EmailField(unique = True, blank = False, null = False)
    nome_completo = models.CharField(max_length = 100, blank = True)
    cpf = models.CharField(max_length = 11, blank = True, null = True, unique = True)
    data_nascimento = models.DateField(blank = True, null = True)
    telefone = models.CharField(max_length = 14, blank = True)
    cep = models.CharField(max_length = 8, blank = True)
    endereco = models.CharField(max_length=255, blank = True)
     
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

    #"""Representa um cliente e suas características herdadas do registro"""

    usuario = models.OneToOneField(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='cliente',
    )
    def __str__(self):
        
        #"""Retorna uma representação em string do cliente."""
       return f"{self.usuario.nome_completo} | {self.usuario.email} | {self.usuario.cpf} | {self.usuario.data_nascimento} | {self.usuario.telefone} | {self.usuario.cpf} | {self.usuario.endereco} | {self.usuario.cep}"

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
        return f"{self.nome} | {self.categoria} "



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

class Carrinho(models.Model):
    # Estabelece a relação cardinal de 1:1 com cliente e carrinho 
    usuario = models.OneToOneField(Usuario, on_delete = models.CASCADE)



class ItemCarrinho(models.Model):
    # Estabelecendo a relação de 1 carrinho : N itens carrinho apartir do uso da ForeignKey (cardinalidade 1:N)
    carrinho = models.ForeignKey(Carrinho, on_delete = models.CASCADE)
    # Estabelecendo a relação de 1 variação : N itens carrinho (exemplo: variação -  camisa M + azul ; itens - 3 itens dessa variação)
    variacao = models.ForeignKey(Variacao, on_delete = models.CASCADE)
    # Número de variações selecionadas por carrinho, como padrão, começando com quantidade de itens 1
    quantidade_itens = models.PositiveIntegerField(default = 1)
    #Evitando 2 ou mais registros de uma MESMA variação no MESMO carrinho, as variações serão somadas por quantidades
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['carrinho', 'variacao'],
                name= 'item_unico_por_carrinho'
            )
        ]
    