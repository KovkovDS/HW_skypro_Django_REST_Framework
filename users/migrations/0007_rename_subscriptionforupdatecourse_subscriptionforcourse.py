# Generated by Django 5.1.6 on 2025-03-14 19:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0003_alter_lesson_course'),
        ('users', '0006_subscriptionforupdatecourse'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SubscriptionForUpdateCourse',
            new_name='SubscriptionForCourse',
        ),
    ]
