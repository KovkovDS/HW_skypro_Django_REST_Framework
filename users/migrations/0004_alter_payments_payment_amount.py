# Generated by Django 5.1.6 on 2025-03-07 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_payments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payments',
            name='payment_amount',
            field=models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Сумма оплаты'),
        ),
    ]
