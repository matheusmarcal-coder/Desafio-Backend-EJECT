from django.contrib import admin
from django.urls import path, include 
from NewStyle.views import ClienteViewSet, ProdutoViewSet, CategoriaViewSet, VariacaoViewSet, RegistroView, LoginView, CarrinhoViewSet, PedidoViewSet, MetodoPagamentoViewSet, EsqueciSenhaView, RedefinirSenhaView
from rest_framework import routers
from drf_spectacular.views import ( SpectacularAPIView, SpectacularSwaggerView) 


router = routers.DefaultRouter()
router.register('clientes', ClienteViewSet, basename='clientes')
router.register('produtos', ProdutoViewSet, basename = 'produtos')
router.register('categorias', CategoriaViewSet, basename = 'categorias')
router.register('variacoes', VariacaoViewSet, basename = 'variacoes')
router.register('carrinho/itens', CarrinhoViewSet, basename = 'carrinho-itens')
router.register('pedidos', PedidoViewSet, basename = 'pedidos')
router.register('metodos_pagamento', MetodoPagamentoViewSet, basename = 'metodos_pagamento')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('carrinho/', CarrinhoViewSet.as_view({'get' : 'list'}), name = 'carrinho-list'),
    path('', include(router.urls)),
    path('produtos/<int:Produto_id>/variacoes/', VariacaoViewSet.as_view({ 'post' : 'create'}) ),
    path('produtos/<int:Produto_id>/variacoes/<int:pk>/', VariacaoViewSet.as_view({ 'put' : 'update'}) ),
    
# Define a URL pattern para login do usuário, mapeando em 'auth/login/' 
    path('auth/login/', LoginView.as_view()),

# Define a URL pattern para registro do usuário, mapeando em 'auth/register/' 
    path('auth/registro/', RegistroView.as_view()),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name = 'swagger-ui'),

    path('auth/esqueci_senha/', EsqueciSenhaView.as_view(), name='esqueci_senha'),

    path('auth/redefinir_senha/', RedefinirSenhaView.as_view(), name='redefinir_senha'),
]
