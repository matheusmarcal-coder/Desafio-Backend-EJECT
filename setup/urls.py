
from django.contrib import admin
from django.urls import path, include 
from NewStyle.views import ClienteViewSet, ProdutoViewSet, CategoriaViewSet
from rest_framework import routers 

router = routers.DefaultRouter()
router.register('clientes', ClienteViewSet, basename='Clientes')
router.register('produtos', ProdutoViewSet, basename = 'Produtos')
router.register('categorias', CategoriaViewSet, basename = 'Categorias')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]
