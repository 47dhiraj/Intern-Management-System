from django.contrib import admin

from .models import User, Task, Attendance

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_staff', 'is_supervisor', 'is_intern', 'created_at']

class TaskAdmin(admin.ModelAdmin):
    list_display = ['tasktitle', 'assignor', 'is_completed']

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['intern', 'status', 'date']


admin.site.register(User, UserAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Attendance, AttendanceAdmin)
