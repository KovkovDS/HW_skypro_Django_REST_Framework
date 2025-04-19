from django.core.management.base import BaseCommand
from django.core.management import call_command
from lms.models import Course, Lesson


class Command(BaseCommand):
    help = 'Load test data from fixture'

    def handle(self, *args, **kwargs):
        Course.objects.all().delete()
        Lesson.objects.all().delete()

        call_command('loaddata', 'lms/fixtures/courses_and_lessons_fixture.json')
        self.stdout.write(self.style.SUCCESS('Successfully loaded data from fixture'))
