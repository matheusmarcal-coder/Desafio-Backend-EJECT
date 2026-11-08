from django_filters import rest_framework as filters 
from NewStyle.models import Produto 
from rest_framework.exceptions import ValidationError

class ProdutoFilter(filters.FilterSet):
    category = filters.NumberFilter( field_name = 'categoria_id')
    min_price = filters.NumberFilter( field_name = 'preco' , lookup_expr= 'gte')
    max_price = filters.NumberFilter ( field_name= 'preco' , lookup_expr= 'lte')
    search = filters.CharFilter (field_name = 'nome', lookup_expr = 'icontains')
    class Meta:
        model = Produto 
        fields = ['category', 'min_price', 'max_price', 'search']

    def filter_queryset(self, queryset ):
        dados = self.form.cleaned_data

        categoria = dados.get('category')
        preco_min = dados.get('min_price')
        preco_max = dados.get('max_price')

        if categoria is not None:
            if categoria <= 0 or categoria != int(categoria):
                raise ValidationError({
                    'category' : 'A categoria deve ter um ID inteiro e positivo'
                })
        if preco_min is not None and preco_min < 0:
            raise ValidationError({
                'min_price' : 'O preço mínimo não pode ser um número negativo'
            })
        if preco_max is not None and preco_min is not None and (preco_max < preco_min): 
            raise ValidationError({
                'min_price' : 'O preço mínimo não pode ser maior que o preço máximo'
            })
        if preco_max is not None and preco_max <0:
            raise ValidationError({
                'preco_max' : 'O preço máximo não pode ser um número negativo'
            })

        return super().filter_queryset(queryset)