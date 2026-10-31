from django.db import models

from django.core.validators import MinValueValidator

class Cliente(models.Model):

    #"""Representa um cliente e suas características."""

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
 #"""Representa um produto e suas características."""

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
    tamanho = models.CharField(max_length=50)
    cor = models.CharField(max_length=50)
    estoque = models.PositiveIntegerField(default=0)