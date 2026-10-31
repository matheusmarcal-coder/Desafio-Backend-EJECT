from rest_framework import serializers

from NewStyle.models import Cliente, Produto, Categoria, Variacao

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