# Generated by Django 4.1.7 on 2023-11-09 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0025_chaufferie_ecrannec_chaufferie_modemnec'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chaufferie',
            name='ecranNec',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='chaufferie',
            name='modemNec',
            field=models.BooleanField(default=False),
        ),
    ]
