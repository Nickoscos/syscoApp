# Generated by Django 4.1.7 on 2023-04-11 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0016_ecs'),
    ]

    operations = [
        migrations.CreateModel(
            name='General',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField(default=1)),
                ('nomGen', models.CharField(default='Général ', max_length=200)),
                ('nbDefaut', models.IntegerField(default=1)),
                ('nbTempExt', models.IntegerField(default=1)),
            ],
        ),
    ]
