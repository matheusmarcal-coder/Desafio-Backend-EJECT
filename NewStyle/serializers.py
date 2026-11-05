from rest_framework import serializers

from NewStyle.models import Cliente, Produto, Categoria, Variacao, Usuario 

from django.contrib.auth.password_validation import validate_password

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 


class ClienteSerializer (serializers.ModelSerializer): 
    class Meta:
        model = Cliente 
        fields = ['id', 'nome', 'email', 'cpf', 'data_nascimento','telefone']

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
        exclude = ["Produto"]


#"""Serializer para o modelo Usuario, incluindo o campo de senha."""
class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    #"""Define a classe Meta para o serializer, especificando o modelo Usuario e os campos a serem incluídos."""
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password']
    
    def create(self, validated_data):
            usuario = Usuario(
                username= validated_data['username'],
                #"""Define o email do usuário (único) a partir dos dados validados fornecidos."""
                email = validated_data['email'],
                #"""Define o papel do usuário como CLIENTE por padrão."""
                papel = Usuario.Papel.CLIENTE
            )
    #"""Define a senha do usuário usando o método set_password para garantir que seja armazenada de forma segura(hash)."""
            usuario.set_password(validated_data['password'])
            usuario.save()

            return usuario
#""Classe feita para, além de verificar o login do usuário, retornar o papel do usuário (cliente ou lojista)""
class LoginSerializer(TokenObtainPairSerializer): 

    def validate(self, attrs):
        dados = super().validate(attrs)

        dados['papel'] = self.user.papel 

        return dados