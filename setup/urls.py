
from django.contrib import admin
from django.urls import path, include 
from NewStyle.views import ClienteViewSet, ProdutoViewSet, CategoriaViewSet, VariacaoViewSet
from rest_framework import routers 

router = routers.DefaultRouter()
router.register('clientes', ClienteViewSet, basename='Clientes')
router.register('produtos', ProdutoViewSet, basename = 'Produtos')
router.register('categorias', CategoriaViewSet, basename = 'Categorias')
router.register('variacoes', VariacaoViewSet, basename = 'Variacoes')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('Produtos/<int:Produto_id>/Variacoes/', VariacaoViewSet.as_view({ 'post' : 'create'}) ),
    path('Produtos/<int:Produto_id>/Variacoes/<int:pk>/', VariacaoViewSet.as_view({ 'put' : 'update'}) ),
]
