from NewStyle.models import Cliente, Produto, Categoria, Variacao 

from NewStyle.serializers import ClienteSerializer, ProdutoSerializer, CategoriaSerializer, VariacaoSerializer, RegistroSerializer

from rest_framework import viewsets, status 

from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework.permissions import AllowAny


class ClienteViewSet(viewsets.ModelViewSet): 
    queryset = Cliente.objects.all().order_by('id')
    serializer_class = ClienteSerializer 

class ProdutoViewSet(viewsets.ModelViewSet):

    queryset = Produto.objects.all().order_by('id')
    serializer_class = ProdutoSerializer 

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all().order_by('id')
    serializer_class = CategoriaSerializer

class VariacaoViewSet(viewsets.ModelViewSet):
    queryset = Variacao.objects.all().order_by('id')
    serializer_class = VariacaoSerializer
    def perform_create(self, serializer):
            serializer.save(Produto_id=self.kwargs['Produto_id'])

class RegistroView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegistroSerializer(data = request.data)

        if serializer.is_valid():
            usuario = serializer.save()

            return Response(
             {
                  "mensagem" : "Usuário registrado com sucesso.",
                  "email" : usuario.email
             },
             status = status.HTTP_201_CREATED
        )

        return Response(
         serializer.errors,
         status=status.HTTP_400_BAD_REQUEST
    )

