from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from NewStyle.models import Cliente, Produto, Usuario 

class produtos(admin.ModelAdmin): 
    list_display = ('id', 'nome', 'preco', 'categoria',)
    list_display_links = ('id', 'nome',)
    list_per_page = 10 
    search_fields = ('nome', 'categoria',)

admin.site.register(Produto, produtos)

@admin.register(Cliente)
class clientes(admin.ModelAdmin):
    # Mostra o ID do cliente e do usuario associado, definido pelos dados fornecidos no registro 
    list_display = ['id', 'usuario']


class UsuarioAdmin(UserAdmin):
    model = Usuario

admin.site.register(Usuario, UsuarioAdmin)