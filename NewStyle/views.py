from NewStyle.models import Cliente, Produto, Categoria, Usuario, Variacao, ItemCarrinho, Carrinho, Pedido, ItemPedido
from NewStyle.serializers import ClienteSerializer, ProdutoSerializer, CategoriaSerializer, VariacaoSerializer, RegistroSerializer, ItemCarrinhoSerializer, LoginSerializer, PedidoSerializer, ConfirmarPedidoSerializer, AtualizarStatusPedidoSerializer
from rest_framework import viewsets, status 
from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework.permissions import AllowAny, DjangoModelPermissionsOrAnonReadOnly, IsAuthenticated 
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError
from decimal import Decimal, InvalidOperation
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend
from NewStyle.filters import ProdutoFilter
from drf_spectacular.utils import extend_schema
from django.db import transaction
from rest_framework.decorators import action
from django.db.models import F

# Validação dos dados do login via token (JWT)
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer 


class ClienteViewSet(viewsets.ModelViewSet): 
    # Exige autenticação via JWT para acessar os dados dos clientes
    permission_classes = [IsAuthenticated]

    serializer_class = ClienteSerializer 

    # Permite vizualisar clientes (get), mas não apagar editar ou criar
    http_method_names = ['get','head', 'options' ]

    # Define o conjunto de consultas (queryset) para o ViewSet de Cliente, filtrando os clientes associados ao usuário autenticado e ordenando-os pelo campo 'id'.
    def get_queryset(self):
         return Cliente.objects.filter( usuario=self.request.user ).order_by('id')


# Mostra todos os produtos cadastrados no banco, ordenados por ID, e permite operações de leitura e escrita para usuários autenticados com permissões(lojista), enquanto usuários anônimos e clientes podem apenas ler os dados.
class ProdutoViewSet(viewsets.ModelViewSet):
    
    # Define o sistema responsável pela filtragem (DjangoFilterBackend)
    filter_backends = [DjangoFilterBackend]

    # Define os filtros que serão utilizados
    filterset_class = ProdutoFilter 

    # Define o conjunto de consultas (queryset) para o ViewSet de Produto, filtrando os produtos com base no papel do usuário autenticado. Se o usuário for um lojista, ele verá todos os produtos; caso contrário, apenas os produtos ativos serão exibidos.
    queryset = Produto.objects.all().order_by('id')

    # Define o conjunto de consultas (queryset) para o ViewSet de Produto, filtrando os produtos com base no papel do usuário autenticado. Se o usuário for um lojista, ele verá todos os produtos; caso contrário, apenas os produtos ativos serão exibidos.
    def get_queryset(self):
        produtos = Produto.objects.all().order_by('id')
        status = self.request.query_params.get('status')

        # Se o usuário estiver autenticado e for um lojista, filtra os produtos com base no parâmetro de status fornecido na requisição. Se o status for 'active', retorna apenas os produtos ativos; se for 'inactive', retorna apenas os produtos inativos; caso contrário, retorna todos os produtos.
        if ( self.request.user.is_authenticated and self.request.user.groups.filter(name='Lojistas').exists() ):
             
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

    # Define as permissões para o ViewSet de Produto, permitindo que usuários autenticados com permissões de modelo possam realizar operações de leitura e escrita, enquanto usuários anônimos podem apenas ler os dados.
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    # Define os métodos HTTP permitidos para o ViewSet de Produto, mas não permitindo exclusão (DELETE).
    http_method_names = ['get', 'post', 'put', 'patch', 'head', 'options']


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all().order_by('id')
    serializer_class = CategoriaSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class VariacaoViewSet(viewsets.ModelViewSet):
    queryset = Variacao.objects.all().order_by('id')
    serializer_class = VariacaoSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly] 
    # Definimos que o método HTTP DELETE não é permitido nem para clientes e nem para o lojista (não exclui variacões e sim o estoque)
    http_method_names = ['get', 'post', 'put', 'patch', 'head', 'options']


class RegistroView(APIView):

    # Define que usuários sem autenticação possam criar uma conta ("AllowAny")
    permission_classes = [AllowAny]

    @extend_schema(request = RegistroSerializer, responses = {201: RegistroSerializer}, description = "Registro de um novo usuário na plataforma")

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


class CarrinhoViewSet(viewsets.ModelViewSet):

    # Define que apenas usuários autenticados consigam acessar o carrinho 
    permission_classes = [IsAuthenticated]

    serializer_class = ItemCarrinhoSerializer

    # Métodos de requisição permitidos para o carrinho
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options', 'patch']

    # Organizamos a relação de que, cada cliente acessa apenas o seu próprio carrinho 
    def get_queryset(self):
        return ItemCarrinho.objects.filter( carrinho__usuario = self.request.user).order_by('id')
    
    # Quando um carrinho é criado, salvamos o carrinho no banco de seu respectivo usuário, se o carrinho já exite, ele apenas vê a listagem 
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        carrinho, carrinho_criado = Carrinho.objects.get_or_create(usuario = request.user) 
        variacao = serializer.validated_data['variacao']
        quantidade_nova =  serializer.validated_data['quantidade_itens']
        item_no_carrinho = ItemCarrinho.objects.filter( carrinho = carrinho, variacao = variacao ). first()

        # Verificamos se no carrinho já existe aquela variação, se existir: adicionamos a nova quantidade somada com a quantidade já implementada daquela variação. Se, a quantidade total exceder o estoque, retorna uma mensagem de erro e não deixa a operação ser executada
        if item_no_carrinho is not None:
            quantidade_total = item_no_carrinho.quantidade_itens + quantidade_nova
            if quantidade_total > variacao.estoque:
                 raise ValidationError( "A quantidade de itens adicionados não pode ultrapassar o estoque da loja" )
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
    @extend_schema(
            request = None, 
            responses={ 200: {
                   'type': 'objects',
                   'properties' : {
                        'mensagem' : {'type' : 'string'},
                        'pedido_id' : {'type' : 'integer'},
                        'status' : {'type' : 'string'}
                    } 
                }
            },
    description = 'Finaliza o carrinho e cria um rascunho do pedido.'
    )

    @action(detail = False, methods= ['patch'], url_path = 'finalizar')
    def finalizar(self, request):

        with transaction.atomic():
            carrinho = Carrinho.objects.filter(usuario=request.user).first()
            if carrinho is None:
                return Response({'erro' : 'Carrinho não encontrado.'}, status = status.HTTP_404_NOT_FOUND)
            itens = ItemCarrinho.objects.filter(carrinho=carrinho)

            if not itens.exists():
                return Response({'erro' : 'O carrinho está vazio.'}, status = status.HTTP_400_BAD_REQUEST)
            
            if Pedido.objects.filter(usuario=request.user, status = 'rascunho').exists():
                return Response({'erro' : 'Você já tem um pedido em rascunho.'}, status = status.HTTP_409_CONFLICT)
            
            # Criamos o rascunho do possível pedido
            pedido = Pedido.objects.create( usuario = request.user, status = 'rascunho')

            # Criamos uma cópia do que está dentro do carrinho para o pedido 
            for item in itens:
                 ItemPedido.objects.create( pedido=pedido, variacao_pedido = item.variacao, quantidade = item.quantidade_itens, preco_unitario = item.variacao.Produto.preco)

            itens.delete()
            return Response(
                 {
                 'mensagem' : 'Carrinho finalizado com sucesso!',
                 'pedido_id' : pedido.id,
                 'status' : pedido.status
                },
            status = status.HTTP_200_OK
            )


class PedidoViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]

    http_method_names = ['get', 'post', 'head', 'options', 'patch']

    def get_queryset(self):
        # Se o usuário for um lojista, ele verá todos os pedidos feitos 
         if self.request.user.groups.filter(name = 'lojistas').exists():
             pedidos = Pedido.objects.all()

             if self.aciton == 'list':
                # O tipo de filtragem de status do pedido será identificada pelo lojista por meio da URL (exemplo: GET /pedidos/?status= entregue -> só filtra os pedidos com status ENTREGUE)
                filtra_status = self.request.query_params.get('status')
                if filtra_status:
                      pedidos = pedidos.filter(status = filtra_status)

                # Se o status não foi informado pelo lojista na URL: Retorna os pedidos ativos(pendente, confirmado e enviado), dos mais antigos até os mais novos
                else:
                    pedidos= pedidos.filter(status__in = ['pendente', 'confirmado', 'enviado'])
             return pedidos.order_by('pedido_criado')


         else:
            # Se não for um lojista (logo, é um cliente), ele verá apenas o próprio pedido
            return Pedido.objects.filter(usuario = self.request.user).order_by('-pedido_criado')

    @extend_schema(
            request = ConfirmarPedidoSerializer,
            responses = {201: PedidoSerializer},
            description = 'Confirma um pedido em rascunho, tornando-o com status PENDENTE, validando e abaixando o estoque.'
    )

    def create(self, request, *args, **kwargs):
        # Valida os dados enviados no pedido 
        serializer = ConfirmarPedidoSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)

        with transaction.atomic():

            pedido = Pedido.objects.filter(usuario = request.user, status = 'rascunho').first()

            if pedido is None:
                 return Response ({'erro' : 'Você não possui um pedido em rascunho'}, status = status.HTTP_404_NOT_FOUND)
            itens = list(pedido.itens_pedido.all())

            if not itens:
                 return Response ({'erro': 'O seu pedido não possui itens!'}, status = status.HTTP_400_BAD_REQUEST)
            for item in itens:
                 atualizado = Variacao.objects.filter(
                    pk = item.variacao_pedido_id,
                    estoque__gte=item.quantidade,
                    Produto__ativo=True
                 ).update( estoque=F('estoque') - item.quantidade)

            if atualizado == 0:
                 transaction.set_rollback(True)

                 return Response ({
                    'erro': 'Produto inativo ou estoque insuficiente',
                    'item_id': item.id
                 },
                    status = status.HTTP_400_BAD_REQUEST
                 )

            pedido.cep_entrega = serializer.validated_data['cep_entrega']
            pedido.rua_entrega = serializer.validated_data['rua_entrega']
            pedido.numero_entrega = serializer.validated_data['numero_entrega']
            pedido.bairro_entrega =serializer.validated_data['bairro_entrega']
            pedido.cidade_entrega =serializer.validated_data['cidade_entrega']
            pedido.uf_entrega =serializer.validated_data['uf_entrega']

            pedido.metodo_pagamento = serializer.validated_data['metodo_pagamento']

            pedido.status = 'pendente'

            pedido.save(update_fields= [
                'cep_entrega',
                'rua_entrega',
                'numero_entrega',
                'bairro_entrega',
                'cidade_entrega',
                'uf_entrega',
                'metodo_pagamento',
                'status'
            ] )

        return Response({
            'mensagem' : 'Pedido confirmado com sucesso!',
            'pedido_id' : pedido.id,
            'status' : pedido.status
        },
            status = status.HTTP_201_CREATED
        )

    def partial_update(self, request, *args, **kwargs):
        # Permite que apenas usuários que pertencem ao grupo Lojistas podem ataualizar o status do pedido. 
        if not request.user.groups.filter(name = 'lojistas').exists():
             return Response ({'erro' : 'Apenas lojistas podem atualizar pedidos.'}, status = status.HTTP_403_FORBIDDEN)
        pedido = self.get_objects()

        serializer = AtualizarStatusPedidoSerializer(data = request.data)
        serializer.is_valid(raise_exceptions = True)

        novo_status = serializer.validated_data['status']
        transicoes_status = {
             'rascunho' : [],
             'pendente' : ['confirmado', 'cancelado'],
             'confirmado' : ['cancelado', 'enviado'],
             'enviado' : ['entregue'],
             'entregue' : [],
             'cancelado' : []
        }
        if novo_status not in transicoes_status.get(pedido.status, []):
             return Response({ 'erro' : 'Esse tipo de transição de status não é permitido.'},
                             status = status.HTTP_400_BAD_REQUEST
                             )

        with transaction.atomic ():
            if novo_status == 'cancelado':
                for item in pedido.itens_pedido.all():
                    Variacao.objects.filter( pk = item.variacao_pedido_id).update(estoque = F('estoque') + item.quantidade)

            pedido.status = novo_status
            pedido.save(update_fields = ['status'])

        return Response ({
             'mensagem' : 'Stauts do pedido atualizado com sucesso.',
             'pedido_id' : pedido.id,
             'status' : pedido.status
        },
            status = status.HTTP_200_OK
        )