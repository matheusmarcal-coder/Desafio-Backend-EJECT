from rest_framework import serializers
from NewStyle.models import Cliente, Produto, Categoria, Variacao, Usuario, ItemCarrinho, ItemPedido, Pedido,  MetodoPagamento
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 



# Serializer para o modelo Usuario, incluindo o campo de senha.
class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    # Define a classe Meta para o serializer, especificando o modelo Usuario e os campos a serem incluídos.
    class Meta:
        model = Usuario
        fields = [ 'email', 'password', 'nome_completo', 'cpf', 'telefone', 'data_nascimento', 'cep', 'endereco' ]
        extra_kwargs = {
            'email' : {'required' : True, 'allow_blank' : False, 'allow_null' : False},
            'nome_completo' : {'required' : True, 'allow_blank' : False},
            'cpf' : {'required' : True, 'allow_blank' : False, 'allow_null' : False},
            'telefone' : {'required' : True, 'allow_blank' : False},
            'data_nascimento' : {'required' : True, 'allow_null' : False},
            'cep' : {'required' : True, 'allow_blank' : False},
            'endereco' : {'required' : True,  'allow_blank' : False}
        }

    def validate_telefone(self, numero):
        if not numero.isdigit() or len(numero) != 11:
            raise serializers.ValidationError("O número de telefone deve conter 11 dígitos, incluindo o DDD.")
        numero = numero [0:2] + " " + numero [2:7] + "-" + numero[7:11]
        return numero 
    
    # Definindo os campos de registro para o usuario 
    def create(self, validated_data):
            usuario = Usuario(

                # Define o email do usuário (único) a partir dos dados validados fornecidos.
                username= validated_data['email'],
                
                email = validated_data['email'],
                nome_completo = validated_data['nome_completo'],
                cpf = validated_data['cpf'],
                telefone = validated_data['telefone'],
                data_nascimento = validated_data['data_nascimento'],
                cep = validated_data['cep'],
                endereco = validated_data['endereco'],

                # Define o papel do usuário em seu registro como CLIENTE por padrão.
                papel = Usuario.Papel.CLIENTE
            )

    # Define a senha do usuário usando o método set_password para garantir que seja armazenada de forma segura(hash).
            usuario.set_password(validated_data['password'])
            usuario.save()

            # Criação de cliente de acordo com os dados fornecidos no registro para usuario
            Cliente.objects.create(usuario= usuario)
            return usuario
    
# Quando consultado, retorna apenas o usuário e seu respectivo ID (quando esse é cliente)
class ClienteSerializer (serializers.ModelSerializer): 
    class Meta:
        model = Cliente 
        fields = ['id', 'usuario']
        read_only_fields = ['usuario']


# Classe feita para, além de verificar o login do usuário, retorna o papel do usuário (cliente ou lojista)
class LoginSerializer(TokenObtainPairSerializer): 
    def validate(self, attrs):
        dados = super().validate(attrs)
        dados['papel'] = self.user.papel 
        return dados


class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        exclude = []


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        exclude = []


class VariacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variacao
        exclude = []


class ItemCarrinhoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCarrinho 
        exclude = []
        read_only_fields = ['carrinho']

    def validate_quantidade_itens(self, value):
        if value <= 0 : 
            raise serializers.ValidationError (
                "A quantidade inserida no carrinho deve ser maior que 0"
            )
        else : 
            return value 
        
    # Verificamos se a variação adcionada pelo cliente está contida em um produto ativo
    def validate_variacao(self, value):
        if value.Produto.ativo is False:
            raise serializers.ValidationError (
                "A variação inserida no carrinho deve estar contida em um produto ativo"
            )
        else: 
            return value 
        
    # Situação onde o cliente está ATUALIZANDO uma variação já existente no carrinho: Se ele está atualizando uma variação existente -> impedimos a troca de variação no meio do processo ; caso contrário -> recuperamos a variação original e atualizamos o estoque 
    def validate(self, attrs):
        quantidade_itens = attrs.get('quantidade_itens')
        variacao = attrs.get('variacao')
        if self.instance is not None:
            if variacao is not None:
                raise serializers.ValidationError("Não é permitido alterar a variação")
            variacao = self.instance.variacao
        if quantidade_itens is not None and quantidade_itens > variacao.estoque: 
            raise serializers.ValidationError("A quantidade de itens adcionada não pode exceder a variação de estoque da loja")
        return attrs


class ItemPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model =  ItemPedido
        fields = ['id', 'variacao_pedido', 'quantidade', 'preco_unitario']
        read_only_fields = fields 


class PedidoSerializer(serializers.ModelSerializer):
    itens_pedido = ItemPedidoSerializer(many = True, read_only = True)
    class Meta:
        model = Pedido
        fields = ['id', 'status', 'uf_entrega', 'cep_entrega' , 'rua_entrega', 'numero_entrega', 'bairro_entrega', 'cidade_entrega','metodo_pagamento', 'pedido_criado', 'itens_pedido']
        read_only_fields = fields


class ConfirmarPedidoSerializer(serializers.Serializer):

    cep_entrega = serializers.CharField(max_length=8, min_length = 8)
    rua_entrega = serializers.CharField(max_length=255)
    numero_entrega = serializers.CharField(max_length=10)
    bairro_entrega =serializers.CharField(max_length=255)
    cidade_entrega = serializers.CharField(max_length=255)
    uf_entrega = serializers.CharField(max_length=2, min_length = 2)

    # Identifica o metodo de pagamento selecionado pelo cliente por ID
    metodo_pagamento_id = serializers.IntegerField(min_value = 1)

    def valitade_cep_entrega(self,value):
        if not value.isdigit():
            raise serializers.ValidationError('O campo CEP precisa apenas conter números.')
        else:
            return value

class AtualizarStatusPedidoSerializer(serializers.Serializer):
    status = serializers.ChoiceField(  
        choices = ['confirmado', 'enviado','entregue','cancelado']
    )


class MetodoPagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetodoPagamento
        fields = ['id', 'tipo_pagamento', 'cartao_final', 'apelido']
        read_only_fields = ['id']

    def validate(self, attrs):
        tipo = attrs.get('tipo_pagamento')
        cartao = attrs.get ('cartao_final', '')
        # Quando o tipo de pagamento escohido é cartão (crédito ou débito), o usuário deve digitar os últimos números do cartão (devem ser obrigatóriamente 4 dígitos e o campo deve apresentar apenas números)
        if tipo in ['credito', 'debito']:
            if len(cartao) != 4 or not cartao.isdigit():
                raise serializers.ValidationError({'cartao_final' : 'Informe apenas os 4 últimos dígitos do seu cartão.'})

        elif tipo == 'pix':
            attrs['cartao_final'] = ''

        return attrs


class EsqueciSenhaSerializer(serializers.Serializer):
    email = serializers.EmailField()


class RedefinirSenhaSerializer(serializers.Serializer):
    uid= serializers.CharField()
    token= serializers.CharField()
    nova_senha= serializers.CharField(write_only=True)
