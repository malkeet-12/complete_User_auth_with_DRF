from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
User._meta.get_field('email')._unique = True
User._meta.get_field('username')._unique = True
# Create your models here.


class UserDetail(models.Model):
	""" This model contains User information"""
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	phone_number = models.CharField(max_length=100)

class ForgotPassword(models.Model):
	email = models.EmailField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True,null=True)
	expired_time = models.DateTimeField(auto_now=False,null=True)
	is_deleted = models.BooleanField(default=False,)
	activation_key =  models.CharField(max_length=100)