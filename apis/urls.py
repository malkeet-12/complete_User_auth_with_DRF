from django.urls import path,include
from . views import*
from apis import views
urlpatterns = [
	path('register', RegisterationView.as_view()),
	path('login', LoginView.as_view()),
	path('logout', LogoutView.as_view()),
	path('change-password' ,ChangePasswordView.as_view()),
	path('forgot-password' ,ForgotPasswordView.as_view()),
	path('confirm-token' , ConfirmToken.as_view())
]