# Generated by Django 4.1.7 on 2023-04-11 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0022_circreg_nbamb'),
    ]

    operations = [
        migrations.AddField(
            model_name='chaudiere',
            name='nbDef',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='chaudiere',
            name='nbTemp',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='chaufferie',
            name='ECSprepa',
            field=models.BooleanField(default=True),
        ),
    ]
