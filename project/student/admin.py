from django.contrib import admin
from .models import Faculty, Group, Student

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('faculty_name',)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'faculty')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'birth_date', 'phone', 'gender', 'faculty', 'group')
    list_filter = ('faculty', 'group', 'gender')
    search_fields = ('last_name', 'first_name', 'middle_name', 'phone')



