# Generated by Django 3.0.8 on 2020-08-16 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0008_auto_20200815_0828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forgotpassword',
            name='activation_key',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='forgotpassword',
            name='email',
            field=models.EmailField(max_length=100),
        ),
    ]