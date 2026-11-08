

from django.contrib import admin
from django.urls import path, include 
from NewStyle.views import ClienteViewSet, ProdutoViewSet, CategoriaViewSet, VariacaoViewSet, RegistroView
from rest_framework import routers 
from rest_framework_simplejwt.views import TokenObtainPairView



router = routers.DefaultRouter()
router.register('clientes', ClienteViewSet, basename='Clientes')
router.register('produtos', ProdutoViewSet, basename = 'Produtos')
router.register('categorias', CategoriaViewSet, basename = 'Categorias')
router.register('variacoes', VariacaoViewSet, basename = 'Variacoes')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('products/<int:Produto_id>/variations/', VariacaoViewSet.as_view({ 'post' : 'create'}) ),
    path('products/<int:Produto_id>/variations/<int:pk>/', VariacaoViewSet.as_view({ 'put' : 'update'}) ),


#"""Define a URL pattern para login do usuário, mapeando em 'auth/login/' ""
    path('auth/login/', TokenObtainPairView.as_view()),
#"""Define a URL pattern para registro do usuário, mapeando em 'auth/register/' ""
    path('auth/register/', RegistroView.as_view())
]
