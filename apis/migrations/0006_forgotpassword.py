# Generated by Django 3.1 on 2020-08-15 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0005_delete_forgotpassword'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForgotPassword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('activation_key', models.CharField(max_length=100)),
            ],
        ),
    ]
