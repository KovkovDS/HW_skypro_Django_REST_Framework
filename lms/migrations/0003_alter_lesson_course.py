# Generated by Django 5.1.6 on 2025-03-14 17:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0002_alter_course_options_alter_lesson_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='lms.course', verbose_name='Курс'),
        ),
    ]
