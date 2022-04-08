from django.contrib import admin

from .models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_staff', 'is_supervisor', 'is_intern', 'created_at']

admin.site.register(User, UserAdmin)
