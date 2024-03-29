# Generated by Django 2.2.10 on 2024-02-11 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('savings', '0012_auto_20240210_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='savingdeposit',
            name='members_registration_cost',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='savingdeposit',
            name='transaction_cost',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10),
        ),
    ]
