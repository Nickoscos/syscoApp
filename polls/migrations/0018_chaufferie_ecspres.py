# Generated by Django 4.1.7 on 2023-04-11 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0017_general'),
    ]

    operations = [
        migrations.AddField(
            model_name='chaufferie',
            name='ECSpres',
            field=models.BooleanField(default=False),
        ),
    ]
