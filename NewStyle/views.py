from NewStyle.models import Cliente, Produto, Categoria, Usuario, Variacao, ItemCarrinho, Carrinho 

from NewStyle.serializers import ClienteSerializer, ProdutoSerializer, CategoriaSerializer, VariacaoSerializer, RegistroSerializer, ItemCarrinhoSerializer

from rest_framework import viewsets, status 

from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework.permissions import AllowAny, DjangoModelPermissionsOrAnonReadOnly, IsAuthenticated 
from rest_framework.pagination import PageNumberPagination

from rest_framework.exceptions import ValidationError

from decimal import Decimal, InvalidOperation

from NewStyle.serializers import LoginSerializer

from rest_framework_simplejwt.views import TokenObtainPairView

from django_filters.rest_framework import DjangoFilterBackend

from NewStyle.filters import ProdutoFilter

class ClienteViewSet(viewsets.ModelViewSet): 
    #""Exige autenticação via JWT para acessar os dados dos clientes
    permission_classes = [IsAuthenticated]
    serializer_class = ClienteSerializer 
    # Permite vizualisar clientes (get), mas não apagar editar ou criar
    http_method_names = ['get','head', 'options' ]
    #"""Define o conjunto de consultas (queryset) para o ViewSet de Cliente, filtrando os clientes associados ao usuário autenticado e ordenando-os pelo campo 'id'."""
    def get_queryset(self):
         return Cliente.objects.filter(
              usuario=self.request.user
         ).order_by('id')
    


# Mostra todos os produtos cadastrados no banco, ordenados por ID, e permite operações de leitura e escrita para usuários autenticados com permissões(lojista), enquanto usuários anônimos e clientes podem apenas ler os dados.
class ProdutoViewSet(viewsets.ModelViewSet):
    #Define o sistema responsável pela filtragem (DjangoFilterBackend)
    filter_backends = [DjangoFilterBackend]

    #Define os filtros que serão utilizados
    filterset_class = ProdutoFilter 

    #""Define o conjunto de consultas (queryset) para o ViewSet de Produto, filtrando os produtos com base no papel do usuário autenticado. Se o usuário for um lojista, ele verá todos os produtos; caso contrário, apenas os produtos ativos serão exibidos."""
    queryset = Produto.objects.all().order_by('id')

    #""Define o conjunto de consultas (queryset) para o ViewSet de Produto, filtrando os produtos com base no papel do usuário autenticado. Se o usuário for um lojista, ele verá todos os produtos; caso contrário, apenas os produtos ativos serão exibidos."""
    def get_queryset(self):

        produtos = Produto.objects.all().order_by('id')

        status = self.request.query_params.get('status')
       

        #""Se o usuário estiver autenticado e for um lojista, filtra os produtos com base no parâmetro de status fornecido na requisição. Se o status for 'active', retorna apenas os produtos ativos; se for 'inactive', retorna apenas os produtos inativos; caso contrário, retorna todos os produtos.""
        if (
             self.request.user.is_authenticated and self.request.user.groups.filter(name='Lojistas').exists()
        ):
             
             if status == 'active':
                    produtos = produtos.filter(ativo=True).order_by('id')
             
             elif status == 'inactive':
                    produtos = produtos.filter(ativo=False).order_by('id')
             else:
                    produtos =  Produto.objects.all().order_by('id')
                  
        # Se o usuário não for um lojsita, o cliente só vera produtos ativos, ordenados por ID
        else:
                produtos = Produto.objects.filter(ativo=True).order_by('id')
    

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

class LoginView(TokenObtainPairView):
     serializer_class = LoginSerializer 


class CarrinhoViewSet(viewsets.ModelViewSet):
    # Define que apenas usuários autenticados consigam acessar o carrinho 
    permission_classes = [IsAuthenticated]
    serializer_class = ItemCarrinhoSerializer
    # Métodos de requisição permitidos para o carrinho
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options']
    # Organizamos a relação de que, cada cliente acessa apenas o seu próprio carrinho 
    def get_queryset(self):
        return ItemCarrinho.objects.filter( carrinho__usuario = self.request.user)
    # Quando um carrinho é criado, salvamos o carrinho no banco de seu respectivo usuário, se o carrinho já exite, ele apenas vê a listagem 
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)

        carrinho, carrinho_criado = Carrinho.objects.get_or_create(usuario = request.user) 

        variacao = serializer.validated_data['variacao']
        quantidade_nova =  serializer.validated_data['quantidade_itens']

        item_no_carrinho = ItemCarrinho.objects.filter(
             carrinho = carrinho,
             variacao = variacao
        ). first()


        # Verificamos se no carrinho já existe aquela variação, se existir: adicionamos a nova quantidade somada com a quantidade já implementada daquela variação. Se, a quantidade total exceder o estoque, retorna uma mensagem de erro e não deixa a operação ser executada
        if item_no_carrinho is not None:
            quantidade_total = item_no_carrinho.quantidade_itens + quantidade_nova
            if quantidade_total > variacao.estoque:
                 raise ValidationError(
                      "A quantidade de itens adcionados não pode ultrapassar o estoque da loja"
                 )
            item_no_carrinho.quantidade_itens = quantidade_total
            item_no_carrinho.save(update_fields=['quantidade_itens'])

            resposta_HTTP = status.HTTP_200_OK
            item = item_no_carrinho
        else:
            item = serializer.save(carrinho=carrinho)
            resposta_HTTP = status.HTTP_201_CREATED
        return Response(self.get_serializer(item).data, status= resposta_HTTP)
        # Permite a atualização dos itens do carrinho via PUT, logo, apenas os campos em que o cliente dejesa atualizar(quantidade do item, por exmeplo), sem precisar atualizar tudo de uma única vez (de forma desnecessária), 
        def update(self, request, *args, **kwargs):
            kwargs['partial'] = True
            return super().update(request, *args, **kwargs)