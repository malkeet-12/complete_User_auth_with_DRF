# Generated by Django 3.1 on 2020-08-15 05:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userdetail',
            old_name='address',
            new_name='phone_number',
        ),
    ]
