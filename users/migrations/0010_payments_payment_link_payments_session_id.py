# Generated by Django 5.1.6 on 2025-03-23 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_payments_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payments',
            name='payment_link',
            field=models.URLField(blank=True, max_length=400, null=True, verbose_name='Ссылка на оплату'),
        ),
        migrations.AddField(
            model_name='payments',
            name='session_id',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ID сессии'),
        ),
    ]
