# Generated by Django 2.2.10 on 2024-01-26 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0008_member_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='middle_name',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]
