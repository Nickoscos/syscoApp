# Generated by Django 4.1.7 on 2023-04-17 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0025_alter_chaudiere_nbtemp'),
    ]

    operations = [
        migrations.AddField(
            model_name='point',
            name='Supp',
            field=models.BooleanField(default=False),
        ),
    ]