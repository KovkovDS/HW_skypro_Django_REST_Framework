from django.core.management.base import BaseCommand
from django.core.management import call_command
from users.models import User, Payments


class Command(BaseCommand):
    help = 'Load test data from fixture'

    def handle(self, *args, **kwargs):
        User.objects.all().delete()
        Payments.objects.all().delete()

        call_command('loaddata', 'users/fixtures/users.json')
        self.stdout.write(self.style.SUCCESS('Successfully loaded data from fixture'))
