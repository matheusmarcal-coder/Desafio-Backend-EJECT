from django.contrib import admin

from NewStyle.models import cliente, produto 

class produtos(admin.ModelAdmin): 
    list_display = ('id', 'nome', 'preco', 'categoria',)
    list_display_links = ('id', 'nome',)
    list_per_page = 10 
    search_fields = ('nome', 'categoria',)

admin.site.register(produto, produtos)

class clientes(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email', 'cpf', 'data_nascimento', 'telefone',)
    list_display_links = ('id', 'nome')
    search_fields = ('nome', 'email',)

admin.site.register(cliente, clientes)