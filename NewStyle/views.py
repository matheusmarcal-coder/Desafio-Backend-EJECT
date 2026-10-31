from NewStyle.models import Cliente, Produto, Categoria 

from NewStyle.serializers import ClienteSerializer, ProdutoSerializer, CategoriaSerializer
from rest_framework import viewsets 

class ClienteViewSet(viewsets.ModelViewSet): 
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer 

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer 

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer