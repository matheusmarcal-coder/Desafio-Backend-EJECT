from rest_framework import serializers

from NewStyle.models import cliente, produto 

class clienteSerializer (serializers.ModelSerializer): 
    class Meta:
        model = cliente 
        fields = ['id', 'nome', 'email', 'cpf', 'data_nascimento','telefone']

class produtoSerializer(serializers.ModelSerializer):
    class Meta:
        model = produto
        fields = '__all__'