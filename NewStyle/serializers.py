from rest_framework import serializers

from NewStyle.models import Cliente, Produto, Categoria, Variacao, Usuario, ItemCarrinho

from django.contrib.auth.password_validation import validate_password

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 



class ClienteSerializer (serializers.ModelSerializer): 
    class Meta:
        model = Cliente 
        fields = ['id', 'usuario']
        read_only_fields = ['usuario']

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class VariacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variacao
        exclude = []


#"""Serializer para o modelo Usuario, incluindo o campo de senha."""
class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    #"""Define a classe Meta para o serializer, especificando o modelo Usuario e os campos a serem incluídos."""
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
            raise serializers.ValidationError(
                "O número de telefone deve conter 11 dígitos, incluindo o DDD."
            )
        numero = numero [0:2] + " " + numero [2:7] + "-" + numero[7:11]
        return numero 
    #Definindo os campos de registro para o usuario 
    def create(self, validated_data):
            usuario = Usuario(
                #"""Define o email do usuário (único) a partir dos dados validados fornecidos."""
                username= validated_data['email'],
                
                email = validated_data['email'],
                
                nome_completo = validated_data['nome_completo'],

                cpf = validated_data['cpf'],

                telefone = validated_data['telefone'],

                data_nascimento = validated_data['data_nascimento'],

                cep = validated_data['cep'],

                endereco = validated_data['endereco'],
                #"""Define o papel do usuário em seu registro como CLIENTE por padrão."""
                papel = Usuario.Papel.CLIENTE
            )
    #"""Define a senha do usuário usando o método set_password para garantir que seja armazenada de forma segura(hash)."""
            usuario.set_password(validated_data['password'])
            usuario.save()
            # Criação de cliente de acordo com os dados fornecidos no registro para usuario
            Cliente.objects.create(usuario= usuario)
            return usuario
    
#""Classe feita para, além de verificar o login do usuário, retornar o papel do usuário (cliente ou lojista)""
class LoginSerializer(TokenObtainPairSerializer): 

    def validate(self, attrs):
        dados = super().validate(attrs)

        dados['papel'] = self.user.papel 

        return dados


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
                raise serializers.ValidationError(
                    "Não é permitido alterar a variação"
                )
            variacao = self.instance.variacao

        if quantidade_itens is not None and quantidade_itens > variacao.estoque: 
            raise serializers.ValidationError(
                "A quantidade de itens adcionada não pode exceder a variação de estoque da loja"
            )
        return attrs