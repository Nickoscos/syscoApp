# Generated by Django 4.1.7 on 2023-04-11 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0020_delete_circcst_remove_chaudiere_nbbruleur_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chaudiere',
            name='bruleurPres',
        ),
    ]
