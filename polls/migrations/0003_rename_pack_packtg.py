# Generated by Django 4.1.7 on 2023-08-21 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_alter_pack_reference'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Pack',
            new_name='PackTG',
        ),
    ]