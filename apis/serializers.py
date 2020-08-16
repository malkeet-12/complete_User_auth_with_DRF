from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from django.contrib.auth.password_validation import validate_password





class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields = ['phone_number']



class CreateUserSerializer(serializers.ModelSerializer):
	profile = ProfileSerializer(required=True)
	class Meta:
		model = User
		fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name','profile')

	def create(self, validated_data):
		username = validated_data['username']
		email = validated_data['email']
		first_name=validated_data['first_name']
		last_name=validated_data['last_name']
		password = validated_data['password']
		profile_data = validated_data.pop('profile')
		user = User.objects.create_user(username=username,email=email,first_name=first_name,last_name=last_name,password=password)
		profile = UserDetail.objects.create(user = user,phone_number = profile_data['phone_number'])
		#user.set_password(validated_data['password'])
		return user


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)