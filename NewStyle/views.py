from NewStyle.models import Cliente, Produto, Categoria, Variacao 

from NewStyle.serializers import ClienteSerializer, ProdutoSerializer, CategoriaSerializer, VariacaoSerializer
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

class VariacaoViewSet(viewsets.ModelViewSet):
    queryset = Variacao.objects.all()
    serializer_class = VariacaoSerializer
    def perform_create(self, serializer):
            serializer.save(Produto_id=self.kwargs['Produto_id'])