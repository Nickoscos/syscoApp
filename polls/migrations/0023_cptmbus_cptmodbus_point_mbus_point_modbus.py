# Generated by Django 4.1.7 on 2023-11-07 20:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0022_chaufferie_nbimp_chaufferie_nbmbus_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CptMbus',
            fields=[
                ('point_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='polls.point')),
            ],
            bases=('polls.point',),
        ),
        migrations.CreateModel(
            name='CptModbus',
            fields=[
                ('point_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='polls.point')),
            ],
            bases=('polls.point',),
        ),
        migrations.AddField(
            model_name='point',
            name='Mbus',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='point',
            name='Modbus',
            field=models.IntegerField(default=0),
        ),
    ]