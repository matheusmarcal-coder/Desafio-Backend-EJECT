

from django.contrib import admin
from django.urls import path, include 
from NewStyle.views import ClienteViewSet, ProdutoViewSet, CategoriaViewSet, VariacaoViewSet, RegistroView, LoginView, CarrinhoViewSet
from rest_framework import routers 





router = routers.DefaultRouter()
router.register('clientes', ClienteViewSet, basename='clientes')
router.register('produtos', ProdutoViewSet, basename = 'produtos')
router.register('categorias', CategoriaViewSet, basename = 'categorias')
router.register('variacoes', VariacaoViewSet, basename = 'variacoes')
router.register('carrinho/itens', CarrinhoViewSet, basename = 'carrinho-itens')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('carrinho/', CarrinhoViewSet.as_view({'get' : 'list'}), name = 'carrinho-list'),
    path('', include(router.urls)),
    path('produtos/<int:Produto_id>/variacoes/', VariacaoViewSet.as_view({ 'post' : 'create'}) ),
    path('produtos/<int:Produto_id>/variacoes/<int:pk>/', VariacaoViewSet.as_view({ 'put' : 'update'}) ),
    


#"""Define a URL pattern para login do usuário, mapeando em 'auth/login/' ""
    path('auth/login/', LoginView.as_view()),
#"""Define a URL pattern para registro do usuário, mapeando em 'auth/register/' ""
    path('auth/registro/', RegistroView.as_view())
]
