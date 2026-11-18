from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser


# Classe personalizada de usuário que estende o modelo AbstractUser do Django.
class Usuario(AbstractUser):

    # Define os papéis disponíveis para o usuário, representando CLIENTES e LOJISTA (papéis).
    class Papel(models.TextChoices):
        CLIENTE = 'cliente', 'Cliente'
        LOJISTA = 'lojista', 'Lojista'

    # Campo de email do usuário, definido como único e obrigatório, além dos outros requisitos para registro de usuário.
    email = models.EmailField(unique = True, blank = False, null = False)

    nome_completo = models.CharField(max_length = 100, blank = True)
    cpf = models.CharField(max_length = 11, blank = True, null = True, unique = True)
    data_nascimento = models.DateField(blank = True, null = True)
    telefone = models.CharField(max_length = 14, blank = True)
    cep = models.CharField(max_length = 8, blank = True)
    endereco = models.CharField(max_length=255, blank = True)
    papel = models.CharField(max_length = 10, choices=Papel.choices, default=Papel.CLIENTE)
    # Definindo que o username padrão do Django será referenciado pelo email único, e que o username(email) e papel do usuário, devem ser obrigatórios na identifação do SUPERUSUÁRIO, quando esse for criado
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'papel']

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Cliente(models.Model):
    # Representa um cliente e suas características herdadas do registro
    usuario = models.OneToOneField( Usuario, on_delete=models.CASCADE, related_name='cliente',)
    
    def __str__(self):    
        # Retorna uma representação em string do cliente.
        return f"{self.usuario.nome_completo} | {self.usuario.email} | {self.usuario.cpf} | {self.usuario.data_nascimento} | {self.usuario.telefone} | {self.usuario.cpf} | {self.usuario.endereco} | {self.usuario.cep}"


class Categoria(models.Model):
    # Representa as categorias de produtos disponíveis.
    nome = models.CharField(max_length = 100)

    def __str__(self):
        # Retorna uma representação em string da categoria.
        return f"{self.nome}"


class Produto(models.Model):
 # Representa um produto e suas características.(estoque não fica no produto, e sim nas variações)
    nome = models.CharField(max_length = 100)
    preco = models.DecimalField(max_digits = 10, decimal_places = 2, validators = [MinValueValidator(0.01)])
    categoria= models.ForeignKey(Categoria, on_delete = models.CASCADE)
    
    # Define se o produto criado está ativo na plataforma ou não
    ativo = models.BooleanField(default = True)

    def __str__(self):
    # Retorna uma representação em string do produto.
        return f"{self.nome} | {self.categoria} "


class Variacao(models.Model):
    # Representa uma variação de produto e suas características.
    Produto = models.ForeignKey( Produto, related_name='variacoes', on_delete=models.CASCADE,)

    # Define os tamanhos disponíveis para a variação do produto, representando diferentes opções de tamanho. (incluindo "Único" como variação), além da representação do campo COR e do campo estoque, que deve ser um número positivo
    class Tamanho (models.TextChoices):
        P = 'P', 'Pequeno'
        M = 'M', 'Médio'
        G = 'G', 'Grande'
        GG = 'GG', 'Extra Grande'
        XGG = 'XGG', 'Extra Extra Grande'
        Único = 'Único', 'Único'
    tamanho = models.CharField(max_length=10, choices=Tamanho.choices)
    cor = models.CharField(max_length=50)
    estoque = models.PositiveIntegerField(default=0)


class Carrinho(models.Model):
    # Estabelece a relação cardinal de 1:1 com cliente e carrinho 
    usuario = models.OneToOneField(Usuario, on_delete = models.CASCADE)

    finalizado= models.BooleanField(default = False)


class ItemCarrinho(models.Model):
    # Estabelecendo a relação de 1 carrinho : N itens carrinho apartir do uso da ForeignKey (cardinalidade 1:N)
    carrinho = models.ForeignKey(Carrinho, on_delete = models.CASCADE)

    # Estabelecendo a relação de 1 variação : N itens carrinho (exemplo: variação -  camisa M + azul ; como item_carrinho representa a variação presente dentro do carrinho [com sua respectiva quantidade], podemos ter por exemplo: JOÃO com a variação 1 no seu carrinho[item_carrinho] e ter a MARIA com a mesma variação 1 em seu carrinho [item_carrinho])
    variacao = models.ForeignKey(Variacao, on_delete = models.CASCADE)

    # Número de variações selecionadas por carrinho, como padrão, começando com quantidade de itens 1
    quantidade_itens = models.PositiveIntegerField(default = 1)

    # Evitando 2 ou mais registros de uma MESMA variação no MESMO carrinho, as variações serão somadas por quantidades
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['carrinho', 'variacao'],
                name= 'item_unico_por_carrinho'
            )
        ]


class MetodoPagamento(models.Model):
    # Métodos de pagamento disponíveis para a compra do pedido
    PAGAMENTO_CHOICES = [
        ('pix', 'PIX'),
        ('credito', 'Crédito'),
        ('debito', 'Débito'),
    ]
    apelido = models.CharField(max_length=255)
    usuario = models.ForeignKey(Usuario, on_delete = models.CASCADE, related_name='metodos_pagamento' )
    tipo_pagamento = models.CharField(max_length=10, choices=PAGAMENTO_CHOICES)
    cartao_final = models.CharField(max_length=4, blank = True)

    def __str__(self):
        return f"{self.usuario.username} | {self.tipo_pagamento}"

    
class Pedido (models.Model):
    # Status rascunho para quando o cliente finaliza o carrinho mas ainda não realizou o pedido (o carrinho é esvaziado, mas o pedido é guardado no rascunho)
    STATUS_CHOICES = [
        ('rascunho', 'Rascunho'),
        ('pendente', 'PENDENTE'),
        ('confirmado','CONFIRMADO'),
        ('enviado','ENVIADO'),
        ('entregue','ENTREGUE'),
        ('cancelado','CANCELADO')
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices = STATUS_CHOICES, default = 'rascunho')

    cep_entrega = models.CharField(max_length=8, blank = True)
    rua_entrega = models.CharField(max_length=255, blank = True)
    numero_entrega = models.CharField(max_length=10,blank = True)
    bairro_entrega =models.CharField(max_length=255, blank = True)
    cidade_entrega = models.CharField(max_length=255, blank = True)
    uf_entrega = models.CharField(max_length=2, blank = True)

    metodo_pagamento = models.CharField(max_length=10, choices = MetodoPagamento.PAGAMENTO_CHOICES ,blank = True)
    pedido_criado = models.DateTimeField(auto_now_add=True)

    


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name= 'itens_pedido')
    variacao_pedido = models.ForeignKey(Variacao, on_delete=models.PROTECT)
    #Quantidade de itens da variação por carrinho finalizado
    quantidade = models.PositiveIntegerField()
    #Preço unitário de um único item da variação 
    preco_unitario = models.DecimalField(max_digits= 10, decimal_places=2)

    def __str__(self):
        return f"Item{self.id} - Pedido{self.pedido.id}"