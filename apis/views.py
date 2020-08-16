from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from . serializers import*
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny

from django.http import JsonResponse
from django.contrib.auth import logout, authenticate, login
import uuid 
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now 
from datetime import datetime, timedelta
import datetime
from django.utils import timezone

class RegisterationView(APIView):

	authentication_classes = () 
	def post(self, request, *args, **kwargs):
		context = {}
		try:       
			serializer = CreateUserSerializer(data=request.data)
			if serializer.is_valid():
				user = serializer.save()
				if user:
					context['status'] = True
					context['message'] = 'Registration successfully please login to continue.'
			else:
				context['message'] = serializer.errors
				context['status']   = False
		except Exception as e:
			raise e
			context['message'] = 'Something went wrong,please try again.'   
		return Response(context)


class LoginView(APIView):
	"""
	An endpoint for Login user
	"""
	authentication_classes = ()
	def post(self, request):
		context = {}
		try:
			username = request.data.get('username')
			password = request.data.get('password')
			user = authenticate(username=username, password=password)
			if user:
				token, created = Token.objects.get_or_create(user=user)
				print(user)
				context['success']= True
				if user.is_superuser or user.is_staff:
					context['is_superuser']= True
				else:
					context['is_superuser']= False
				context['message'] = 'Login Successfull'
				context['data'] = { 'token': token.key }
				context['user'] = {'username': username}
				login(request, user)
			else:
				context['success'] = False
				context['message'] = 'Invalid username or password'
		except Exception as e:    
			context['success'] = False
			context['message'] = str(e)
			print(e)
		return Response(context)

class LogoutView(APIView):
	"""
	An endpoint for Logout user.
	"""

	permission_classes = [IsAuthenticated]
	def post(self, request):
		context = {}
		try:
			request.user.auth_token.delete()
			context['message'] = 'Token deleted' 
		except Exception as e:
			context['status'] = False
			context['msg'] = 'Cannot access token'
		logout(request)
		context['status'] = True
		context['success'] = 'You have been logged out'
		return Response(context)




class ChangePasswordView(APIView):
	"""
	An endpoint for changing password.
	"""
	permission_classes = (IsAuthenticated,)

	def get_object(self, queryset=None):
		obj = self.request.user
		return obj

	def put(self, request, *args, **kwargs):
		context={}
		self.object = self.get_object()
		serializer  = ChangePasswordSerializer(data=request.data)
		if serializer.is_valid():
			# Check old password
			if not self.object.check_password(serializer.data.get("old_password")):
				context['status'] = False
				context["old_password"] = 'old_password is wrong'
				return Response(context)
			self.object.set_password(serializer.data.get("new_password"))
			self.object.save()
			context['status'] =True
			context['message'] ='Password updated successfully'
			context['data'] = serializer.data
		return Response(context)


class ForgotPasswordView(APIView):
	authentication_classes = ()
	def post(self,request):
		context ={}
		try:
			email = request.data.get('email')
			# now =  timezone.now()
			# expired_time = now + datetime.timedelta(seconds=15)
			match = User.objects.get(email=email)
			activation_key = uuid.uuid4().hex[:6].upper()
			db = ForgotPassword(email=email,activation_key=activation_key)
			db.save()
			send_mail('Token verification',
					  activation_key,
					  settings.EMAIL_HOST_USER,
					  [email],
					  fail_silently=False,)
			context['status']= True
			context['message']= 'successfully saved' 
		except Exception as e:    
			context['success'] = False
			context['message'] = str(e)
		return Response(context)



# class ConfirmToken(APIView):
# 	authentication_classes = ()
# 	def post(self,request,*args,**kwargs):
# 		context = {}
# 		email = request.data.get('email')
# 		activation_key = request.data.get('token')
# 		try:
# 			match = ForgotPassword.objects.get(activation_key=activation_key)
# 			if match:
# 				latest = ForgotPassword.objects.latest('id')
# 				if latest.activation_key == activation_key and latest.is_deleted == False and latest.email==email:
# 					user = User.objects.get(email=email)
# 					user.set_password(request.data.get('new_password'))
# 					latest.is_deleted = True
# 					user.save()
# 					latest.save()
# 					context['status'] = True
# 					context['message'] = 'successfully reset password'
# 					return Response(context)
# 				else:
# 					context['status'] = False
# 					context['status'] = 'Invalid Token please Generate new Token'
# 					return Response(context)
# 			else:
# 				context['status'] = False
# 				context['message'] = 'Token doesnot exists'
# 				return Response(context)
# 		except Exception as e:    
# 			context['success'] = False
# 			context['message'] = str(e)
# 			print(e)
# 		return Response(context)



# one_time = Share_url.objects.get(key=uidb64)
#             print(one_time)
#             if one_time:
#                 one_time.checked = True
#                 exp_time = one_time.expired_time
#                 now = datetime.datetime.now()
#                 if now > exp_time:
#                     return HttpResponse('link is expired')




class ConfirmToken(APIView):
	authentication_classes = ()
	def post(self,request,*args,**kwargs):
		context = {}
		email = request.data.get('email')
		activation_key = request.data.get('token')
		try:
			match = ForgotPassword.objects.filter(email = email)
			latest = match.latest('id')
			#exp_time = latest.expired_time
			#now =  timezone.now()
			if latest.activation_key == activation_key:
				if latest.is_deleted == False :		
					user = User.objects.get(email=email)
					user.set_password(request.data.get('new_password'))
					latest.is_deleted = True
					user.save()
					latest.save()
					context['status'] = True
					context['message'] = 'successfully reset password'
					return Response(context)				
				else:
					context['status'] = False
					context['message'] = 'This token is already use please Generate new one'
					return Response(context)
			else:
				context['status'] = False
				context['message'] = 'Invalid Token'
				return Response(context)
		except Exception as e:    
			context['success'] = False
			context['message'] = 'wrong email'
			print(e)
		return Response(context)


