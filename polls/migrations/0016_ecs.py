# Generated by Django 4.1.7 on 2023-03-20 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0015_point_equip_alter_point_libelle'),
    ]

    operations = [
        migrations.CreateModel(
            name='ECS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField(default=1)),
                ('nomECS', models.CharField(default='ECS <django.db.models.fields.IntegerField>', max_length=200)),
                ('nbTemp', models.IntegerField(default=1)),
                ('nbBallon', models.IntegerField(default=1)),
                ('nbV3V', models.IntegerField(default=1)),
                ('nbPpe', models.IntegerField(default=2)),
            ],
        ),
    ]
