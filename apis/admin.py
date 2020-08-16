from django.contrib import admin
from . models import UserDetail,ForgotPassword
# Register your models here.
admin.site.register(UserDetail)


class ForgotPasswordAdmin(admin.ModelAdmin):
    list_display = ('id','email','created_at','activation_key','is_deleted','expired_time')
admin.site.register(ForgotPassword, ForgotPasswordAdmin)