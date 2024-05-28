# seed_data.py

from django.core.management.base import BaseCommand
from auth_api.models import CustomUser
from invoice.models import Department

class Command(BaseCommand):
    help = 'Seed de dados para criar usuários e departamentos'
   
    def handle(self, *args, **kwargs):
        # Crie departamentos
        departamentos_data = [
             {'name': 'null department'},
            # Adicione mais departamentos conforme necessário
        ]
        for departamento_data in departamentos_data:
            departamento = Department.objects.create(**departamento_data)

            # Crie usuários associados a este departamento
            users_data = [
                {'username': 'admin', 'account_type':'admin', 'email': 'admin@example.com', 'password': 'admin', 'department': departamento, "is_superuser": 1,  "is_staff": 1},
                {'username': 'sandernunes', 'account_type':'admin', 'email': 'sandernunes@example.com', 'password': 'lolo1234', 'department': departamento, "is_superuser": 1,  "is_staff": 1},
            ]
            for user_data in users_data:
                CustomUser.objects.create_user(**user_data)

        self.stdout.write(self.style.SUCCESS('Dados de seed criados com sucesso!'))
