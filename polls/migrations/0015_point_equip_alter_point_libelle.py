# Generated by Django 4.1.7 on 2023-03-19 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0014_circcst_circreg_chaufferie_nbcirccst_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='point',
            name='equip',
            field=models.CharField(default='equipement', max_length=200),
        ),
        migrations.AlterField(
            model_name='point',
            name='libelle',
            field=models.CharField(default='libellé', max_length=200),
        ),
    ]