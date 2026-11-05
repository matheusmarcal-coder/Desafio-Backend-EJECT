from NewStyle.models import Cliente, Produto, Categoria, Variacao 

from NewStyle.serializers import ClienteSerializer, ProdutoSerializer, CategoriaSerializer, VariacaoSerializer, RegistroSerializer

from rest_framework import viewsets, status 

from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework.permissions import AllowAny, DjangoModelPermissionsOrAnonReadOnly, IsAuthenticated 


class ClienteViewSet(viewsets.ModelViewSet): 
    #""Exige autenticação via JWT para acessar os dados dos clientes
    permission_classes = [IsAuthenticated]
    serializer_class = ClienteSerializer 
    #"""Define o conjunto de consultas (queryset) para o ViewSet de Cliente, filtrando os clientes associados ao usuário autenticado e ordenando-os pelo campo 'id'."""
    def get_queryset(self):
         return Cliente.objects.filter(
              usuario=self.request.user
         ).order_by('id')

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all().order_by('id')
    serializer_class = ProdutoSerializer 
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all().order_by('id')
    serializer_class = CategoriaSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

class VariacaoViewSet(viewsets.ModelViewSet):
    queryset = Variacao.objects.all().order_by('id')
    serializer_class = VariacaoSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly] 
    def perform_create(self, serializer):
            serializer.save(Produto_id=self.kwargs['Produto_id'])

class RegistroView(APIView):
    #""Define que usuários sem autenticação possam criar uma conta ("AllowAny")""
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

