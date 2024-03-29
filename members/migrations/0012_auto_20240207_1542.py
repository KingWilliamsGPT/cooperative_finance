# Generated by Django 2.2.10 on 2024-02-07 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0011_auto_20240207_1454'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='kin1',
        ),
        migrations.RemoveField(
            model_name='member',
            name='kin2',
        ),
        migrations.AddField(
            model_name='member',
            name='next_of_kin_name',
            field=models.CharField(blank=True, max_length=256, verbose_name='Next of Kin Name'),
        ),
        migrations.AddField(
            model_name='member',
            name='next_of_kin_phone_no',
            field=models.CharField(blank=True, max_length=256, verbose_name='Next of Kin Phone Number'),
        ),
        migrations.AddField(
            model_name='member',
            name='relationship_type',
            field=models.CharField(choices=[('PARENT', 'Parent'), ('MOTHER', 'Mother'), ('FATHER', 'Father'), ('CHILD', 'Child'), ('SON', 'Son'), ('DAUGHTER', 'Daughter'), ('SIBLING', 'Sibling'), ('BROTHER', 'Brother'), ('SISTER', 'Sister'), ('GRANDPARENT', 'Grandparent'), ('GRANDMOTHER', 'Grandmother'), ('GRANDFATHER', 'Grandfather'), ('GRANDCHILD', 'Grandchild'), ('GRANDSON', 'Grandson'), ('GRANDDAUGHTER', 'Granddaughter'), ('UNCLE', 'Uncle'), ('AUNT', 'Aunt'), ('COUSIN', 'Cousin'), ('NIECE', 'Niece'), ('NEPHEW', 'Nephew'), ('SPOUSE', 'Spouse'), ('HUSBAND', 'Husband'), ('WIFE', 'Wife'), ('PARTNER', 'Partner')], default='WIFE', max_length=20),
            preserve_default=False,
        ),
    ]
