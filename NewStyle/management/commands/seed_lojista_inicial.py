import os 

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group 
from NewStyle.models import Usuario 

class Command(BaseCommand):
    help = 'Cria o usuário inicial do tipo LOJISTA e adiciona ao grupo "Lojistas".'

    def handle(self, *args, **kwargs):
        email = os.environ['LOJISTA_EMAIL']
        senha = os.environ['LOJISTA_SENHA']

        # Verifica se o grupo "Lojistas" existe, caso contrário, cria-o
        grupo_lojistas, criado = Group.objects.get_or_create(name='Lojistas')

        usuario, criado_usuario = Usuario.objects.get_or_create(
            email = email,
            defaults = {
                'username': email,
                'papel': Usuario.Papel.LOJISTA
            }
        )
        # Verifica se o usuário foi criado e adiciona ao grupo "Lojistas"
        if criado_usuario: 
            usuario.set_password(senha)
            usuario.save()
        # caso o usuário já exista, verifica se ele é do tipo LOJISTA
        else:
            if usuario.papel != Usuario.Papel.LOJISTA:
                raise CommandError(f"O usuário com email '{email}' já existe, e pertence a outro tipo de usuário.")



        # Garante que: se a conta foi criada agora, será adcionada no grupo Lojistas, caso a conta já exista no grupo Lojistas, nada será feito"
        usuario.groups.add(grupo_lojistas)
        
        self.stdout.write(self.style.SUCCESS(f"Usuário inicial do tipo LOJISTA configurado com sucesso. Email: {email}"))
