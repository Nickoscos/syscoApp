# Generated by Django 4.1.7 on 2023-11-02 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_carteautom_imagerie_carteautom_maxmbus'),
    ]

    operations = [
        migrations.AddField(
            model_name='carteautom',
            name='DO',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
