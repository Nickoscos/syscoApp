# Generated by Django 4.1.7 on 2023-11-03 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0015_alter_automate_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='automate',
            name='id',
        ),
        migrations.AddField(
            model_name='automate',
            name='carteautom_ptr',
            field=models.OneToOneField(auto_created=True, default=0, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='polls.carteautom'),
            preserve_default=False,
        ),
    ]
