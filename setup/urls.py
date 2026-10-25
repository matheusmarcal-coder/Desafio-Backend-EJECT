
from django.contrib import admin
from django.urls import path, include 
from NewStyle.views import clienteViewSet, produtoViewSet
from rest_framework import routers 

router = routers.DefaultRouter()
router.register('clientes', clienteViewSet, basename='clientes')
router.register('produtos', produtoViewSet, basename = 'produtos')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]
