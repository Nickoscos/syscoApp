# Generated by Django 4.1.7 on 2023-11-03 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0014_automate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='automate',
            name='user',
            field=models.CharField(default='', max_length=200),
        ),
    ]
