from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "Load test data from fixture"

    def handle(self, *args, **kwargs):
        Group.objects.all().delete()

        call_command("loaddata", "users/fixtures/groups.json")
        self.stdout.write(self.style.SUCCESS("Successfully loaded data from fixture"))
