from NewStyle.models import cliente, produto 

from NewStyle.serializers import clienteSerializer, produtoSerializer 
from rest_framework import viewsets 

class clienteViewSet(viewsets.ModelViewSet): 
    queryset = cliente.objects.all()
    serializer_class = clienteSerializer 

class produtoViewSet(viewsets.ModelViewSet):
    queryset = produto.objects.all()
    serializer_class = produtoSerializer 