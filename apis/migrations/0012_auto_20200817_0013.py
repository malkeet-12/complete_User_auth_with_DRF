# Generated by Django 3.0.8 on 2020-08-16 18:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0011_auto_20200816_2359'),
    ]

    operations = [
        migrations.RenameField(
            model_name='forgotpassword',
            old_name='exipred_time',
            new_name='expired_time',
        ),
    ]
