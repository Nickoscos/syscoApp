# Generated by Django 4.1.7 on 2023-03-15 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_delete_liste'),
    ]

    operations = [
        migrations.CreateModel(
            name='point',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=200)),
                ('TM', models.IntegerField()),
                ('TS', models.IntegerField()),
                ('TR', models.IntegerField()),
                ('TC', models.IntegerField()),
            ],
        ),
    ]
