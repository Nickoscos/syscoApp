# Generated by Django 4.1.7 on 2023-04-11 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0023_chaudiere_nbdef_chaudiere_nbtemp_chaufferie_ecsprepa'),
    ]

    operations = [
        migrations.AddField(
            model_name='ecs',
            name='nbDef',
            field=models.IntegerField(default=1),
        ),
    ]
