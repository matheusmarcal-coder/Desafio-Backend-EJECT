from NewStyle.models import Cliente, Produto, Categoria, Usuario, Variacao 

from NewStyle.serializers import ClienteSerializer, ProdutoSerializer, CategoriaSerializer, VariacaoSerializer, RegistroSerializer

from rest_framework import viewsets, status 

from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework.permissions import AllowAny, DjangoModelPermissionsOrAnonReadOnly, IsAuthenticated 
from rest_framework.pagination import PageNumberPagination

from rest_framework.exceptions import ValidationError

from decimal import Decimal, InvalidOperation


class ClienteViewSet(viewsets.ModelViewSet): 
    #""Exige autenticação via JWT para acessar os dados dos clientes
    permission_classes = [IsAuthenticated]
    serializer_class = ClienteSerializer 
    #"""Define o conjunto de consultas (queryset) para o ViewSet de Cliente, filtrando os clientes associados ao usuário autenticado e ordenando-os pelo campo 'id'."""
    def get_queryset(self):
         return Cliente.objects.filter(
              usuario=self.request.user
         ).order_by('id')
    
# Classe responsável pela listagem de produtos, com no máximo 10 produtos por página 
class PaginacaoProdutos(PageNumberPagination):
    page_size = 10

# Mostra todos os produtos cadastrados no banco, ordenados por ID, e permite operações de leitura e escrita para usuários autenticados com permissões(lojista), enquanto usuários anônimos e clientes podem apenas ler os dados.
class ProdutoViewSet(viewsets.ModelViewSet):
    #""Define o conjunto de consultas (queryset) para o ViewSet de Produto, filtrando os produtos com base no papel do usuário autenticado. Se o usuário for um lojista, ele verá todos os produtos; caso contrário, apenas os produtos ativos serão exibidos."""
    queryset = Produto.objects.all().order_by('id')
    # Permite a paginação de produtos, de no máximo 10 produtos por página
    pagination_class = PaginacaoProdutos
    #""Define o conjunto de consultas (queryset) para o ViewSet de Produto, filtrando os produtos com base no papel do usuário autenticado. Se o usuário for um lojista, ele verá todos os produtos; caso contrário, apenas os produtos ativos serão exibidos."""
    def get_queryset(self):

        produtos = Produto.objects.all().order_by('id')

        status = self.request.query_params.get('status')
        categoria = self.request.query_params.get('category')
        preco_min = self.request.query_params.get('min_price')
        preco_max = self.request.query_params.get('max_price')
        busca_produto = self.request.query_params.get('search')

        if (
             self.request.user.is_authenticated and self.request.user.groups.filter(name='Lojistas').exists()
        ):
             #""Se o usuário estiver autenticado e for um lojista, filtra os produtos com base no parâmetro de status fornecido na requisição. Se o status for 'active', retorna apenas os produtos ativos; se for 'inactive', retorna apenas os produtos inativos; caso contrário, retorna todos os produtos.""
             if status == 'active':
                    produtos = produtos.filter(ativo=True).order_by('id')
             
             elif status == 'inactive':
                    produtos = produtos.filter(ativo=False).order_by('id')
             else:
                    produtos =  Produto.objects.all().order_by('id')
                  

        else:
                produtos = Produto.objects.filter(ativo=True).order_by('id')
        #""Se o parâmetro de categoria for fornecido na requisição, filtra os produtos com base na categoria especificada, retornando apenas os produtos pertencentes a essa categoria.""
        if categoria:
            if categoria.isdigit() and int(categoria) > 0:
                produtos = produtos.filter(categoria__id=categoria).order_by('id')
            else: 
                 raise ValidationError({
                      "category" : "A categoria deve ter um ID numérico positivo de 1 a 7"
                 })

        # busca de produtos por um preço maior ou igual, e verifica se é realmente um número ou um número negativo ou uma string
        if preco_min:
            try: 
                preco_min=Decimal(preco_min)
                if preco_min < 0:
                      raise ValidationError({
                           "min_price" : "O preço mínimo não pode ser um número negativo"
                      })
                
                produtos = produtos.filter(preco__gte=preco_min).order_by('id')
            except InvalidOperation:
                raise ValidationError({
                     "min_price" : "Insira um número válido para o preço mínimo"
                })

        # busca de produtos por um preço menor ou igual, e verifica se é realmente um número ou um número negativo ou uma string
        if preco_max:
            try: 
                preco_max = Decimal(preco_max)
                if preco_max < 0:
                     raise ValidationError({
                          "max_price" : "O preço máximo não pode ser um número negativo"
                     })
                  
                produtos = produtos.filter(preco__lte=preco_max).order_by('id')

            except InvalidOperation:
                raise ValidationError({
                    "max_price" : "Insira um número válido para o preço máximo"
                 })
        # Verifica se o preço mínimo é realmente menor ou igual que o preço máximo
        if preco_min and preco_max:
            if preco_min > preco_max: 
                 raise ValidationError({
                    "min_price" : "O preço mínimo não pode ser maior que o preço máximo"     
                 })

        # busca produtos pelo nome digitado (não diferencia de letras maiúsculas e minúsculas)
        if busca_produto:
             produtos = produtos.filter(nome__icontains=busca_produto)

        return produtos
    
    serializer_class = ProdutoSerializer 
    #""Define as permissões para o ViewSet de Produto, permitindo que usuários autenticados com permissões de modelo possam realizar operações de leitura e escrita, enquanto usuários anônimos podem apenas ler os dados.""
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    #""Define os métodos HTTP permitidos para o ViewSet de Produto, mas não permitindo exclusão (DELETE).""
    http_method_names = ['get', 'post', 'put', 'patch', 'head', 'options']

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
            #""Definimos que o método HTTP DELETE não é permitido nem para clientes e nem para o lojista( não exclui variacões e sim o estoquel)
    http_method_names = ['get', 'post', 'put', 'patch', 'head', 'options']
    
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

