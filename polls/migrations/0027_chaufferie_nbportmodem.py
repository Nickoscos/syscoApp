# Generated by Django 4.1.7 on 2023-11-09 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0026_alter_chaufferie_ecrannec_alter_chaufferie_modemnec'),
    ]

    operations = [
        migrations.AddField(
            model_name='chaufferie',
            name='nbPortModem',
            field=models.IntegerField(default=5),
        ),
    ]