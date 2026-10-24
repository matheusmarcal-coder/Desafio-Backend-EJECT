from django.db import models

from django.core.validators import MinValueValidator

class cliente(models.Model):
    nome = models.CharField(max_length = 100)
    email = models.EmailField(blank = False, max_length = 30)
    cpf = models.CharField(max_length = 11)
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length = 14)


    def __str__(self):
        return self.nome 

class produto(models.Model):

    CATEGORIA = (
        ('Calç', 'Calças'),
        ('Berm', 'Bermudas'),
        ('Blus', 'Blusas'),
        ('Rega', 'Regatas'),
        ('Vest', 'Vestidos'),
        ('Shor', 'Shorts'),
        ('Saia', 'Saias'),

    )

    nome = models.CharField(max_length = 100)
    preco = models.DecimalField(max_digits = 10, decimal_places = 2, validators = [MinValueValidator(0.01)])
    categoria= models.CharField(max_length = 4, blank = False, null=False, choices = CATEGORIA)

    def __str__(self):
        return self.nome 


