from django.http import JsonResponse

def clientes(request):
    if request.method == 'GET':
        cliente = {
            'id' : '1',
            'nome': 'cliente 1'
        }
        return JsonResponse(cliente)