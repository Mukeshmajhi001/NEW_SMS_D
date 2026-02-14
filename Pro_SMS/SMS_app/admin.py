from django.contrib import admin

# Register your models here.
from .models import Student, Teacher, Department, Parent

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'department']
    search_fields = ['name', 'phone', 'email']

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email']
    search_fields = ['name', 'phone', 'email']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'student']
    
    
from .models import HomeImage

@admin.register(HomeImage)
class HomeImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'uploaded_at']
    list_editable = ['order', 'is_active']